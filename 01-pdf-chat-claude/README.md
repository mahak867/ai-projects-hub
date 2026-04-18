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

## ⚠️ Known Limitations
- **Context window**: PDFs longer than ~150,000 words are truncated before being sent to Claude
- **Text only**: Images, tables, and charts inside PDFs are not extracted — text layer only
- **No persistence**: Conversation resets on page refresh; there is no session storage
- **Scanned PDFs**: PyPDF2 cannot extract text from image-based (scanned) PDFs — use a PDF with a text layer

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
