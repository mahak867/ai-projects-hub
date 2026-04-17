"""
Pattern 5: Constitutional Constraints
Define a set of rules Claude must evaluate its OWN output against before responding.
Prevents harmful, biased, or off-brand outputs at the prompt level.
"""
import os, sys
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not set"); sys.exit(1)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

CONSTITUTION = """
RESPONSE CONSTITUTION — evaluate your draft against these before outputting:

1. ACCURACY: Every factual claim must be defensible. If uncertain, say so.
2. NO SPECIFIC STOCK TIPS: You may discuss sectors, ratios, and concepts — never say "buy X".
3. BALANCED: For every bullish point, consider the bear case.
4. INDIA-CONTEXT: Use NSE/BSE data, ₹ denominations, SEBI regulations — not US-centric defaults.
5. RISK-FIRST: Lead with risks before opportunities for any investment discussion.
6. BEGINNER-SAFE: Define jargon on first use. No assumed knowledge.

If your draft violates any rule, revise it before outputting.
"""


def generate_market_commentary(topic: str) -> str:
    """Generate market commentary governed by a response constitution.

    Args:
        topic: Market topic to comment on

    Returns:
        Commentary string that adheres to the constitution
    """
    system = f"You are a financial educator writing for retail investors in India.\n\n{CONSTITUTION}"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600,
        system=system,
        messages=[{"role": "user", "content": f"Write a 150-word market commentary on: {topic}"}],
    )
    return response.content[0].text


def main():
    topics = [
        "Why small-cap stocks are volatile",
        "How rising US interest rates affect Indian markets",
    ]
    for topic in topics:
        print(f"\nTopic: {topic}\n{'='*50}")
        print(generate_market_commentary(topic))


if __name__ == "__main__":
    main()
