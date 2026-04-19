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

## ⚠️ Known Limitations
- **Library sandbox**: The execution sandbox supports a fixed set of libraries (pandas, numpy, matplotlib); code requiring other packages will fail
- **Large CSVs**: Files with more than ~100,000 rows may hit the context window limit when Claude inspects the data schema
- **Non-standard formats**: Assumes well-formed CSV with a header row; TSV, Excel, or malformed files require pre-processing
- **Generated code quality**: Occasionally Claude generates code with edge-case bugs (e.g., wrong column names); re-running usually fixes it

## 🧪 Testing & Linting

```bash
# Install linter
pip install ruff

# Check for style and correctness issues
ruff check .

# Verify all dependencies install correctly
pip install -r requirements.txt

# Smoke test — confirm imports load without error
python -c "import anthropic, streamlit, pandas; print('All dependencies OK')"
```
