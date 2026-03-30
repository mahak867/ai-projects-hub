# 📋 AI Resume Analyzer

Upload your resume + paste a job description → get a match score, gap analysis, and improvement suggestions.

![Demo](https://img.shields.io/badge/difficulty-beginner-green?style=flat-square)

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What you get
- **Match score** 0-100 with level (Poor/Fair/Good/Excellent)
- **Matching skills** — what you already have that they want
- **Missing skills** — what to learn or emphasize
- **Resume improvements** — section-by-section suggestions
- **Cover letter points** — what to highlight
- **Interview prep topics** — what they'll likely ask

## How it works
Claude parses both documents and returns structured JSON with the full analysis. The JSON schema is defined in the prompt to ensure consistent output every time.

## Key concept: Structured output
By asking Claude to return JSON with a specific schema and parsing it in Python, you get reliable, machine-readable AI output — the foundation of production AI systems.
