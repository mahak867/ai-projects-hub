"""
AI Code Reviewer — runs Claude on changed files in a PR
Can be used standalone or as part of a GitHub Action
"""
import anthropic
import subprocess
import os
import sys
import json
import requests
from pathlib import Path

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

SUPPORTED_EXTENSIONS = {'.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.java', '.rs', '.cpp', '.c', '.cs'}

def get_changed_files() -> list[str]:
    """Get files changed in the current PR/commit"""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True, text=True
    )
    files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
    return [f for f in files if Path(f).suffix in SUPPORTED_EXTENSIONS]

def get_diff(file_path: str) -> str:
    """Get the git diff for a specific file"""
    result = subprocess.run(
        ["git", "diff", "HEAD~1", "HEAD", "--", file_path],
        capture_output=True, text=True
    )
    return result.stdout[:6000]  # Limit size

def get_file_content(file_path: str) -> str:
    """Get current file content"""
    try:
        with open(file_path) as f:
            return f.read()[:8000]
    except FileNotFoundError:
        return ""

def review_file(file_path: str, diff: str, content: str) -> dict:
    """Get Claude's review of a file"""
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
      "issue": "<what's wrong>",
      "fix": "<how to fix it>"
    }}
  ],
  "positives": ["<good thing 1>", "<good thing 2>"],
  "security_concerns": ["<concern>"] or [],
  "performance_notes": ["<note>"] or [],
  "suggestions": ["<improvement>"]
}}

Return ONLY valid JSON."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())

def post_github_comment(comment: str):
    """Post review comment to GitHub PR"""
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    pr_number = os.environ.get("PR_NUMBER", "")
    
    if not all([token, repo, pr_number]):
        print("[GitHub] Missing env vars, printing instead:")
        print(comment)
        return
    
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    requests.post(url, json={"body": comment}, headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"})

def format_review(file_path: str, review: dict) -> str:
    """Format review as markdown"""
    rating = review.get("overall_rating", "")
    emoji = {"Approve": "✅", "Request Changes": "🔴", "Needs Discussion": "🟡"}.get(rating, "⚪")
    
    md = [f"## {emoji} `{file_path}` — {rating}", f"\n{review.get('summary', '')}\n"]
    
    if review.get("issues"):
        md.append("### Issues Found")
        for issue in review["issues"]:
            severity_emoji = {"Critical": "🚨", "High": "⚠️", "Medium": "📝", "Low": "💡"}.get(issue["severity"], "📝")
            md.append(f"\n**{severity_emoji} {issue['severity']}** — `{issue.get('line_hint', '')}`")
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

def run_review(files: list[str] = None):
    """Main review runner"""
    if files is None:
        files = get_changed_files()
    
    if not files:
        print("No supported files changed.")
        return
    
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
        
        review = review_file(file_path, diff, content)
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
    files = sys.argv[1:] if len(sys.argv) > 1 else None
    result = run_review(files)
    if result:
        print(result)
