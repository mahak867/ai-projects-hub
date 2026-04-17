"""
Pattern 10: Uncertainty Quantification
Force Claude to express confidence levels explicitly.
In finance, knowing WHAT Claude knows vs guesses is as important as the answer.
"""
import os, sys, json
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not set"); sys.exit(1)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def analyze_with_uncertainty(claim: str, evidence: list[str]) -> dict:
    """Analyze a financial claim and explicitly quantify uncertainty.

    Args:
        claim: The claim to evaluate (e.g. "TCS will outperform in FY26")
        evidence: List of evidence strings supporting or opposing the claim

    Returns:
        Dict with verdict, confidence, reasoning, bull_case, bear_case,
        data_quality, and unknown_factors
    """
    evidence_text = "\n".join(f"- {e}" for e in evidence)

    prompt = f"""Evaluate this financial claim with explicit uncertainty quantification.

CLAIM: {claim}

EVIDENCE:
{evidence_text}

Respond with JSON only:
{{
  "verdict": "LIKELY TRUE | UNCERTAIN | LIKELY FALSE",
  "confidence_pct": <0-100, where 50 = genuinely uncertain>,
  "reasoning": "string — 2-3 sentences on why",
  "bull_case": "string — strongest argument FOR the claim",
  "bear_case": "string — strongest argument AGAINST the claim",
  "data_quality": "High | Medium | Low — how reliable is the evidence",
  "unknown_factors": ["string — key things we don't know that would change the answer"],
  "time_sensitivity": "string — how quickly could this change"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1].lstrip("json").strip().rstrip("`")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse uncertainty output: {e}") from e


def main():
    claim = "Indian IT sector will outperform broader Nifty 50 in the next 12 months"
    evidence = [
        "USD/INR stable at 83-84, supporting export revenues",
        "US Fed rate cuts expected to boost client IT budgets",
        "TCS and Infosys both raised guidance in Q3 FY25",
        "AI-related deal wins accelerating across top-tier IT firms",
        "Valuation premium (P/E 25x) already prices in recovery",
        "US recession risk remains non-trivial at ~30% probability",
    ]
    result = analyze_with_uncertainty(claim, evidence)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
