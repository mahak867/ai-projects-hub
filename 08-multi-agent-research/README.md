# 🔬 Multi-Agent Research Pipeline

Three Claude agents collaborate to produce better research than any single agent could.

![Demo](https://img.shields.io/badge/difficulty-intermediate-orange?style=flat-square)

## The agent pipeline

```
Topic → [Researcher] → [Critic] → [Writer] → Final Report
```

1. **Researcher** gathers comprehensive information
2. **Critic** challenges assumptions and finds gaps  
3. **Writer** synthesizes both into a balanced, polished report

## Usage

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

# Research any topic
python research.py "Impact of AI on Indian IT sector"

# Deep research mode
python research.py "NSE SME IPO boom 2024" --depth deep

# Save outputs
python research.py "Claude vs GPT-4" --save outputs/claude_vs_gpt

# Show all agent outputs
python research.py "Quantum computing" --show-all
```

## Example topics that work well
- Industry analysis: *"State of Indian fintech 2025"*
- Tech comparisons: *"RAG vs fine-tuning for production AI"*
- Market research: *"Electric vehicle adoption in India"*
- Concept explanations: *"How do transformer attention mechanisms work"*

## Key concept: Multi-agent critique loop
The critic agent dramatically improves output quality by forcing the system to address counterarguments. This pattern — generate, critique, synthesize — is used in production AI systems at major companies.

## ⚠️ Known Limitations
- **No internet access**: All three agents reason from Claude's training data only — no live search or fact-checking against current sources
- **API cost**: Runs three full Claude calls per topic; 3× more expensive than a single-prompt approach
- **Best for stable topics**: Works well for analytical and conceptual questions; may produce outdated results for fast-moving news topics
- **Output length**: Deep mode significantly increases response time and token usage for lengthy reports

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

# Quick functional test with a short topic
python research.py "What is RAG in AI?" --depth shallow
```
