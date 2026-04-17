"""
Pattern 4: Few-Shot Examples
Show Claude the exact input→output format you want before asking your real question.
Dramatically improves consistency and format adherence.
"""
import os, sys, json
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not set"); sys.exit(1)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def classify_news_sentiment(headline: str) -> dict:
    """Classify a financial news headline using few-shot examples.

    Args:
        headline: News headline string

    Returns:
        Dict with sentiment, impact, affected_sectors, confidence
    """
    prompt = f"""Classify financial news headlines for Indian market impact.

Examples:
INPUT: "RBI holds repo rate steady at 6.5%, signals cautious outlook"
OUTPUT: {{"sentiment": "Neutral", "impact": "Medium", "affected_sectors": ["Banking", "Real Estate", "NBFCs"], "confidence": 90, "reasoning": "Rate hold was expected; cautious language limits upside"}}

INPUT: "Infosys raises FY25 revenue guidance to 4.5-5% in constant currency"
OUTPUT: {{"sentiment": "Positive", "impact": "High", "affected_sectors": ["IT", "Technology"], "confidence": 88, "reasoning": "Guidance upgrade signals demand recovery; IT sector re-rating likely"}}

INPUT: "India's CPI inflation rises to 6.8%, above RBI's 6% upper tolerance"  
OUTPUT: {{"sentiment": "Negative", "impact": "High", "affected_sectors": ["Banking", "FMCG", "Consumer"], "confidence": 85, "reasoning": "Above-tolerance inflation increases rate hike probability, dampens consumption"}}

Now classify:
INPUT: "{headline}"
OUTPUT:"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def main():
    headlines = [
        "Reliance Industries Q3 profit rises 11% YoY, beats estimates",
        "FII outflows hit ₹45,000 crore in January amid dollar strength",
        "SEBI tightens F&O margin rules effective April 2025",
    ]
    for h in headlines:
        print(f"\nHeadline: {h}")
        result = classify_news_sentiment(h)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
