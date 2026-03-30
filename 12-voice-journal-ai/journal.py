"""
Voice Journal AI
Record voice -> transcribe with Whisper -> extract insights with Claude -> save to file
"""
import anthropic
import json
import os
import sys
import datetime
from pathlib import Path

client = anthropic.Anthropic()
JOURNAL_FILE = Path("journal.json")

def transcribe(audio_path: str) -> str:
    """Transcribe audio using OpenAI Whisper (local)"""
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"]
    except ImportError:
        print("whisper not installed. Using sample text for demo.")
        return "Today was a productive day. I finished the quarterly report and had a great call with the team. Feeling a bit stressed about the deadline next week. Need to exercise more and eat better. Planning to read for 30 minutes before bed."

def extract_insights(transcript: str, date: str) -> dict:
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
    return json.loads(raw.strip())

def save_entry(entry: dict):
    entries = []
    if JOURNAL_FILE.exists():
        with open(JOURNAL_FILE) as f:
            entries = json.load(f)
    entries.append(entry)
    with open(JOURNAL_FILE, "w") as f:
        json.dump(entries, f, indent=2)

def show_trends():
    if not JOURNAL_FILE.exists():
        print("No journal entries yet.")
        return
    with open(JOURNAL_FILE) as f:
        entries = json.load(f)
    if not entries:
        return

    prompt = f"""Analyze these journal entries and identify trends, patterns, and growth:

{json.dumps([{"date": e["date"], "mood": e["insights"]["mood"], "mood_score": e["insights"]["mood_score"], "themes": e["insights"]["themes"], "wins": e["insights"]["wins"]} for e in entries[-30:]], indent=2)}

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

def record_and_analyze(audio_path: str = None, text: str = None):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    if text:
        transcript = text
    elif audio_path:
        print(f"Transcribing {audio_path}...")
        transcript = transcribe(audio_path)
        print(f"Transcript: {transcript[:100]}...")
    else:
        print("Enter your journal entry (press Enter twice when done):")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        transcript = "\n".join(lines[:-1])

    print("Extracting insights...")
    insights = extract_insights(transcript, date)

    entry = {"date": date, "transcript": transcript, "insights": insights}
    save_entry(entry)

    print(f"\n📔 Journal Entry — {date}")
    print(f"Mood: {insights['mood']} ({insights['mood_score']}/10)")
    print(f"Summary: {insights['summary']}")
    if insights.get("wins"):
        print(f"Wins: {', '.join(insights['wins'])}")
    if insights.get("todos"):
        print(f"TODOs: {', '.join(insights['todos'])}")
    print(f"Reflection: {insights['reflection']}")
    print(f"Tomorrow: {insights['tomorrow_intention']}")
    print(f"\nSaved to {JOURNAL_FILE}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "trends":
            show_trends()
        elif sys.argv[1] == "demo":
            record_and_analyze(text="Had a tough morning but pushed through. Finished the AI project I've been working on for weeks. Feeling proud but exhausted. Need to call mom this weekend. Want to start running again.")
        elif os.path.exists(sys.argv[1]):
            record_and_analyze(audio_path=sys.argv[1])
    else:
        record_and_analyze()
