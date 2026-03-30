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
