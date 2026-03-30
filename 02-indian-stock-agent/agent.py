import anthropic
import yfinance as yf
import json
from datetime import datetime, timedelta

client = anthropic.Anthropic()

# Tools Claude can use
tools = [
    {
        "name": "get_stock_quote",
        "description": "Get current price, change, volume for an NSE/BSE stock. Use symbol like RELIANCE.NS, TCS.NS, INFY.NS",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Yahoo Finance symbol e.g. RELIANCE.NS"}
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_historical_data",
        "description": "Get historical price data and calculate returns over different periods",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "period": {"type": "string", "enum": ["1mo", "3mo", "6mo", "1y", "2y", "5y"]}
            },
            "required": ["symbol", "period"]
        }
    },
    {
        "name": "get_fundamentals",
        "description": "Get P/E ratio, market cap, book value, dividend yield and other fundamentals",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"}
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "compare_stocks",
        "description": "Compare multiple stocks side by side",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbols": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of Yahoo Finance symbols"
                }
            },
            "required": ["symbols"]
        }
    }
]

def get_stock_quote(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="2d")
        current = hist['Close'].iloc[-1]
        prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
        change = current - prev
        change_pct = (change / prev) * 100
        return {
            "symbol": symbol,
            "name": info.get("longName", symbol),
            "price": round(current, 2),
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
            "volume": info.get("volume", 0),
            "market_cap_cr": round(info.get("marketCap", 0) / 1e7, 0),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}

def get_historical_data(symbol: str, period: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        if hist.empty:
            return {"error": "No data found"}
        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]
        returns = ((end_price - start_price) / start_price) * 100
        high = hist['High'].max()
        low = hist['Low'].min()
        return {
            "symbol": symbol,
            "period": period,
            "start_price": round(start_price, 2),
            "end_price": round(end_price, 2),
            "return_pct": round(returns, 2),
            "period_high": round(high, 2),
            "period_low": round(low, 2),
            "avg_volume": round(hist['Volume'].mean(), 0),
        }
    except Exception as e:
        return {"error": str(e)}

def get_fundamentals(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "symbol": symbol,
            "name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "pb_ratio": info.get("priceToBook"),
            "ps_ratio": info.get("priceToSalesTrailing12Months"),
            "roe": round(info.get("returnOnEquity", 0) * 100, 2) if info.get("returnOnEquity") else None,
            "roa": round(info.get("returnOnAssets", 0) * 100, 2) if info.get("returnOnAssets") else None,
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "dividend_yield": round(info.get("dividendYield", 0) * 100, 2) if info.get("dividendYield") else 0,
            "eps": info.get("trailingEps"),
            "book_value": info.get("bookValue"),
            "revenue_growth": round(info.get("revenueGrowth", 0) * 100, 2) if info.get("revenueGrowth") else None,
            "profit_margins": round(info.get("profitMargins", 0) * 100, 2) if info.get("profitMargins") else None,
        }
    except Exception as e:
        return {"error": str(e)}

def compare_stocks(symbols: list) -> dict:
    results = []
    for sym in symbols:
        quote = get_stock_quote(sym)
        fund = get_fundamentals(sym)
        hist = get_historical_data(sym, "1y")
        results.append({**quote, **fund, "1y_return": hist.get("return_pct")})
    return {"comparison": results}

def run_tool(name: str, inputs: dict) -> str:
    if name == "get_stock_quote":
        return json.dumps(get_stock_quote(**inputs))
    elif name == "get_historical_data":
        return json.dumps(get_historical_data(**inputs))
    elif name == "get_fundamentals":
        return json.dumps(get_fundamentals(**inputs))
    elif name == "compare_stocks":
        return json.dumps(compare_stocks(**inputs))
    return json.dumps({"error": "Unknown tool"})

def analyze(query: str) -> str:
    print(f"\n🔍 Analyzing: {query}\n")
    
    messages = [{"role": "user", "content": query}]
    
    system = """You are an expert Indian stock market analyst. You have access to real-time NSE/BSE data.

When analyzing stocks:
- Use Yahoo Finance symbols with .NS suffix for NSE stocks (e.g., RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS)
- Always fetch current data before making claims
- Give clear buy/hold/sell recommendations with reasoning
- Compare against sector peers when relevant
- Mention key risks
- Format output clearly with sections

Common NSE symbols: RELIANCE.NS, TCS.NS, HDFCBANK.NS, INFY.NS, ICICIBANK.NS, WIPRO.NS, 
BAJFINANCE.NS, HINDUNILVR.NS, ADANIENT.NS, TATAMOTORS.NS, NIFTY50 (^NSEI)"""

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system,
            tools=tools,
            messages=messages
        )
        
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
        
        tool_calls = [b for b in response.content if b.type == "tool_use"]
        if not tool_calls:
            break
            
        messages.append({"role": "assistant", "content": response.content})
        
        tool_results = []
        for tc in tool_calls:
            print(f"  🔧 Calling {tc.name}({tc.input})")
            result = run_tool(tc.name, tc.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": result
            })
        
        messages.append({"role": "user", "content": tool_results})
    
    return "Analysis complete."

if __name__ == "__main__":
    print("=" * 60)
    print("🇮🇳 Indian Stock Analysis Agent")
    print("=" * 60)
    print("Examples:")
    print("  - Analyze TCS and give me a recommendation")
    print("  - Compare HDFC Bank vs ICICI Bank")
    print("  - Is Reliance overvalued right now?")
    print("  - Best performing Nifty 50 stocks this year")
    print("  - quit to exit")
    print("=" * 60)
    
    while True:
        query = input("\nYour question: ").strip()
        if query.lower() in ("quit", "exit", "q"):
            break
        if query:
            result = analyze(query)
            print(f"\n📊 Analysis:\n{result}")
