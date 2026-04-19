"""
Build Your Own Perplexity
Web search + Claude = streaming AI answers with citations.
"""
from typing import Dict, List
import json
import os
from datetime import datetime

import anthropic
import requests
import streamlit as st

st.set_page_config(page_title="AI Search", page_icon="🔍", layout="wide")

with st.sidebar:
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
    )
    brave_key = st.text_input(
        "Brave Search API Key (optional — leave blank to use free DuckDuckGo)",
        type="password",
        value=os.getenv("BRAVE_API_KEY", ""),
    )
    st.markdown("""
**Keys needed:**
- [Anthropic](https://console.anthropic.com) — Claude (required)
- [Brave Search](https://brave.com/search/api/) — faster / 2,000 free searches/month (optional)
- No Brave key? DuckDuckGo is used automatically at no cost.
""")


def _duckduckgo_search(query: str, count: int = 5) -> List[Dict[str, str]]:
    """Free web search via DuckDuckGo — no API key required.

    Args:
        query: Search query string
        count: Number of results to return

    Returns:
        List of result dicts with 'title', 'url', and 'snippet' keys
    """
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            raw = list(ddgs.text(query, max_results=count))
        return [
            {
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
            }
            for r in raw
        ]
    except ImportError:
        return [
            {
                "title": "duckduckgo-search not installed",
                "url": "",
                "snippet": "Run: pip install duckduckgo-search",
            }
        ]
    except Exception as e:
        return [{"title": "DuckDuckGo search error", "url": "", "snippet": str(e)}]


def brave_search(query: str, brave_api_key: str, count: int = 5) -> List[Dict[str, str]]:
    """Search the web using Brave Search API, or DuckDuckGo when no key is provided.

    Args:
        query: Search query string
        brave_api_key: Brave Search API key (leave empty to use free DuckDuckGo)
        count: Number of results to return

    Returns:
        List of result dicts with 'title', 'url', and 'snippet' keys
    """
    if not brave_api_key:
        return _duckduckgo_search(query, count)
    try:
        r = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": brave_api_key,
            },
            params={"q": query, "count": count, "search_lang": "en"},
            timeout=10,
        )
        r.raise_for_status()
        results = r.json().get("web", {}).get("results", [])
        return [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("description", ""),
            }
            for item in results
        ]
    except requests.RequestException as e:
        return [{"title": "Search error", "url": "", "snippet": str(e)}]


def format_sources(results: List[Dict[str, str]]) -> str:
    """Format search results as a numbered source list for the prompt.

    Args:
        results: List of search result dicts

    Returns:
        Formatted string with numbered sources
    """
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']}\nURL: {r['url']}\n{r['snippet']}\n")
    return "\n".join(lines)


st.title("🔍 AI Search")
st.caption("Ask anything → get AI answers with web citations")

if "history" not in st.session_state:
    st.session_state.history: List[Dict[str, str]] = []

query = st.chat_input("Ask anything...")

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if query:
    if not api_key:
        st.error("Please enter your Anthropic API key in the sidebar")
        st.stop()

    st.session_state.history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.status(f"Searching the web for: {query}", expanded=True) as status:
            results = brave_search(query, brave_key)
            st.write(f"Found {len(results)} sources")
            status.update(label="Generating answer...", state="running")

        sources_text = format_sources(results)
        system = f"""You are a helpful AI assistant that answers questions based on web search results.
Today is {datetime.now().strftime('%B %d, %Y')}.

Web search results:
{sources_text}

Instructions:
- Answer the question thoroughly using the search results
- Cite sources using [1], [2], etc. inline
- If search results do not fully answer the question, say so
- Be accurate and helpful
- Format with markdown for readability"""

        placeholder = st.empty()
        full_response = ""

        claude_client = anthropic.Anthropic(api_key=api_key)
        with claude_client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=system,
            messages=[{"role": "user", "content": query}],
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

        with st.expander("📚 Sources"):
            for i, r in enumerate(results, 1):
                st.markdown(f"**[{i}] [{r['title']}]({r['url']})**")
                st.caption(r["snippet"])

    st.session_state.history.append({"role": "assistant", "content": full_response})
