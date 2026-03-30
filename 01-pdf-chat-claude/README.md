# 📄 PDF Chat with Claude

Chat with any PDF using Claude. Upload a document, ask questions, get answers with page citations.

![Demo](https://img.shields.io/badge/difficulty-beginner-green?style=flat-square)

## What you'll build
A Streamlit app where you upload any PDF and have a conversation with it. Claude reads the entire document and answers with specific page references.

## Setup (3 steps)

```bash
pip install -r requirements.txt
streamlit run app.py
# Open http://localhost:8501, paste your Claude API key, upload a PDF
```

## How it works

1. PyPDF2 extracts text from each page, labeled `[Page N]`
2. Full document is passed to Claude as system context
3. Multi-turn conversation maintained in session state
4. Claude cites page numbers in every answer

## Example questions to try
- "What are the main conclusions of this document?"
- "Summarize page 5"
- "What does it say about [topic]?"
- "List all dates mentioned in the document"

## Extend it
- Add support for multiple PDFs
- Export conversation to markdown
- Add semantic search with embeddings for very large PDFs
