"""
PDF Chat with Claude
Upload any PDF and ask questions — Claude answers with exact page references.
"""
from typing import Dict, List, Tuple
import io
import os

import anthropic
import PyPDF2
import streamlit as st

st.set_page_config(page_title="PDF Chat with Claude", page_icon="📄", layout="wide")
st.title("📄 Chat with any PDF using Claude")
st.caption("Upload a PDF and ask questions — Claude will answer with page references")

with st.sidebar:
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-...",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
    )
    st.markdown("Get your key at [console.anthropic.com](https://console.anthropic.com)")
    uploaded = st.file_uploader("Upload PDF", type="pdf")
    if uploaded:
        st.success(f"Loaded: {uploaded.name}")


def extract_pdf_text(file: io.BytesIO) -> Tuple[str, int]:
    """Extract text from a PDF file, tagging each page.

    Args:
        file: PDF file as a Streamlit UploadedFile (file-like object)

    Returns:
        Tuple of (full_text_with_page_markers, page_count)
    """
    reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages.append(f"[Page {i + 1}]\n{text}")
    return "\n\n".join(pages), len(reader.pages)


def ask_claude(
    client: anthropic.Anthropic,
    pdf_text: str,
    question: str,
    history: List[Dict[str, str]],
) -> str:
    """Send a question about the PDF to Claude and return the response.

    Args:
        client: Anthropic API client
        pdf_text: Extracted PDF content with page markers
        question: User's question
        history: Previous messages in format [{"role": "...", "content": "..."}]

    Returns:
        Claude's response text
    """
    system = f"""You are a helpful assistant that answers questions about a PDF document.

Here is the PDF content with page numbers:
<document>
{pdf_text[:80000]}
</document>

When answering:
- Always cite the page number (e.g., "According to page 3...")
- Be concise but complete
- If the answer is not in the document, say so clearly"""

    messages = history + [{"role": "user", "content": question}]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system,
        messages=messages,
    )
    return response.content[0].text


# Session state initialisation
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "pdf_pages" not in st.session_state:
    st.session_state.pdf_pages = 0

# Load PDF when a new file is uploaded
if uploaded and uploaded != st.session_state.get("last_file"):
    with st.spinner("Reading PDF..."):
        st.session_state.pdf_text, st.session_state.pdf_pages = extract_pdf_text(uploaded)
        st.session_state.last_file = uploaded
        st.session_state.messages = []
    st.success(f"Ready! {st.session_state.pdf_pages} pages loaded.")

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask anything about your PDF..."):
    if not api_key:
        st.error("Please enter your API key in the sidebar")
        st.stop()
    if not st.session_state.pdf_text:
        st.error("Please upload a PDF first")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            api_client = anthropic.Anthropic(api_key=api_key)
            history = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[:-1]
            ]
            response = ask_claude(api_client, st.session_state.pdf_text, prompt, history)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
