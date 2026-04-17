"""
Pattern 9: Output Format Templates
Give Claude the exact template to fill in — not just "return JSON".
Reduces parsing failures to near-zero in production.
"""
import os, sys, json, re
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not set"); sys.exit(1)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# The exact template Claude must fill — field names, types, and constraints are explicit
EARNINGS_TEMPLATE = {
    "company": "string — company name",
    "ticker": "string — NSE symbol without .NS",
    "result": "BEAT | MISS | IN-LINE",
    "eps_actual": "number — actual EPS in ₹",
    "eps_estimate": "number — analyst consensus estimate in ₹",
    "surprise_pct": "number — percentage surprise (positive = beat)",
    "revenue_cr": "number — revenue in crores",
    "yoy_growth_pct": "number — year-over-year revenue growth",
    "management_tone": "Optimistic | Cautious | Neutral | Concerned",
    "key_quote": "string — most important quote from management, max 20 words",
    "market_reaction": "string — expected stock move direction and magnitude",
    "sectors_impacted": ["string — sector name"],
    "confidence": "integer 0-100 — confidence in this analysis",
}


def parse_earnings_report(raw_text: str) -> dict:
    """Extract structured earnings data using an explicit output template.

    Args:
        raw_text: Raw earnings report text (press release, article, etc.)

    Returns:
        Structured earnings dict matching EARNINGS_TEMPLATE

    Raises:
        ValueError: If output cannot be parsed as JSON
    """
    prompt = f"""Extract earnings information from the text below.
Fill in EVERY field of this exact template. Use null for unavailable data.
Return ONLY the filled JSON — no preamble, no markdown fences.

TEMPLATE TO FILL:
{json.dumps(EARNINGS_TEMPLATE, indent=2)}

TEXT:
{raw_text}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Template output unparseable: {e}\nRaw: {raw}") from e


def main():
    sample_report = """
    Infosys Q3 FY2025 Results: Revenue at ₹41,764 crore, up 7.9% YoY.
    EPS came in at ₹22.3 vs analyst estimate of ₹21.8.
    CEO Salil Parekh said: "Deal pipeline remains strong across all verticals."
    Company raised FY25 revenue guidance to 4.5-5% in constant currency.
    Stock up 4% in pre-market trading.
    """
    result = parse_earnings_report(sample_report)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
