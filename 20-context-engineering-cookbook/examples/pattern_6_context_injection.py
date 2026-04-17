"""
Pattern 6: Context Injection with Priority Levels
When injecting multiple context sources, explicitly label their priority.
Claude respects the hierarchy and resolves conflicts correctly.
"""
import os, sys, json
from datetime import datetime
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not set"); sys.exit(1)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def answer_with_prioritized_context(
    question: str,
    realtime_data: dict,
    historical_data: dict,
    general_knowledge: str,
) -> str:
    """Answer using multiple context sources with explicit priority ordering.

    Priority: real-time data > historical data > general knowledge.
    Claude is told this explicitly so it resolves conflicts correctly.

    Args:
        question: User question
        realtime_data: Most recent data (highest priority)
        historical_data: Historical context (medium priority)
        general_knowledge: Background info (lowest priority)

    Returns:
        Claude's answer
    """
    prompt = f"""Answer the question using the context below.
PRIORITY ORDER: Real-time data > Historical data > General knowledge.
If sources conflict, always prefer higher-priority data and explain the conflict.

[PRIORITY 1 — REAL-TIME DATA — use this first, override others if conflict]
{json.dumps(realtime_data, indent=2)}

[PRIORITY 2 — HISTORICAL DATA — use for trend context]
{json.dumps(historical_data, indent=2)}

[PRIORITY 3 — GENERAL KNOWLEDGE — background only, lowest trust]
{general_knowledge}

QUESTION: {question}

Answer in 150 words max. Cite which priority level your key facts come from."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def main():
    realtime = {"TCS_price": 4150, "TCS_change_pct": 2.3, "timestamp": datetime.now().isoformat(), "volume_vs_avg": "+45%"}
    historical = {"TCS_52w_high": 4350, "TCS_52w_low": 3200, "avg_pe_3yr": 26, "revenue_cagr_5yr": "14%"}
    background = "TCS is India's largest IT services company by market cap, part of the Tata Group."

    result = answer_with_prioritized_context(
        "Is TCS a good buy right now?",
        realtime, historical, background
    )
    print(result)


if __name__ == "__main__":
    main()
