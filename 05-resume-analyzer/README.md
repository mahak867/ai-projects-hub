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

## ⚠️ Known Limitations
- **Language**: Works best with English-language resumes and job descriptions; other languages may produce lower-quality analysis
- **Niche roles**: Very specialized technical roles (e.g., RF hardware engineer, semiconductor process) may yield less accurate skill gap assessments
- **ATS scoring**: The match score reflects Claude's analysis, not any specific ATS algorithm; actual recruiter tools may score differently
- **No file persistence**: Analysis results are not saved between sessions; export manually if needed

## 🧪 Testing & Linting

```bash
# Install linter
pip install ruff

# Check for style and correctness issues
ruff check .

# Verify all dependencies install correctly
pip install -r requirements.txt

# Smoke test — confirm imports load without error
python -c "import anthropic, streamlit, PyPDF2; print('All dependencies OK')"
```
