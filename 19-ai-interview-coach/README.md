# 🎤 AI Interview Coach

Practice any interview type with Claude. Get scored, specific feedback on every answer.

![Demo](https://img.shields.io/badge/difficulty-advanced-red?style=flat-square)

## Setup
```bash
pip install -r requirements.txt
streamlit run coach.py
```

## Interview types
- **Technical** — Coding, algorithms, system concepts
- **Behavioral** — STAR format, leadership, conflict
- **System Design** — Architecture, scaling, trade-offs
- **Case Study** — Problem-solving, estimation
- **HR** — Salary, culture fit, motivation

## Scoring
Each answer gets: overall score (0-10), grade (A-F), strengths, improvements, and a sample strong answer to compare against.

## Key concept: Stateful AI coaching
The coach tracks questions already asked (no repeats), maintains your score history, and generates a final readiness report — demonstrating how to build stateful AI applications with Streamlit session state.

## ⚠️ Known Limitations
- **No live coding environment**: Technical questions are text-based; there is no integrated code editor or test runner for coding challenges
- **Training data cutoff**: Questions and sample answers are generated from Claude's training data; very recently introduced frameworks or APIs may not appear
- **Session state only**: Score history and question log reset on page refresh; there is no persistent storage across sessions
- **Single-user**: Designed for solo practice; no multi-user, leaderboard, or progress tracking across devices

## 🧪 Testing & Linting

```bash
# Install linter
pip install ruff

# Check for style and correctness issues
ruff check .

# Verify all dependencies install correctly
pip install -r requirements.txt

# Smoke test — confirm imports load without error
python -c "import anthropic, streamlit; print('All dependencies OK')"
```
