"""
Pattern 3: Role + Constraints
Assign Claude a precise expert role AND define explicit constraints.
Role alone gives expertise; constraints prevent unwanted outputs.
"""
import os, sys
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not set"); sys.exit(1)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def get_financial_advice(question: str, user_profile: dict) -> str:
    """Answer a financial question with role + constraints.

    The role gives depth; the constraints ensure safety and relevance.

    Args:
        question: User's financial question
        user_profile: Dict with age, risk_tolerance, investment_horizon

    Returns:
        Claude's response as a string
    """
    system = f"""You are a SEBI-registered investment advisor with 15 years of experience 
in Indian equity markets (NSE/BSE). You specialize in retail investor education.

USER PROFILE:
- Age: {user_profile.get('age')}
- Risk tolerance: {user_profile.get('risk_tolerance')}
- Investment horizon: {user_profile.get('investment_horizon')}
- Monthly investable surplus: ₹{user_profile.get('monthly_surplus_inr', 0):,}

CONSTRAINTS — you MUST follow these:
1. Never recommend specific stocks — discuss categories or sectors only
2. Always mention that past returns don't guarantee future performance
3. Suggest consulting a financial advisor for personalized advice
4. Use ₹ and Indian market context (SIP, ELSS, PPF, NPS) not USD
5. Keep responses under 300 words — retail investors need clarity, not volume
6. If asked about options/derivatives, explain risk first before anything else"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=system,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text


def main():
    profile = {"age": 28, "risk_tolerance": "moderate", "investment_horizon": "10 years", "monthly_surplus_inr": 25000}
    questions = [
        "Should I invest in small-cap mutual funds?",
        "How should I split my ₹25,000 monthly savings?",
    ]
    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {get_financial_advice(q, profile)}")
        print("-" * 50)


if __name__ == "__main__":
    main()
