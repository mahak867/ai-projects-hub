# 📑 Document Intelligence

Extract structured data from PDFs and compare multiple documents with Claude.

![Demo](https://img.shields.io/badge/difficulty-advanced-red?style=flat-square)

## Setup
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage
```bash
# Extract from one document
python extractor.py extract TCS_AR_2024.pdf --type annual_report
python extractor.py extract contract.pdf --type contract --output result.json

# Compare multiple documents (e.g., 3 years of annual reports)
python extractor.py compare TCS_2022.pdf TCS_2023.pdf TCS_2024.pdf --type annual_report
python extractor.py compare q1.pdf q2.pdf q3.pdf q4.pdf --focus "revenue trends and margin changes"
```

## Document types
- `annual_report` — Revenue, profit, EPS, risks, highlights
- `contract` — Parties, value, obligations, termination
- `research_paper` — Methodology, findings, limitations
- `invoice` — Line items, totals, terms

## Key concept: Schema-guided extraction
By giving Claude a JSON schema, it reliably extracts the exact fields you need — turning unstructured PDFs into structured databases.
