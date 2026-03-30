"""Pattern 7: Self-Critique Loop"""
import anthropic

client = anthropic.Anthropic()

def analyze_with_critique(question: str) -> str:
    # Step 1: Initial answer
    r1 = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=600,
        messages=[{"role": "user", "content": question}])
    initial = r1.content[0].text

    # Step 2: Self-critique
    r2 = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=400,
        messages=[
            {"role": "user", "content": question},
            {"role": "assistant", "content": initial},
            {"role": "user", "content": "Review your answer critically. What are the 2-3 weakest or most uncertain points? What important context did you miss?"}
        ])
    critique = r2.content[0].text

    # Step 3: Revised answer
    r3 = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=800,
        messages=[{"role": "user", "content": f"""Original question: {question}
Your initial answer: {initial}
Your self-critique: {critique}

Write an improved final answer that addresses the critique."""}])
    return r3.content[0].text

result = analyze_with_critique("What are the key risks of investing in Indian small-cap stocks in 2025?")
print(result)
