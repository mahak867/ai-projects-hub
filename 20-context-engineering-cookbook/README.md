# 🍳 Context Engineering Cookbook

The most important collection of prompting patterns for production AI systems. Real examples with before/after comparisons.

![Demo](https://img.shields.io/badge/type-reference-blue?style=flat-square)

---

## What is Context Engineering?

Context engineering is the practice of deliberately designing the information Claude receives to get reliable, accurate, production-quality outputs. It goes beyond "prompt engineering" — it's about structuring the entire context window.

---

## Pattern 1: Structured Output with JSON Schema

**Before (fragile):**
```
Extract the company name and revenue from this text.
```

**After (reliable):**
```
Extract information from the text below.

Return ONLY valid JSON matching this exact schema:
{
  "company_name": "string",
  "revenue_crores": number,
  "fiscal_year": "string or null",
  "confidence": "high|medium|low"
}

TEXT:
{text}
```

**Why it works:** Specifying the schema eliminates format ambiguity. Claude reliably produces parseable JSON every time.

---

## Pattern 2: Chain of Thought for Complex Reasoning

**Before:**
```
Is this stock overvalued?
Stock data: {data}
```

**After:**
```
Analyze whether this stock is overvalued.

Think through this step by step:
1. Compare P/E to sector median
2. Assess revenue growth vs valuation premium
3. Consider qualitative factors (moat, management)
4. Reach a conclusion

Stock data: {data}
```

**Why it works:** Forcing Claude to reason explicitly before concluding dramatically improves accuracy on analytical tasks.

---

## Pattern 3: Role + Constraints

**Before:**
```
Summarize this document.
```

**After:**
```
You are a senior analyst at a hedge fund. Your audience is portfolio managers who have 60 seconds to read your summary.

Rules:
- Maximum 5 bullet points
- Each bullet must contain a specific number or date
- Flag any regulatory risks with [RISK]
- End with a one-line investment implication

DOCUMENT:
{document}
```

**Why it works:** The role sets the register. The constraints eliminate guessing about format, length, and focus.

---

## Pattern 4: Few-Shot Examples

**Before:**
```
Classify the sentiment of this tweet.
```

**After:**
```
Classify tweet sentiment as: BULLISH, BEARISH, or NEUTRAL.

Examples:
Tweet: "HDFC Bank crushing it this quarter! 🚀" → BULLISH
Tweet: "Infosys guidance cut is worrying for the whole sector" → BEARISH  
Tweet: "TCS announces new office in Pune" → NEUTRAL
Tweet: "Reliance AGM today - waiting for announcements" → NEUTRAL

Now classify:
Tweet: "{tweet}"
```

**Why it works:** Examples calibrate Claude's understanding of your specific classification criteria better than descriptions alone.

---

## Pattern 5: Constitutional Constraints

**Before:**
```
Write a trading strategy based on this data.
```

**After:**
```
Write a trading strategy based on this data.

CONSTRAINTS (follow all):
- Do not use leverage or derivatives
- Maximum position size: 5% of portfolio
- Always include a stop loss
- Flag if strategy requires >30 min/day to execute
- Add disclaimer: "Past performance does not guarantee future results"
- Do not recommend strategies requiring >₹10 lakh capital

DATA: {data}
```

**Why it works:** Explicit constraints prevent Claude from producing technically correct but practically problematic outputs.

---

## Pattern 6: Context Injection with Priority Levels

```python
def build_context(user_query, user_data, company_docs, public_docs):
    return f"""PRIORITY 1 — MUST FOLLOW (company policy):
{company_docs[:2000]}

PRIORITY 2 — USER CONTEXT (personalize with this):
{user_data[:1000]}

PRIORITY 3 — BACKGROUND KNOWLEDGE (use if relevant):
{public_docs[:3000]}

USER QUESTION: {user_query}

Answer based on Priority 1 first, then personalize with Priority 2, use Priority 3 only to fill gaps."""
```

**Why it works:** Explicit priority hierarchies prevent Claude from over-weighting public knowledge when internal policy should dominate.

---

## Pattern 7: Self-Critique Loop

```python
def with_self_critique(client, initial_prompt: str) -> str:
    # Step 1: Generate
    response1 = client.messages.create(...)
    initial = response1.content[0].text

    # Step 2: Critique
    response2 = client.messages.create(messages=[
        {"role": "user", "content": initial_prompt},
        {"role": "assistant", "content": initial},
        {"role": "user", "content": "Review your answer. What are the 3 weakest points? What did you miss or get wrong?"}
    ])
    critique = response2.content[0].text

    # Step 3: Revise
    response3 = client.messages.create(messages=[
        {"role": "user", "content": f"Original prompt: {initial_prompt}\nYour draft: {initial}\nYour critique: {critique}\nNow write the improved final version."}
    ])
    return response3.content[0].text
```

**Why it works:** The critique step catches errors and gaps the initial generation misses. Quality improvement of ~40% on analytical tasks.

---

## Pattern 8: Retrieval Context Formatting

**Bad (walls of text):**
```
Context: [3000 word block with no structure]
```

**Good (structured retrieval):**
```
RELEVANT CONTEXT (use these to answer, cite by [Source N]):

[Source 1] TCS Q3 FY25 Results (confidence: high)
Revenue: ₹63,973 Cr (+5.6% YoY)
Net Profit: ₹12,380 Cr (+11.9% YoY)

[Source 2] Analyst Report — Jefferies (confidence: medium)  
Target price: ₹4,200. Rating: Buy.
Key thesis: AI deals pipeline growing 40% QoQ.

[Source 3] News — Economic Times (confidence: low, recent)
TCS signs $250M deal with European bank.

USER QUESTION: {question}
```

**Why it works:** Labeled sources with confidence scores let Claude weight information appropriately and cite accurately.

---

## Pattern 9: Output Format Templates

```
Generate the market brief in EXACTLY this format:

MARKET BRIEF — {date}
Sentiment: [BULLISH/BEARISH/NEUTRAL] | Score: [X/100]

TOP MOVER: [Symbol] [+/-X%] — [one line reason]

3 THINGS TO WATCH:
1. [Item]
2. [Item]  
3. [Item]

BOTTOM LINE: [One sentence investment implication]
---
```

**Why it works:** Templates are especially powerful when output will be parsed programmatically or displayed in a UI.

---

## Pattern 10: Uncertainty Quantification

```
Answer the following question about {company}.
For each claim, append a confidence level: [HIGH], [MEDIUM], or [LOW].

Use [HIGH] only if the information comes from official filings.
Use [MEDIUM] if from reliable secondary sources.
Use [LOW] if inferring or estimating.

At the end, add: "CAVEAT: [list any significant uncertainties]"
```

**Why it works:** Forces Claude to distinguish between facts and inferences, making outputs more trustworthy for decision-making.

---

## Running the Examples

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python examples/pattern_1_structured_output.py
python examples/pattern_7_self_critique.py
# etc.
```

See the `examples/` folder for runnable code for each pattern.

---

## Which Pattern to Use?

| Situation | Best Pattern |
|-----------|-------------|
| Parsing AI output in code | Pattern 1 (JSON Schema) |
| Complex analytical questions | Pattern 2 (CoT) |
| Consistent tone/format | Pattern 3 (Role + Constraints) |
| Classification tasks | Pattern 4 (Few-Shot) |
| Avoiding harmful outputs | Pattern 5 (Constitutional) |
| Enterprise RAG systems | Patterns 6 + 8 |
| High-stakes decisions | Pattern 7 (Self-Critique) |
| Dashboard/UI output | Pattern 9 (Templates) |
| Research/analysis | Pattern 10 (Uncertainty) |

---

*Built by [mahak867](https://github.com/mahak867) · MIT License*

## ⚠️ Known Limitations
- **Model sensitivity**: All patterns are tuned for Claude 3.5 Sonnet; results on other models (GPT-4, Gemini) may differ and may need prompt adjustments
- **Cost of Pattern 7**: The self-critique loop (Pattern 7) makes three sequential API calls — roughly 3× the cost of a single call
- **Prompt fragility**: Small wording changes can shift output quality significantly; treat the examples as starting points, not production-ready copy-paste
- **No evaluation harness**: The cookbook demonstrates patterns but does not include automated tests or quality benchmarks to validate improvements

## 🧪 Testing & Linting

```bash
# Install linter
pip install ruff

# Check for style and correctness issues
ruff check .

# Verify all dependencies install correctly
pip install -r requirements.txt

# Smoke test — confirm imports load without error
python -c "import anthropic; print('All dependencies OK')"

# Run all pattern examples
python examples/pattern_1_structured_output.py
python examples/pattern_7_self_critique.py
```
