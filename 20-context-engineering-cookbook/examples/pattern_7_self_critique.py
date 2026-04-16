"""
Pattern 7: Self-Critique Loop
Shows how to improve Claude's answers by asking it to critique and revise its own work.
"""
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


def analyze_with_critique(question: str) -> str:
    """Run a three-pass self-critique loop to produce a better answer.

    Pass 1 — Initial answer
    Pass 2 — Self-critique (find weaknesses and gaps)
    Pass 3 — Revised answer incorporating the critique

    Args:
        question: The question to answer

    Returns:
        Improved final answer as a string
    """
    # Pass 1: Initial answer
    r1 = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600,
        messages=[{"role": "user", "content": question}],
    )
    initial = r1.content[0].text

    # Pass 2: Self-critique
    r2 = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[
            {"role": "user", "content": question},
            {"role": "assistant", "content": initial},
            {
                "role": "user",
                "content": (
                    "Review your answer critically. "
                    "What are the 2-3 weakest or most uncertain points? "
                    "What important context did you miss?"
                ),
            },
        ],
    )
    critique = r2.content[0].text

    # Pass 3: Revised answer
    r3 = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        messages=[{
            "role": "user",
            "content": (
                f"Original question: {question}\n"
                f"Your initial answer: {initial}\n"
                f"Your self-critique: {critique}\n\n"
                "Write an improved final answer that addresses the critique."
            ),
        }],
    )
    return r3.content[0].text


def main() -> None:
    """Run an example self-critique analysis."""
    question = "What are the key risks of investing in Indian small-cap stocks?"
    print(f"Question: {question}\n")
    print("Running 3-pass self-critique loop...\n")
    result = analyze_with_critique(question)
    print("Final Answer:\n")
    print(result)


if __name__ == "__main__":
    main()
