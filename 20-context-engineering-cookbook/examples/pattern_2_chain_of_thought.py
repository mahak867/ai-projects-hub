"""
Pattern 2: Chain of Thought for Complex Reasoning
Force Claude to show its reasoning steps before giving an answer.
This dramatically improves accuracy on multi-step problems.
"""
import os, sys
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not set"); sys.exit(1)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def analyze_investment(company_data: dict) -> dict:
    """Use chain-of-thought to reason through an investment decision.

    Args:
        company_data: Dict with financials (revenue, growth, pe, debt_equity, etc.)

    Returns:
        Dict with reasoning steps and final recommendation
    """
    prompt = f"""Analyze this company as an investment opportunity.

COMPANY DATA:
{company_data}

Think through this step by step:

<reasoning>
Step 1 - Valuation: Is the P/E reasonable for the growth rate?
Step 2 - Financial health: What does the debt/equity and current ratio tell us?
Step 3 - Growth quality: Is revenue growth sustainable?
Step 4 - Risks: What are the top 2-3 risks?
Step 5 - Verdict: Synthesize steps 1-4 into a clear recommendation.
</reasoning>

After your reasoning, provide a final JSON:
{{"recommendation": "BUY|HOLD|SELL", "confidence": 0-100, "target_horizon": "string", "summary": "string"}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"full_response": response.content[0].text}


def main():
    company = {
        "name": "TCS",
        "pe_ratio": 28,
        "revenue_growth_pct": 12,
        "debt_to_equity": 0.05,
        "roe_pct": 45,
        "current_ratio": 3.2,
        "profit_margin_pct": 19,
        "sector": "IT Services",
    }
    print("Chain-of-Thought Investment Analysis\n" + "="*50)
    result = analyze_investment(company)
    print(result["full_response"])


if __name__ == "__main__":
    main()
