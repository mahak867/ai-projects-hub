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

## ⚠️ Known Limitations
- **Text-based PDFs only**: PyMuPDF cannot extract text from scanned (image-based) PDFs — OCR pre-processing is required for those
- **Large documents**: PDFs longer than ~150 pages are chunked; very long documents may produce incomplete extraction for fields that appear late in the file
- **Schema accuracy**: Extraction quality depends heavily on the JSON schema definition in the prompt; poorly defined schemas yield inconsistent results
- **Table extraction**: Complex multi-column financial tables may be extracted with incorrect cell alignment

## 🧪 Testing & Linting

```bash
# Install linter
pip install ruff

# Check for style and correctness issues
ruff check .

# Verify all dependencies install correctly
pip install -r requirements.txt

# Smoke test — confirm imports load without error
python -c "import anthropic, fitz; print('All dependencies OK')"
```
