"""
Voice Journal AI
Record voice -> transcribe with Whisper -> extract insights with Claude -> save to file
"""
from typing import Dict, List, Optional
from pathlib import Path
import anthropic
import json
import os
import sys
import datetime

# Configuration
JOURNAL_FILE = Path("journal.json")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
    print("Get your key at: https://console.anthropic.com")
    print("Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
    sys.exit(1)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def transcribe(audio_path: str, demo_mode: bool = False) -> str:
    """Transcribe audio using OpenAI Whisper.

    Args:
        audio_path: Path to audio file (mp3, wav, m4a, etc.)
        demo_mode: If True, skip transcription and use sample text

    Returns:
        Transcribed text

    Raises:
        ImportError: If whisper package is not installed and demo_mode is False
        FileNotFoundError: If audio file does not exist
    """
    if demo_mode:
        print("⚠️  DEMO MODE: Using sample transcript (pass a real audio file to transcribe)")
        return (
            "Today was a productive day. I finished the quarterly report and "
            "had a great call with the team. Feeling a bit stressed about the "
            "deadline next week. Need to exercise more and eat better. "
            "Planning to read for 30 minutes before bed."
        )

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        import whisper
    except ImportError as e:
        raise ImportError(
            "OpenAI Whisper is not installed.\n"
            "Install it with: pip install openai-whisper\n"
            "Or run in demo mode: python journal.py demo"
        ) from e

    print("Loading Whisper model...")
    model = whisper.load_model("base")

    print(f"Transcribing {audio_path}...")
    result = model.transcribe(audio_path)
    return result["text"]


def extract_insights(transcript: str, date: str) -> Dict[str, object]:
    """Extract structured insights from a journal transcript using Claude.

    Args:
        transcript: Journal entry text
        date: Entry date in format "YYYY-MM-DD HH:MM"

    Returns:
        Dictionary with keys: summary, mood, mood_score, key_events, wins,
        challenges, todos, themes, reflection, tomorrow_intention

    Raises:
        ValueError: If the transcript is empty or Claude returns invalid JSON
    """
    if not transcript.strip():
        raise ValueError("Transcript cannot be empty")

    prompt = f"""Analyze this journal entry from {date} and extract structured insights.

JOURNAL ENTRY:
{transcript}

Return JSON with exactly these keys:
{{
  "summary": "<2-3 sentence summary>",
  "mood": "<Happy/Neutral/Stressed/Anxious/Excited/Tired/Grateful>",
  "mood_score": <1-10 where 10 is best>,
  "key_events": ["event1", "event2"],
  "wins": ["win1", "win2"],
  "challenges": ["challenge1"],
  "todos": ["todo1", "todo2"],
  "themes": ["theme1", "theme2"],
  "reflection": "<one insightful observation about patterns or growth>",
  "tomorrow_intention": "<one thing to focus on tomorrow>"
}}

Return ONLY valid JSON."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
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


def save_entry(entry: Dict[str, object]) -> None:
    """Save a journal entry to the JSON file and optionally sync to S3.

    Args:
        entry: Dictionary containing date, transcript, and insights
    """
    entries: List[Dict] = []

    if JOURNAL_FILE.exists():
        with open(JOURNAL_FILE, "r") as f:
            entries = json.load(f)

    entries.append(entry)

    with open(JOURNAL_FILE, "w") as f:
        json.dump(entries, f, indent=2)

    _sync_to_s3(JOURNAL_FILE)


def _sync_to_s3(local_file: Path) -> None:
    """Optionally upload the journal JSON to S3 for cross-device access.

    Reads JOURNAL_S3_BUCKET (and optionally JOURNAL_S3_KEY) from env.
    Does nothing if JOURNAL_S3_BUCKET is not set.
    """
    bucket = os.getenv("JOURNAL_S3_BUCKET")
    if not bucket:
        return

    s3_key = os.getenv("JOURNAL_S3_KEY", local_file.name)
    try:
        import boto3  # type: ignore[import]
        boto3.client("s3").upload_file(str(local_file), bucket, s3_key)
        print(f"☁️  Synced to s3://{bucket}/{s3_key}")
    except ImportError:
        print("⚠️  S3 sync skipped — install boto3: pip install boto3")
    except Exception as e:
        print(f"⚠️  S3 sync failed: {e}")


def show_trends() -> None:
    """Analyze and display trends across all journal entries."""
    if not JOURNAL_FILE.exists():
        print("📔 No journal entries yet. Start by recording your first entry!")
        return

    with open(JOURNAL_FILE, "r") as f:
        entries = json.load(f)

    if not entries:
        print("📔 No journal entries yet.")
        return

    recent_entries = entries[-30:]
    summary_data = [
        {
            "date": e["date"],
            "mood": e["insights"]["mood"],
            "mood_score": e["insights"]["mood_score"],
            "themes": e["insights"]["themes"],
            "wins": e["insights"]["wins"],
        }
        for e in recent_entries
    ]

    prompt = f"""Analyze these journal entries and identify trends, patterns, and growth:

{json.dumps(summary_data, indent=2)}

Provide:
1. Mood trends over time
2. Recurring themes
3. Growth patterns
4. Recommendations for improvement
5. Things to celebrate

Be warm, insightful, and specific."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    print("\n📊 Journal Trends:\n")
    print(response.content[0].text)


def record_and_analyze(
    audio_path: Optional[str] = None,
    text: Optional[str] = None,
    demo_mode: bool = False,
) -> None:
    """Record and analyze a journal entry.

    Args:
        audio_path: Path to audio file to transcribe
        text: Direct text entry (skips transcription)
        demo_mode: Use sample text instead of real transcription
    """
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    if text:
        transcript = text
    elif audio_path:
        transcript = transcribe(audio_path, demo_mode=demo_mode)
        if not demo_mode:
            print(f"✓ Transcript: {transcript[:100]}...")
    else:
        print("📝 Enter your journal entry (press Enter twice when done):")
        lines: List[str] = []
        empty_count = 0

        while True:
            line = input()
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
            lines.append(line)

        transcript = "\n".join(lines).strip()

        if not transcript:
            print("❌ No entry text provided. Exiting.")
            return

    print("🤔 Extracting insights...")
    try:
        insights = extract_insights(transcript, date)
    except ValueError as e:
        print(f"❌ Error extracting insights: {e}")
        return

    entry = {"date": date, "transcript": transcript, "insights": insights}
    save_entry(entry)

    print(f"\n📔 Journal Entry — {date}")
    print(f"Mood: {insights['mood']} ({insights['mood_score']}/10)")
    print(f"Summary: {insights['summary']}")

    if insights.get("wins"):
        print(f"✨ Wins: {', '.join(insights['wins'])}")

    if insights.get("todos"):
        print(f"📋 TODOs: {', '.join(insights['todos'])}")

    print(f"💭 Reflection: {insights['reflection']}")
    print(f"🌅 Tomorrow: {insights['tomorrow_intention']}")
    print(f"\n✓ Saved to {JOURNAL_FILE}")


def main() -> None:
    """Main entry point."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "trends":
            show_trends()

        elif command == "demo":
            record_and_analyze(demo_mode=True)

        elif command in ("help", "-h", "--help"):
            print("""
Voice Journal AI - Usage:

  python journal.py              # Manual text entry
  python journal.py demo         # Run with sample text
  python journal.py trends       # View trend analysis
  python journal.py <audio.mp3>  # Transcribe audio file
  python journal.py help         # Show this help

Requirements:
  - ANTHROPIC_API_KEY environment variable
  - For audio: pip install openai-whisper
            """)

        elif os.path.exists(sys.argv[1]):
            record_and_analyze(audio_path=sys.argv[1])

        else:
            print(f"❌ Unknown command or file not found: {sys.argv[1]}")
            print("Run 'python journal.py help' for usage")
            sys.exit(1)
    else:
        record_and_analyze()


if __name__ == "__main__":
    main()
