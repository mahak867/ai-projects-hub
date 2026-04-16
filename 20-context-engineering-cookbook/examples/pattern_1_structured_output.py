"""
Pattern 1: Structured JSON Output
Demonstrates how to reliably get structured data from Claude.
"""
from typing import Dict, Optional
import json
import os
import sys

import anthropic

# Validate API key at startup
_api_key = os.getenv("ANTHROPIC_API_KEY")
if not _api_key:
    print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
    print("Get your key at: https://console.anthropic.com")
    sys.exit(1)

client = anthropic.Anthropic(api_key=_api_key)


def extract_stock_data(text: str) -> Dict[str, object]:
    """Extract structured stock data from a natural-language news snippet.

    Args:
        text: Raw text mentioning a stock (e.g. a news headline or blurb)

    Returns:
        Dictionary with company, symbol, price, change_pct, and recommendation

    Raises:
        ValueError: If Claude returns invalid JSON
    """
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": f"""Extract stock information from the text below.
Return ONLY valid JSON — no preamble, no markdown fences:
{{"company": "string", "symbol": "string", "price": number, "change_pct": number, "recommendation": "BUY|SELL|HOLD|null"}}

TEXT: {text}""",
        }],
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1].lstrip("json").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Claude returned invalid JSON: {e}\nResponse: {raw}") from e


def main() -> None:
    """Run example extractions to demonstrate the pattern."""
    texts = [
        "TCS shares rose 3.2% to ₹4,150 today after strong Q3 results. Analysts recommend buying.",
        "Infosys (INFY) fell 2.1% to ₹1,820 on weak guidance. Most analysts are holding.",
        "HDFC Bank up 1.5% at ₹1,650, outperforming the Nifty Bank index.",
    ]
    for text in texts:
        print(f"Input: {text}")
        result = extract_stock_data(text)
        print(json.dumps(result, indent=2))
        print()


if __name__ == "__main__":
    main()
