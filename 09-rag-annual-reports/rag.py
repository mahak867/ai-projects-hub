"""
RAG over NSE Annual Reports
Download annual reports → chunk → embed → vector search → Claude answers
"""
import anthropic
import chromadb
import requests
import PyPDF2
import io
import hashlib
import os
import argparse
from pathlib import Path

import os as _os, sys as _sys
_api_key = _os.getenv('ANTHROPIC_API_KEY')
if not _api_key:
    print('\u274c Error: ANTHROPIC_API_KEY environment variable not set')
    print('Get your key at: https://console.anthropic.com')
    _sys.exit(1)
client = anthropic.Anthropic(api_key=_api_key)
chroma = chromadb.PersistentClient(path="./chroma_db")

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return [c for c in chunks if len(c.strip()) > 50]

def embed_text(texts: list[str]) -> list[list[float]]:
    """Use Claude's embedding via a simple approach — hash-based for demo,
    or use voyage-ai / openai embeddings in production"""
    # For production: use voyage-ai embeddings (Anthropic recommends these)
    # from anthropic import Anthropic
    # Use: pip install voyageai and voyage_client.embed(texts)
    
    # Simple TF-IDF style embedding for demo (replace with real embeddings)
    import hashlib
    import math
    
    def simple_embed(text: str, dims: int = 384) -> list[float]:
        words = text.lower().split()
        vec = [0.0] * dims
        for word in words:
            h = int(hashlib.md5(word.encode()).hexdigest(), 16)
            idx = h % dims
            vec[idx] += 1.0
        norm = math.sqrt(sum(x*x for x in vec)) or 1
        return [x/norm for x in vec]
    
    return [simple_embed(t) for t in texts]

def ingest_pdf(pdf_path: str, company: str, year: str, collection_name: str = "annual_reports"):
    print(f"Ingesting {company} {year} annual report...")
    
    collection = chroma.get_or_create_collection(collection_name)
    
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        full_text = ""
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text += f"\n[Page {i+1}]\n{text}"
    
    chunks = chunk_text(full_text)
    print(f"  {len(chunks)} chunks from {len(reader.pages)} pages")
    
    embeddings = embed_text(chunks)
    
    ids = [f"{company}_{year}_{i}" for i in range(len(chunks))]
    metadatas = [{"company": company, "year": year, "chunk_id": i} for i in range(len(chunks))]
    
    # Add in batches
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        collection.add(
            documents=chunks[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
            ids=ids[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size]
        )
    
    print(f"  Ingested {len(chunks)} chunks")

def query(question: str, companies: list[str] = None, years: list[str] = None, 
          collection_name: str = "annual_reports", n_results: int = 8) -> str:
    
    collection = chroma.get_or_create_collection(collection_name)
    
    where = {}
    if companies and len(companies) == 1:
        where["company"] = companies[0]
    if years and len(years) == 1:
        where["year"] = years[0]
    
    query_embed = embed_text([question])[0]
    
    results = collection.query(
        query_embeddings=[query_embed],
        n_results=n_results,
        where=where if where else None,
        include=["documents", "metadatas"]
    )
    
    if not results["documents"][0]:
        return "No relevant information found in the annual reports."
    
    context_parts = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        context_parts.append(f"[{meta['company']} {meta['year']}]\n{doc}")
    
    context = "\n\n---\n\n".join(context_parts)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system="""You are a financial analyst expert on Indian companies. 
Answer questions based ONLY on the provided annual report excerpts.
Always cite which company and year your information comes from.
If information is not in the excerpts, say so clearly.""",
        messages=[{
            "role": "user",
            "content": f"""Based on the annual report excerpts below, answer this question:

QUESTION: {question}

EXCERPTS:
{context}

Provide a detailed, accurate answer citing specific companies and years."""
        }]
    )
    
    return response.content[0].text

def main():
    parser = argparse.ArgumentParser(description="RAG over NSE Annual Reports")
    subparsers = parser.add_subparsers(dest="command")
    
    ingest_parser = subparsers.add_parser("ingest", help="Ingest a PDF")
    ingest_parser.add_argument("pdf", help="Path to PDF file")
    ingest_parser.add_argument("company", help="Company name e.g. TCS")
    ingest_parser.add_argument("year", help="Year e.g. 2024")
    
    query_parser = subparsers.add_parser("query", help="Ask a question")
    query_parser.add_argument("question", help="Your question")
    query_parser.add_argument("--company", help="Filter by company")
    query_parser.add_argument("--year", help="Filter by year")
    
    args = parser.parse_args()
    
    if args.command == "ingest":
        ingest_pdf(args.pdf, args.company, args.year)
        print("Done! You can now query this report.")
    
    elif args.command == "query":
        companies = [args.company] if args.company else None
        years = [args.year] if args.year else None
        answer = query(args.question, companies, years)
        print(f"\n📊 Answer:\n{answer}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
