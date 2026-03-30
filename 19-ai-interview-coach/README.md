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
