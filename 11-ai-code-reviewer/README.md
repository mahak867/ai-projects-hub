# 🔍 AI Code Reviewer

GitHub Action that automatically reviews every PR with Claude. Gets added to any repo in 2 minutes.

![Demo](https://img.shields.io/badge/difficulty-intermediate-orange?style=flat-square)

## Setup (2 steps)

### 1. Add GitHub secret
Go to your repo → Settings → Secrets → Actions → New repository secret:
- Name: `ANTHROPIC_API_KEY`
- Value: your Claude API key

### 2. Add the workflow
```bash
mkdir -p .github/workflows
cp ai-review.yml .github/workflows/
git add .github/workflows/ai-review.yml
git commit -m "Add AI code review"
git push
```

That's it. Every PR now gets automatically reviewed.

## What the review includes
- **Overall rating** — Approve / Request Changes / Needs Discussion
- **Issues with severity** — Critical / High / Medium / Low
- **Security concerns** — SQL injection, hardcoded secrets, etc.
- **What's good** — positive reinforcement
- **Suggestions** — improvements without blocking

## Run locally
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

# Review specific files
python review.py src/main.py utils/helpers.py

# Review all changed files in latest commit
python review.py
```

## Key concept: GitHub Actions + AI
Combining GitHub's event system with Claude creates always-on AI assistance that runs exactly when needed — no babysitting required.
