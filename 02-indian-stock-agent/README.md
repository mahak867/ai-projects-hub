# 🇮🇳 Indian Stock Analysis Agent

An AI agent that analyzes NSE/BSE stocks using real-time data and Claude's reasoning.

![Demo](https://img.shields.io/badge/difficulty-beginner-green?style=flat-square)

## What you'll build
An interactive CLI agent that can fetch real stock data, calculate returns, compare companies, and give you investment analysis — all powered by Claude with tool use.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python agent.py
```

## Example queries

```
Analyze TCS and give me a buy/sell recommendation
Compare HDFC Bank vs ICICI Bank vs SBI
Is Reliance Industries overvalued at current price?
Which Nifty IT stocks have the best ROE?
Show me the 1-year performance of BAJFINANCE
```

## How it works

Uses Claude's **tool use** feature — Claude decides which data to fetch, calls the tools, then synthesizes a complete analysis. The agent can chain multiple tool calls to answer complex questions.

**Tools available:**
- `get_stock_quote` — Live price, change, volume
- `get_historical_data` — Returns over any period
- `get_fundamentals` — P/E, ROE, margins, ratios
- `compare_stocks` — Side-by-side comparison

## Key concept: Tool Use (Function Calling)
Claude doesn't just generate text — it decides what data it needs, fetches it via tools, then reasons over real numbers. This is the foundation of every production AI agent.
