"""
NSE Earnings Monitor — watches for earnings announcements,
fetches stock data, runs Claude analysis, sends Telegram alerts.
"""
import anthropic
import yfinance as yf
import requests
import os
import json
import time
import schedule
from datetime import datetime
from dataclasses import dataclass

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Stocks to monitor
WATCHLIST = {
    "TCS.NS": "TCS",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "RELIANCE.NS": "Reliance",
    "ICICIBANK.NS": "ICICI Bank",
    "WIPRO.NS": "Wipro",
    "BAJFINANCE.NS": "Bajaj Finance",
    "AXISBANK.NS": "Axis Bank",
    "HINDUNILVR.NS": "HUL",
    "TATAMOTORS.NS": "Tata Motors",
}

@dataclass
class EarningsAlert:
    symbol: str
    name: str
    actual_eps: float | None
    estimate_eps: float | None
    surprise_pct: float | None
    revenue: float | None
    price: float
    change_pct: float
    analysis: str

def get_earnings_data(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    info = ticker.info
    hist = ticker.history(period="5d")
    
    earnings = ticker.earnings_history
    latest_eps = None
    estimate_eps = None
    surprise = None
    
    if earnings is not None and not earnings.empty:
        latest = earnings.iloc[-1]
        latest_eps = float(latest.get("epsActual", 0) or 0)
        estimate_eps = float(latest.get("epsEstimate", 0) or 0)
        if estimate_eps and estimate_eps != 0:
            surprise = ((latest_eps - estimate_eps) / abs(estimate_eps)) * 100
    
    current_price = float(hist['Close'].iloc[-1]) if not hist.empty else 0
    prev_price = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
    change_pct = ((current_price - prev_price) / prev_price * 100) if prev_price else 0
    
    return {
        "symbol": symbol,
        "name": info.get("longName", symbol),
        "price": round(current_price, 2),
        "change_pct": round(change_pct, 2),
        "eps_actual": latest_eps,
        "eps_estimate": estimate_eps,
        "surprise_pct": round(surprise, 2) if surprise else None,
        "revenue": info.get("totalRevenue"),
        "pe": info.get("trailingPE"),
        "market_cap": info.get("marketCap"),
    }

def analyze_earnings(data: dict) -> str:
    prompt = f"""Analyze this NSE earnings result in 3-4 sentences for a retail investor.
    
Company: {data['name']} ({data['symbol']})
Current Price: ₹{data['price']} ({'+' if data['change_pct'] >= 0 else ''}{data['change_pct']}% today)
EPS Actual: {data['eps_actual']}
EPS Estimate: {data['eps_estimate']}
EPS Surprise: {data['surprise_pct']}% {'beat' if (data['surprise_pct'] or 0) > 0 else 'miss'}
P/E Ratio: {data['pe']}

Give: (1) Whether this is a beat or miss and by how much, (2) What this means for the stock, (3) Short-term outlook.
Keep it under 120 words, plain text, no headers."""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def send_telegram(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[Telegram disabled] {message[:100]}...")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    })

def format_alert(data: dict, analysis: str) -> str:
    surprise = data.get('surprise_pct')
    surprise_emoji = "🟢" if (surprise or 0) > 0 else "🔴" if (surprise or 0) < 0 else "⚪"
    price_emoji = "📈" if data['change_pct'] > 0 else "📉"
    
    return f"""*🔔 NSE Earnings Alert*

{surprise_emoji} *{data['name']}* ({data['symbol'].replace('.NS', '')})
{price_emoji} ₹{data['price']} ({'+' if data['change_pct'] >= 0 else ''}{data['change_pct']}%)

*EPS:* {data['eps_actual']} vs {data['eps_estimate']} est.
*Surprise:* {'+' if (surprise or 0) > 0 else ''}{surprise}%

*Claude Analysis:*
{analysis}

_{datetime.now().strftime('%d %b %Y, %I:%M %p IST')}_"""

def check_earnings():
    print(f"\n[{datetime.now().strftime('%H:%M')}] Checking earnings...")
    for symbol, name in WATCHLIST.items():
        try:
            data = get_earnings_data(symbol)
            # Only alert if there's recent earnings data with surprise
            if data.get('surprise_pct') is not None:
                print(f"  {name}: EPS surprise {data['surprise_pct']}%")
                analysis = analyze_earnings(data)
                alert = format_alert(data, analysis)
                send_telegram(alert)
                print(f"  Alert sent for {name}")
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"  Error for {symbol}: {e}")

def run_once():
    """Run a single check and show results"""
    print("NSE Earnings Monitor — Single Run")
    print("=" * 50)
    for symbol, name in list(WATCHLIST.items())[:3]:
        print(f"\nChecking {name}...")
        data = get_earnings_data(symbol)
        analysis = analyze_earnings(data)
        alert = format_alert(data, analysis)
        print(alert)
        print("-" * 40)

if __name__ == "__main__":
    import sys
    if "--once" in sys.argv:
        run_once()
    else:
        print("NSE Earnings Monitor started")
        print(f"Monitoring {len(WATCHLIST)} stocks")
        print("Checking every 30 minutes during market hours")
        schedule.every(30).minutes.do(check_earnings)
        check_earnings()
        while True:
            schedule.run_pending()
            time.sleep(60)
