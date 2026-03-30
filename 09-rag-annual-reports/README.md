# 📑 RAG over NSE Annual Reports

Ask questions across multiple company annual reports. Claude finds relevant sections and answers with citations.

![Demo](https://img.shields.io/badge/difficulty-intermediate-orange?style=flat-square)

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
# 1. Ingest annual reports (download PDFs from NSE website first)
python rag.py ingest TCS_AR_2024.pdf TCS 2024
python rag.py ingest INFY_AR_2024.pdf Infosys 2024

# 2. Ask questions
python rag.py query "What was the revenue growth for TCS?"
python rag.py query "Compare employee headcount between TCS and Infosys" 
python rag.py query "What are the key risks mentioned?" --year 2024
python rag.py query "Dividend history and policy" --company TCS
```

## Where to get annual reports
- NSE: [nseindia.com](https://nseindia.com) → Company Filings
- BSE: [bseindia.com](https://bseindia.com) → Annual Reports
- Company investor relations pages

## Key concept: RAG (Retrieval Augmented Generation)
PDFs are chunked into ~800 word segments, embedded into vectors, stored in ChromaDB. At query time, the most similar chunks are retrieved and passed to Claude as context. This lets you search across thousands of pages instantly.

## Production upgrade
Replace the simple embedding with Voyage AI embeddings (recommended by Anthropic) for dramatically better retrieval accuracy:
```python
import voyageai
vo = voyageai.Client(api_key="...")
embeddings = vo.embed(texts, model="voyage-finance-2").embeddings
```
