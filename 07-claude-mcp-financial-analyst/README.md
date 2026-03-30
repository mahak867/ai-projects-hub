# 💹 Claude MCP Financial Analyst

An MCP server that gives Claude Desktop real-time access to NSE/BSE stock data, screening, and portfolio analytics.

![Demo](https://img.shields.io/badge/difficulty-intermediate-orange?style=flat-square)

## What this unlocks in Claude Desktop

After setup, you can ask Claude things like:
- *"Analyze TCS.NS and compare it to Infosys.NS"*
- *"Screen these 20 NSE stocks for ROE > 20% and PE < 25"*
- *"Calculate returns for a portfolio: 40% Reliance, 30% HDFC Bank, 30% TCS"*
- *"Which sectors are performing best this month?"*

## Setup

```bash
pip install -r requirements.txt
```

Edit `claude_desktop_config.json` — replace path with your actual path.

Copy to Claude Desktop config:
- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Restart Claude Desktop. You'll see a 🔧 icon in the chat input.

## Tools available

| Tool | What it does |
|------|-------------|
| `get_stock_data` | Full fundamentals + technicals for any symbol |
| `screen_stocks` | Filter by ROE, P/E, market cap |
| `calculate_returns` | Portfolio return + Sharpe ratio |
| `get_sector_performance` | All NSE sectors ranked by performance |

## Key concept: MCP
Model Context Protocol lets Claude call external tools directly from the chat interface, without you writing any code each time. Build once, use forever.
