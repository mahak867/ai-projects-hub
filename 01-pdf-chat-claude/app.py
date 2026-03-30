import streamlit as st
import anthropic
import PyPDF2
import io

st.set_page_config(page_title="PDF Chat with Claude", page_icon="📄", layout="wide")

st.title("📄 Chat with any PDF using Claude")
st.caption("Upload a PDF and ask questions — Claude will answer with page references")

with st.sidebar:
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    st.markdown("Get your key at [console.anthropic.com](https://console.anthropic.com)")
    uploaded = st.file_uploader("Upload PDF", type="pdf")
    if uploaded:
        st.success(f"Loaded: {uploaded.name}")

def extract_pdf_text(file) -> tuple[str, int]:
    reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text.strip():
            pages.append(f"[Page {i+1}]\n{text}")
    return "\n\n".join(pages), len(reader.pages)

def ask_claude(client, pdf_text: str, question: str, history: list) -> str:
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
        messages=messages
    )
    return response.content[0].text

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "pdf_pages" not in st.session_state:
    st.session_state.pdf_pages = 0

if uploaded and uploaded != st.session_state.get("last_file"):
    with st.spinner("Reading PDF..."):
        st.session_state.pdf_text, st.session_state.pdf_pages = extract_pdf_text(uploaded)
        st.session_state.last_file = uploaded
        st.session_state.messages = []
    st.success(f"Ready! {st.session_state.pdf_pages} pages loaded.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

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
            client = anthropic.Anthropic(api_key=api_key)
            history = [{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages[:-1]]
            response = ask_claude(client, st.session_state.pdf_text, prompt, history)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
