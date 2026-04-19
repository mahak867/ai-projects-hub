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

## ⚠️ Known Limitations
- **Voice transcription**: Audio input requires OpenAI Whisper (separate API key); without it only text entry is supported
- **English only**: Voice transcription and mood analysis are optimized for English; other languages will produce lower quality results
- **Local storage only**: Journal entries are saved as JSON on disk with no encryption — do not store sensitive personal data without adding encryption
- **No cross-device sync**: Journal data lives on your local machine; cloud sync requires additional setup

## 🧪 Testing & Linting

```bash
# Install linter
pip install ruff

# Check for style and correctness issues
ruff check .

# Verify all dependencies install correctly
pip install -r requirements.txt

# Smoke test — confirm imports load without error
python -c "import anthropic; print('All dependencies OK')"

# Run the built-in demo (no API key needed for import check)
python journal.py demo
```
