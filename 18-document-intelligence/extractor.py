"""Document Intelligence — extract, compare, and analyze multiple documents with Claude"""
import anthropic, PyPDF2, json, io, os, argparse
from pathlib import Path

client = anthropic.Anthropic()

def extract_pdf(path: str) -> str:
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return "\n".join(p.extract_text() for p in reader.pages if p.extract_text())

def extract_structured(text: str, doc_type: str, schema: dict) -> dict:
    prompt = f"""Extract structured information from this {doc_type}.

SCHEMA TO EXTRACT:
{json.dumps(schema, indent=2)}

DOCUMENT:
{text[:10000]}

Return ONLY valid JSON matching the schema exactly. Use null for missing fields."""

    r = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=2000,
        messages=[{"role": "user", "content": prompt}])
    raw = r.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"): raw = raw[4:]
    return json.loads(raw.strip())

def compare_documents(docs: list[dict], comparison_focus: str = "all differences") -> str:
    prompt = f"""Compare these documents and analyze {comparison_focus}.

DOCUMENTS:
{json.dumps(docs, indent=2, default=str)[:12000]}

Provide:
1. Key similarities
2. Important differences  
3. Trends over time (if applicable)
4. Recommendations based on the comparison
5. Summary table (use markdown)

Be specific with numbers and facts."""

    r = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=2000,
        messages=[{"role": "user", "content": prompt}])
    return r.content[0].text

SCHEMAS = {
    "annual_report": {
        "company_name": "string", "fiscal_year": "string",
        "revenue": "number (crores)", "net_profit": "number (crores)",
        "eps": "number", "dividend_per_share": "number",
        "total_assets": "number", "key_highlights": ["string"],
        "major_risks": ["string"], "ceo_message_summary": "string",
    },
    "contract": {
        "parties": ["string"], "effective_date": "string",
        "value": "string", "duration": "string",
        "key_obligations": ["string"], "termination_conditions": ["string"],
        "governing_law": "string",
    },
    "research_paper": {
        "title": "string", "authors": ["string"], "abstract": "string",
        "methodology": "string", "key_findings": ["string"],
        "limitations": ["string"], "future_work": "string",
    },
    "invoice": {
        "vendor": "string", "customer": "string", "invoice_number": "string",
        "date": "string", "items": [{"description": "string", "amount": "number"}],
        "total": "number", "due_date": "string", "payment_terms": "string",
    }
}

def main():
    parser = argparse.ArgumentParser(description="Document Intelligence with Claude")
    sub = parser.add_subparsers(dest="command")

    ext = sub.add_parser("extract", help="Extract structured data from a PDF")
    ext.add_argument("pdf", help="PDF file path")
    ext.add_argument("--type", choices=list(SCHEMAS.keys()), default="annual_report")
    ext.add_argument("--output", help="Save JSON to file")

    cmp = sub.add_parser("compare", help="Compare multiple PDFs")
    cmp.add_argument("pdfs", nargs="+", help="PDF files to compare")
    cmp.add_argument("--type", choices=list(SCHEMAS.keys()), default="annual_report")
    cmp.add_argument("--focus", default="all differences and trends")

    args = parser.parse_args()

    if args.command == "extract":
        print(f"Extracting {args.type} data from {args.pdf}...")
        text = extract_pdf(args.pdf)
        result = extract_structured(text, args.type, SCHEMAS[args.type])
        print(json.dumps(result, indent=2))
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Saved to {args.output}")

    elif args.command == "compare":
        print(f"Comparing {len(args.pdfs)} documents...")
        extracted = []
        for pdf in args.pdfs:
            text = extract_pdf(pdf)
            data = extract_structured(text, args.type, SCHEMAS[args.type])
            data["_source_file"] = Path(pdf).name
            extracted.append(data)
            print(f"  Processed: {pdf}")
        print("\nGenerating comparison report...")
        report = compare_documents(extracted, args.focus)
        print(report)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
