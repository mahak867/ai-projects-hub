"""Pattern 1: Structured JSON Output"""
import anthropic, json

client = anthropic.Anthropic()

def extract_stock_data(text: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{"role": "user", "content": f"""Extract stock information.
Return ONLY valid JSON:
{{"company": "string", "symbol": "string", "price": number, "change_pct": number, "recommendation": "BUY|SELL|HOLD|null"}}

TEXT: {text}"""}]
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"): raw = raw.split("```")[1].lstrip("json").strip()
    return json.loads(raw)

# Test it
texts = [
    "TCS shares rose 3.2% to ₹4,150 today after strong Q3 results. Analysts recommend buying.",
    "Infosys (INFY) fell 2.1% to ₹1,820 on weak guidance. Most analysts are holding.",
]
for text in texts:
    result = extract_stock_data(text)
    print(json.dumps(result, indent=2))
    print()
