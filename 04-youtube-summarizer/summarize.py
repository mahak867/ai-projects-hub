"""
YouTube Summarizer
Paste a YouTube URL -> structured notes with key points, quotes, and action items.
"""
from typing import Dict
import argparse
import glob
import json
import os
import re
import subprocess
import sys

import anthropic

# Validate API key at startup
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
    print("Get your key at: https://console.anthropic.com")
    sys.exit(1)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def get_transcript(url: str) -> tuple[str, str]:
    """Download transcript using yt-dlp.

    Args:
        url: YouTube video URL

    Returns:
        Tuple of (video_title, transcript_text)

    Raises:
        FileNotFoundError: If yt-dlp is not installed or no transcript is available
        subprocess.CalledProcessError: If yt-dlp fails
    """
    print(f"Fetching transcript for: {url}")

    result = subprocess.run(
        [
            "yt-dlp", "--skip-download",
            "--write-auto-subs", "--sub-lang", "en",
            "--sub-format", "vtt",
            "--output", "/tmp/yt_%(id)s",
            "--print", "title",
            url,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"yt-dlp failed: {result.stderr.strip()}\n"
            "Make sure yt-dlp is installed: pip install yt-dlp"
        )

    title = result.stdout.strip()

    vtt_files = glob.glob("/tmp/yt_*.vtt")
    if not vtt_files:
        raise FileNotFoundError(
            "No transcript found. The video may not have subtitles.\n"
            "Try a video that has auto-generated captions enabled."
        )

    with open(vtt_files[0], "r") as f:
        vtt_content = f.read()

    # Parse VTT to plain text, deduplicate consecutive lines
    lines = vtt_content.split("\n")
    text_lines: list[str] = []
    for line in lines:
        line = line.strip()
        if (
            line
            and not line.startswith("WEBVTT")
            and not re.match(r"^\d+:\d+", line)
            and not re.match(r"^\d+$", line)
            and not line.startswith("NOTE")
            and (not text_lines or line != text_lines[-1])
        ):
            clean = re.sub(r"<[^>]+>", "", line)
            if clean:
                text_lines.append(clean)

    # Cleanup temp files
    for f in vtt_files:
        os.remove(f)

    return title, " ".join(text_lines)


def summarize(url: str, style: str = "comprehensive") -> Dict[str, object]:
    """Summarize a YouTube video.

    Args:
        url: YouTube video URL
        style: One of 'comprehensive', 'brief', or 'notes'

    Returns:
        Dictionary with title, url, style, summary, and transcript_length
    """
    title, transcript = get_transcript(url)
    print(f"Video: {title}")
    print(f"Transcript length: {len(transcript)} chars")

    prompts: Dict[str, str] = {
        "comprehensive": f"""Summarize this YouTube video transcript.

Title: {title}

Transcript:
{transcript[:60000]}

Provide:
1. **TL;DR** (2-3 sentences max)
2. **Key Points** (bullet list of 5-8 main takeaways)
3. **Detailed Summary** (3-5 paragraphs covering the full content)
4. **Memorable Quotes** (2-3 best quotes)
5. **Action Items** (what the viewer should do based on this video)
6. **Who should watch this** (target audience)""",

        "brief": f"""Give me a very brief summary of this YouTube video.
Title: {title}
Transcript: {transcript[:40000]}

Format: TL;DR (2 sentences) + 5 bullet point takeaways""",

        "notes": f"""Convert this YouTube video into structured study notes.
Title: {title}
Transcript: {transcript[:60000]}

Create organized notes with headers, subheadings, and key concepts.""",
    }

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompts[style]}],
    )

    return {
        "title": title,
        "url": url,
        "style": style,
        "summary": response.content[0].text,
        "transcript_length": len(transcript),
    }


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Summarize any YouTube video with Claude")
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument(
        "--style",
        choices=["comprehensive", "brief", "notes"],
        default="comprehensive",
        help="Summary style",
    )
    parser.add_argument("--output", help="Save result to JSON file")
    args = parser.parse_args()

    result = summarize(args.url, args.style)

    print("\n" + "=" * 60)
    print(f"📺 {result['title']}")
    print("=" * 60)
    print(result["summary"])

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Saved to {args.output}")


if __name__ == "__main__":
    main()
