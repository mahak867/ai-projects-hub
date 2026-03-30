# 📊 Agentic Data Analyst

Upload any CSV → Claude writes analysis code → executes it → explains results in plain English.

![Demo](https://img.shields.io/badge/difficulty-advanced-red?style=flat-square)

## Setup
```bash
pip install -r requirements.txt
streamlit run analyst.py
```

## Works with any CSV
- Sales data → revenue trends, top products
- Customer data → segmentation, churn patterns
- Financial data → P&L analysis, anomalies
- Survey data → sentiment patterns

## Key concept: Code generation + execution
Claude generates pandas code tailored to your specific dataset, executes it in a sandbox, then interprets the results. This "code-as-tool" pattern is how production AI agents work.
