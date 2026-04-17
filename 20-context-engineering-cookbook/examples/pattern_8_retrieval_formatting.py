"""
Pattern 8: Retrieval Context Formatting
How you format retrieved chunks before passing to Claude dramatically affects answer quality.
This pattern shows the difference between naive and optimized retrieval formatting.
"""
import os, sys
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not set"); sys.exit(1)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def format_chunks_naive(chunks: list[dict]) -> str:
    """Bad: dumps raw chunks with no structure."""
    return "\n".join(c["text"] for c in chunks)


def format_chunks_optimized(chunks: list[dict]) -> str:
    """Good: structured with source metadata, relevance scores, clear separators."""
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(
            f"[SOURCE {i}]\n"
            f"Company: {chunk['company']} | Year: {chunk['year']} | "
            f"Page: {chunk['page']} | Relevance: {chunk['score']:.0%}\n"
            f"{chunk['text']}\n"
        )
    return "\n---\n".join(parts)


def answer_with_rag(question: str, chunks: list[dict], use_optimized: bool = True) -> str:
    """Answer a RAG question with naive vs optimized chunk formatting.

    Args:
        question: User question
        chunks: Retrieved document chunks with metadata
        use_optimized: If True, uses structured formatting; else naive

    Returns:
        Claude's answer
    """
    context = format_chunks_optimized(chunks) if use_optimized else format_chunks_naive(chunks)
    label = "OPTIMIZED" if use_optimized else "NAIVE"

    prompt = f"""Answer based ONLY on the provided document excerpts.
If the answer is not in the excerpts, say "Not found in provided documents."
Always cite the source number (e.g., [SOURCE 1]).

EXCERPTS ({label} FORMAT):
{context}

QUESTION: {question}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def main():
    # Simulated RAG chunks (in real use, these come from ChromaDB/FAISS)
    chunks = [
        {"company": "TCS", "year": "2024", "page": 42, "score": 0.94,
         "text": "Revenue for FY2024 stood at ₹2,40,893 crore, a growth of 8.2% year-over-year. "
                 "Net profit margin improved to 19.1% from 18.3% in FY2023."},
        {"company": "TCS", "year": "2023", "page": 38, "score": 0.87,
         "text": "FY2023 revenue was ₹2,22,634 crore with headcount reaching 6,14,795 employees globally."},
        {"company": "Infosys", "year": "2024", "page": 55, "score": 0.81,
         "text": "Infosys reported FY2024 revenue of ₹1,53,670 crore with a net margin of 17.2%."},
    ]

    question = "What was TCS revenue growth in FY2024 and how does it compare to Infosys?"

    print("NAIVE formatting result:")
    print(answer_with_rag(question, chunks, use_optimized=False))
    print("\n" + "="*60)
    print("\nOPTIMIZED formatting result:")
    print(answer_with_rag(question, chunks, use_optimized=True))


if __name__ == "__main__":
    main()
