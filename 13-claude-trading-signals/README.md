# 📊 Claude Trading Signals

Technical analysis pipeline: compute RSI/MACD/Bollinger → Claude interprets → generates BUY/SELL/HOLD signal with entry, stop loss, target.

![Demo](https://img.shields.io/badge/difficulty-advanced-red?style=flat-square)

> ⚠️ **Paper trading only. NOT financial advice.**

## Setup
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage
```bash
# Analyze default watchlist
python signals.py

# Analyze specific stocks
python signals.py TCS.NS INFY.NS BAJFINANCE.NS

# Single stock deep dive
python signals.py RELIANCE.NS
```

## Sample output
```
🟢 BUY | Confidence: ████████░░ 80%
Entry: ₹3,450 | SL: ₹3,380 | Target: ₹3,600
RSI at 42 with golden cross forming — momentum building on above-average volume.
```

## Indicators computed
RSI (14), MACD (12/26/9), Bollinger Bands, SMA20/50, Golden Cross, Volume trend

## Key concept: AI + deterministic computation
Compute indicators with pandas (reliable math), then use Claude for interpretation (pattern recognition + context). Never let AI do the math; let it do the reasoning.

## ⚠️ Known Limitations
- **Paper trading only**: Signals are for educational and research purposes — this is NOT financial advice and should not be used for real trades
- **Data delay**: yfinance prices may be delayed by 15 minutes; signals based on delayed data should not be used for intraday decisions
- **No backtesting**: Signal quality is not historically validated; there is no built-in backtesting or performance tracking
- **Limited indicators**: The current set (RSI, MACD, Bollinger Bands) covers common patterns but misses options, order-flow, and fundamental signals

## 🧪 Testing & Linting

```bash
# Install linter
pip install ruff

# Check for style and correctness issues
ruff check .

# Verify all dependencies install correctly
pip install -r requirements.txt

# Smoke test — confirm imports load without error
python -c "import anthropic, yfinance, pandas; print('All dependencies OK')"
```
