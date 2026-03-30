# 🎙️ Voice Journal AI

Record your day → Claude extracts mood, wins, todos, and insights → builds your personal growth timeline.

![Demo](https://img.shields.io/badge/difficulty-intermediate-orange?style=flat-square)

## Setup
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage
```bash
# Type your entry
python journal.py

# Analyze an audio file
python journal.py recording.mp3

# Run a demo
python journal.py demo

# See 30-day trends
python journal.py trends
```

## What you get per entry
- Mood score (1-10) and label
- Key events, wins, challenges
- Auto-extracted TODOs
- Themes and patterns
- Claude's reflection on your growth
- Intention for tomorrow

## Key concept: Structured extraction
By defining a strict JSON schema in the prompt, Claude reliably extracts structured data from unstructured voice/text. This pattern works for any extraction task.
