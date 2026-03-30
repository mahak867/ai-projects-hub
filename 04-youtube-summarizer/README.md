# 📺 YouTube Summarizer with Claude

Paste any YouTube URL, get a structured summary with key points, quotes, and action items.

![Demo](https://img.shields.io/badge/difficulty-beginner-green?style=flat-square)

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
# Full comprehensive summary
python summarize.py "https://youtube.com/watch?v=..."

# Quick TL;DR + bullet points
python summarize.py "https://youtube.com/watch?v=..." --style brief

# Study notes format
python summarize.py "https://youtube.com/watch?v=..." --style notes

# Save to file
python summarize.py "https://youtube.com/watch?v=..." --output summary.json
```

## How it works
1. `yt-dlp` downloads auto-generated subtitles as VTT
2. VTT format is cleaned to plain text
3. Claude summarizes based on the requested style
4. Output is structured and ready to use

## Limitations
- Requires videos with English subtitles (auto-generated OK)
- Very long videos (3hr+) are truncated to ~60k chars
- Private/age-restricted videos won't work

## Extend it
- Add a Streamlit UI
- Batch summarize a playlist
- Generate flashcards from educational videos
- Translate summaries to other languages
