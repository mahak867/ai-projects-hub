# 📈 Open Source Screener

> **Difficulty:** Advanced  
> **Time to Complete:** ~30 minutes

Self-hosted Indian stock screener with Claude AI analysis. Screen NSE/BSE stocks by fundamentals and get AI-powered investment insights.

## What This Does

Screens any list of NSE/BSE stocks against your chosen fundamental criteria (ROE, P/E, market cap, debt) and then runs Claude AI analysis on the results — giving you top picks, sector trends, valuation summaries, and red flags.

## Demo

```
$ python screener.py --min-roe 15 --max-pe 30

📈 Open Source NSE Screener
Screening 20 stocks with filters:
  Min ROE: 15% | Max P/E: 30 | Min Cap: ₹5,000 Cr

✓ 8 stocks passed filters

Symbol           Name                           Price     ROE%     P/E    MarCap Cr   1Y Ret%
-----------------------------------------------------------------------------------------------
TCS.NS           Tata Consultancy Services    4150.00    45.2    28.3      1512000    12.3
...

🤖 Claude AI Analysis:
**Top 3 Picks**
1. TCS.NS — Strong ROE of 45%, reasonable P/E at 28x for a market leader...
```

## Prerequisites

- Python 3.10 or higher
- Anthropic API key ([get one free](https://console.anthropic.com))

## Installation

```bash
git clone https://github.com/mahak867/ai-projects-hub.git
cd ai-projects-hub/17-open-source-screener

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Setup

```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

## Usage

```bash
# Screen Nifty 50 with default filters
python screener.py

# Custom filters
python screener.py --min-roe 15 --max-pe 25

# Screen specific stocks
python screener.py --symbols TCS.NS INFY.NS WIPRO.NS HDFCBANK.NS

# Screen without AI analysis (faster)
python screener.py --min-roe 20 --no-ai

# Save results to JSON
python screener.py --output results.json
```

### All Options

| Flag | Default | Description |
|------|---------|-------------|
| `--symbols` | Nifty 50 | Space-separated list of Yahoo Finance symbols |
| `--min-roe` | 10 | Minimum return on equity (%) |
| `--max-pe` | 50 | Maximum trailing P/E ratio |
| `--min-cap` | 5000 | Minimum market cap in Crores |
| `--max-de` | 3 | Maximum debt-to-equity ratio |
| `--no-ai` | — | Skip Claude AI analysis |
| `--output` | — | Save JSON results to file |

## Project Structure

```
17-open-source-screener/
├── screener.py          # Main screener with CLI and AI analysis
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## How It Works

1. Fetches stock data from Yahoo Finance using `yfinance`
2. Applies your chosen fundamental filters (ROE, P/E, market cap, debt)
3. Displays a formatted table of stocks that pass
4. Sends the screened results to Claude for AI-powered analysis
5. Claude returns top picks, sector insights, valuation commentary, and red flags

## Troubleshooting

**"No data available" for some symbols**
→ Some stocks may have incomplete data on Yahoo Finance. Try again or check the symbol format (must end in `.NS` for NSE or `.BO` for BSE).

**"ANTHROPIC_API_KEY not set"**
→ Run `export ANTHROPIC_API_KEY='sk-ant-...'` before running the script.

**"ImportError: No module named yfinance"**
→ Run `pip install -r requirements.txt`

## Learn More

- [Anthropic Claude API Docs](https://docs.anthropic.com/)
- [yfinance Documentation](https://python-yfinance.readthedocs.io/)
- [NSE Official Site](https://www.nseindia.com/)

---

**Built with Claude by Anthropic** | [More AI Projects](https://github.com/mahak867/ai-projects-hub)

## ⚠️ Known Limitations
- **Data delay**: Yahoo Finance prices are delayed by up to 15–30 minutes; not suitable for intraday decisions
- **Fundamental data accuracy**: Ratios (ROE, P/E, D/E) are sourced from Yahoo Finance and may differ slightly from official BSE/NSE filings
- **BSE coverage**: BSE symbols (`.BO` suffix) have lower data coverage than NSE (`.NS`) on Yahoo Finance — some BSE stocks may show incomplete metrics
- **No real-time order book**: This is a screener, not a trading terminal; it does not connect to any brokerage API

## 🧪 Testing & Linting

```bash
# Install linter
pip install ruff

# Check for style and correctness issues
ruff check .

# Verify all dependencies install correctly
pip install -r requirements.txt

# Smoke test — confirm imports load without error
python -c "import anthropic, yfinance; print('All dependencies OK')"

# Run screener without AI analysis (no API key needed for this step)
python screener.py --no-ai
```
