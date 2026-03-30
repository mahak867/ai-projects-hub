"""
Build Your Own Perplexity
Web search + Claude = streaming AI answers with citations
"""
import anthropic
import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="AI Search", page_icon="🔍", layout="wide")

client = anthropic.Anthropic(api_key=st.sidebar.text_input("Anthropic API Key", type="password"))
brave_key = st.sidebar.text_input("Brave Search API Key (free at brave.com/search/api)", type="password")

st.sidebar.markdown("""
**Free API keys needed:**
- [Anthropic](https://console.anthropic.com) — Claude
- [Brave Search](https://brave.com/search/api/) — Web results (2000 free/month)
""")

def brave_search(query: str, count: int = 5) -> list[dict]:
    if not brave_key:
        return [{"title": "Demo result", "url": "https://example.com", "snippet": f"Demo snippet for: {query}. Add a Brave API key for real results."}]
    try:
        r = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers={"Accept": "application/json", "Accept-Encoding": "gzip", "X-Subscription-Token": brave_key},
            params={"q": query, "count": count, "search_lang": "en"}
        )
        results = r.json().get("web", {}).get("results", [])
        return [{"title": r.get("title", ""), "url": r.get("url", ""), "snippet": r.get("description", "")} for r in results]
    except Exception as e:
        return [{"title": "Search error", "url": "", "snippet": str(e)}]

def format_sources(results: list[dict]) -> str:
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']}\nURL: {r['url']}\n{r['snippet']}\n")
    return "\n".join(lines)

st.title("🔍 AI Search")
st.caption("Ask anything → get AI answers with web citations")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.chat_input("Ask anything...")

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if query:
    st.session_state.history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.status(f"Searching the web for: {query}", expanded=True) as status:
            results = brave_search(query)
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
- If search results don't fully answer the question, say so
- Be accurate and helpful
- Format with markdown for readability"""

        placeholder = st.empty()
        full_response = ""

        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=system,
            messages=[{"role": "user", "content": query}]
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
