"""
AI Code Reviewer
Runs Claude on changed files in a PR. Can be used standalone or as a GitHub Action.
"""
from typing import Dict, List, Optional
import json
import os
import subprocess
import sys
from pathlib import Path

import anthropic
import requests

# Validate API key at startup
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
    print("Get your key at: https://console.anthropic.com")
    sys.exit(1)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".java", ".rs", ".cpp", ".c", ".cs"}


def get_changed_files() -> List[str]:
    """Get source files changed in the current PR/commit.

    Returns:
        List of changed file paths with supported extensions
    """
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True,
        text=True,
    )
    files = [f.strip() for f in result.stdout.split("\n") if f.strip()]
    return [f for f in files if Path(f).suffix in SUPPORTED_EXTENSIONS]


def get_diff(file_path: str) -> str:
    """Get the git diff for a specific file.

    Args:
        file_path: Relative path to the file

    Returns:
        Diff string (truncated to 6000 chars)
    """
    result = subprocess.run(
        ["git", "diff", "HEAD~1", "HEAD", "--", file_path],
        capture_output=True,
        text=True,
    )
    return result.stdout[:6000]


def get_file_content(file_path: str) -> str:
    """Get the current content of a file.

    Args:
        file_path: Path to the file

    Returns:
        File content (truncated to 8000 chars), or empty string if not found
    """
    try:
        with open(file_path) as f:
            return f.read()[:8000]
    except FileNotFoundError:
        return ""


def review_file(file_path: str, diff: str, content: str) -> Dict[str, object]:
    """Get Claude's review of a changed file.

    Args:
        file_path: Path to the file being reviewed
        diff: Git diff for the file
        content: Current full file content

    Returns:
        Dictionary with overall_rating, summary, issues, positives, and suggestions

    Raises:
        ValueError: If Claude returns invalid JSON
    """
    prompt = f"""Review this code change as a senior engineer. Be constructive and specific.

FILE: {file_path}
DIFF:
```
{diff}
```

FULL FILE CONTEXT:
```
{content[:4000]}
```

Provide a JSON review with exactly these keys:
{{
  "overall_rating": "<Approve|Request Changes|Needs Discussion>",
  "summary": "<1-2 sentence summary of the changes>",
  "issues": [
    {{
      "severity": "<Critical|High|Medium|Low>",
      "line_hint": "<approximate line or function>",
      "issue": "<what is wrong>",
      "fix": "<how to fix it>"
    }}
  ],
  "positives": ["<good thing 1>", "<good thing 2>"],
  "security_concerns": ["<concern>"],
  "performance_notes": ["<note>"],
  "suggestions": ["<improvement>"]
}}

Return ONLY valid JSON."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Claude returned invalid JSON: {e}\nResponse: {raw}") from e


def post_github_comment(comment: str) -> None:
    """Post a review comment to a GitHub PR.

    Args:
        comment: Markdown-formatted comment body
    """
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    pr_number = os.environ.get("PR_NUMBER", "")

    if not all([token, repo, pr_number]):
        print("[GitHub] Missing env vars (GITHUB_TOKEN, GITHUB_REPOSITORY, PR_NUMBER), printing instead:")
        print(comment)
        return

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    requests.post(
        url,
        json={"body": comment},
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        },
    )


def format_review(file_path: str, review: Dict[str, object]) -> str:
    """Format a review dictionary as Markdown.

    Args:
        file_path: Path to the reviewed file
        review: Review dictionary from review_file()

    Returns:
        Markdown-formatted review string
    """
    rating = review.get("overall_rating", "")
    emoji = {"Approve": "✅", "Request Changes": "🔴", "Needs Discussion": "🟡"}.get(rating, "⚪")

    md = [f"## {emoji} `{file_path}` — {rating}", f"\n{review.get('summary', '')}\n"]

    if review.get("issues"):
        md.append("### Issues Found")
        for issue in review["issues"]:
            sev_emoji = {"Critical": "🚨", "High": "⚠️", "Medium": "📝", "Low": "💡"}.get(
                issue["severity"], "📝"
            )
            md.append(f"\n**{sev_emoji} {issue['severity']}** — `{issue.get('line_hint', '')}`")
            md.append(f"- **Problem:** {issue['issue']}")
            md.append(f"- **Fix:** {issue['fix']}")

    if review.get("security_concerns"):
        md.append("\n### 🔒 Security Concerns")
        for c in review["security_concerns"]:
            md.append(f"- {c}")

    if review.get("positives"):
        md.append("\n### 👍 What's Good")
        for p in review["positives"]:
            md.append(f"- {p}")

    if review.get("suggestions"):
        md.append("\n### 💡 Suggestions")
        for s in review["suggestions"]:
            md.append(f"- {s}")

    return "\n".join(md)


def run_review(files: Optional[List[str]] = None) -> Optional[str]:
    """Run a full code review on changed files.

    Args:
        files: List of file paths to review. If None, detects changed files from git.

    Returns:
        Full review as a Markdown string, or None if no files to review
    """
    if files is None:
        files = get_changed_files()

    if not files:
        print("No supported files changed.")
        return None

    print(f"Reviewing {len(files)} files...")

    all_reviews = ["# 🤖 Claude Code Review\n"]
    request_changes = False

    for file_path in files:
        if not os.path.exists(file_path):
            continue

        print(f"  Reviewing {file_path}...")
        diff = get_diff(file_path)
        content = get_file_content(file_path)

        if not diff and not content:
            continue

        try:
            review = review_file(file_path, diff, content)
        except ValueError as e:
            print(f"  ⚠️  Could not parse review for {file_path}: {e}")
            continue

        formatted = format_review(file_path, review)
        all_reviews.append(formatted)
        all_reviews.append("\n---\n")

        if review.get("overall_rating") == "Request Changes":
            request_changes = True

    if request_changes:
        all_reviews.append("\n> ⚠️ **Changes requested** — please address the issues above before merging.")
    else:
        all_reviews.append("\n> ✅ **Looks good** — no blocking issues found.")

    all_reviews.append(f"\n*Reviewed by Claude Sonnet · {len(files)} files*")

    final_comment = "\n".join(all_reviews)
    post_github_comment(final_comment)
    print("\nReview complete!")
    return final_comment


if __name__ == "__main__":
    file_args = sys.argv[1:] if len(sys.argv) > 1 else None
    result = run_review(file_args)
    if result:
        print(result)
