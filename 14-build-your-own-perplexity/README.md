# 🔍 Build Your Own Perplexity

AI-powered search with streaming answers and citations. Web search results + Claude = instant knowledge.

![Demo](https://img.shields.io/badge/difficulty-advanced-red?style=flat-square)

## Setup (2 free API keys)
```bash
pip install -r requirements.txt
streamlit run app.py
```

Get free keys:
- **Claude**: [console.anthropic.com](https://console.anthropic.com)
- **Brave Search**: [brave.com/search/api](https://brave.com/search/api) (2000 free searches/month)

## Features
- Streaming responses (text appears as Claude writes)
- Inline citations [1] [2] [3]
- Expandable source panel
- Conversation history

## Key concept: RAG with live web data
Instead of a static vector database, this RAG system fetches fresh web results at query time. The pattern: retrieve → format as context → generate with citations.

## Extend it
- Add DuckDuckGo as fallback search
- Cache results in Redis
- Add image search
- Deploy to Streamlit Cloud (free)
