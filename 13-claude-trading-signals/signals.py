"""
Claude Trading Signals — Technical analysis + AI interpretation for NSE stocks
Paper trading tracker (NOT financial advice)
"""
import anthropic
import yfinance as yf
import pandas as pd
import json
import os
import sqlite3
from datetime import datetime

import sys

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
    print("   Fix: export ANTHROPIC_API_KEY='sk-ant-...'")
    print("   Get a key: https://console.anthropic.com")
    sys.exit(1)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
DB_PATH = "paper_trades.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY, symbol TEXT, action TEXT, price REAL,
        quantity INTEGER, date TEXT, signal_reason TEXT, pnl REAL DEFAULT 0
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS signals (
        id INTEGER PRIMARY KEY, symbol TEXT, signal TEXT, confidence INTEGER,
        analysis TEXT, date TEXT, price REAL
    )""")
    conn.commit()
    return conn

def compute_technicals(symbol: str, period: str = "6mo") -> dict:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    if hist.empty:
        return {}

    close = hist['Close']
    volume = hist['Volume']

    # Moving averages
    sma20 = close.rolling(20).mean().iloc[-1]
    sma50 = close.rolling(50).mean().iloc[-1]
    ema12 = close.ewm(span=12).mean().iloc[-1]
    ema26 = close.ewm(span=26).mean().iloc[-1]
    macd = ema12 - ema26
    signal_line = pd.Series([macd]).ewm(span=9).mean().iloc[-1]

    # RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    rsi = (100 - (100 / (1 + rs))).iloc[-1]

    # Bollinger Bands
    sma20_bb = close.rolling(20).mean()
    std20 = close.rolling(20).std()
    bb_upper = (sma20_bb + 2 * std20).iloc[-1]
    bb_lower = (sma20_bb - 2 * std20).iloc[-1]

    # Volume trend
    avg_vol = volume.rolling(20).mean().iloc[-1]
    curr_vol = volume.iloc[-1]

    current_price = float(close.iloc[-1])
    prev_price = float(close.iloc[-2])
    week_ago = float(close.iloc[-5]) if len(close) >= 5 else prev_price
    month_ago = float(close.iloc[-21]) if len(close) >= 21 else prev_price

    return {
        "symbol": symbol,
        "current_price": round(current_price, 2),
        "day_change_pct": round((current_price - prev_price) / prev_price * 100, 2),
        "week_change_pct": round((current_price - week_ago) / week_ago * 100, 2),
        "month_change_pct": round((current_price - month_ago) / month_ago * 100, 2),
        "sma20": round(float(sma20), 2),
        "sma50": round(float(sma50), 2),
        "price_vs_sma20_pct": round((current_price - float(sma20)) / float(sma20) * 100, 2),
        "rsi": round(float(rsi), 1),
        "macd": round(float(macd), 3),
        "macd_signal": round(float(signal_line), 3),
        "bb_upper": round(float(bb_upper), 2),
        "bb_lower": round(float(bb_lower), 2),
        "bb_position_pct": round((current_price - float(bb_lower)) / (float(bb_upper) - float(bb_lower)) * 100, 1),
        "volume_vs_avg_pct": round((float(curr_vol) - float(avg_vol)) / float(avg_vol) * 100, 1),
        "above_sma20": current_price > float(sma20),
        "above_sma50": current_price > float(sma50),
        "golden_cross": float(sma20) > float(sma50),
    }

def generate_signal(technicals: dict) -> dict:
    prompt = f"""You are a technical analyst for Indian equities. Analyze these indicators and generate a trading signal.

TECHNICAL DATA:
{json.dumps(technicals, indent=2)}

RULES:
- RSI > 70: Overbought, lean bearish. RSI < 30: Oversold, lean bullish.
- Price > SMA20 and SMA20 > SMA50 (golden cross): Bullish trend
- MACD > Signal line: Bullish momentum
- BB position > 80%: Near upper band, potential reversal
- High volume confirms moves

Generate a JSON signal:
{{
  "signal": "<BUY|SELL|HOLD>",
  "confidence": <0-100>,
  "timeframe": "<Intraday|Swing (3-5 days)|Positional (2-4 weeks)>",
  "entry_price": <suggested entry>,
  "stop_loss": <suggested stop loss price>,
  "target": <price target>,
  "risk_reward": <ratio>,
  "reasoning": "<2-3 sentences explaining the signal>",
  "key_risks": ["risk1", "risk2"],
  "indicators_summary": "<which indicators are bullish/bearish>"
}}

IMPORTANT: This is for educational paper trading only, not real financial advice.
Return ONLY valid JSON."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError as e:
        raise ValueError(f"Claude returned invalid JSON for signal: {e}\nResponse: {raw}") from e

def analyze(symbols: list[str], save: bool = True) -> list[dict]:
    conn = init_db() if save else None
    results = []

    for symbol in symbols:
        print(f"Analyzing {symbol}...")
        technicals = compute_technicals(symbol)
        if not technicals:
            print(f"  No data for {symbol}")
            continue

        signal = generate_signal(technicals)
        result = {**technicals, **signal, "date": datetime.now().isoformat()}
        results.append(result)

        if save and conn:
            conn.execute(
                "INSERT INTO signals (symbol, signal, confidence, analysis, date, price) VALUES (?,?,?,?,?,?)",
                (symbol, signal["signal"], signal["confidence"], signal["reasoning"],
                 datetime.now().isoformat(), technicals["current_price"])
            )
            conn.commit()

        confidence_bar = "█" * (signal["confidence"] // 10) + "░" * (10 - signal["confidence"] // 10)
        signal_emoji = {"BUY": "🟢", "SELL": "🔴", "HOLD": "🟡"}.get(signal["signal"], "⚪")

        print(f"  {signal_emoji} {signal['signal']} | Confidence: {confidence_bar} {signal['confidence']}%")
        print(f"  Entry: ₹{signal.get('entry_price')} | SL: ₹{signal.get('stop_loss')} | Target: ₹{signal.get('target')}")
        print(f"  {signal['reasoning']}")

    if conn:
        conn.close()
    return results

WATCHLIST = ["TCS.NS", "INFY.NS", "HDFCBANK.NS", "RELIANCE.NS", "ICICIBANK.NS"]

if __name__ == "__main__":
    import sys
    symbols = sys.argv[1:] if len(sys.argv) > 1 else WATCHLIST
    print("=" * 60)
    print("📊 NSE Trading Signals (Paper Trading Only)")
    print("=" * 60)
    print("⚠️  NOT financial advice. Educational use only.\n")
    results = analyze(symbols)
    print(f"\n✅ Analyzed {len(results)} stocks. Signals saved to {DB_PATH}")
