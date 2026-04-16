"""
Indian Stock Analysis Agent
Ask plain-English questions about NSE/BSE stocks.
Claude fetches real data via tool use and gives structured analysis.
"""
from typing import Any, Dict, List
import anthropic
import yfinance as yf
import json
import os
import re
import sys
from datetime import datetime

# Validate API key at startup
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
    print("Get your key at: https://console.anthropic.com")
    print("Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
    sys.exit(1)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

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


def validate_symbol(symbol: str) -> str:
    """Validate and normalise a Yahoo Finance symbol.

    Args:
        symbol: Raw symbol string

    Returns:
        Uppercased symbol

    Raises:
        ValueError: If symbol format is invalid
    """
    symbol = symbol.strip().upper()
    if not re.match(r"^[A-Z0-9^]+(\.(NS|BO|L|AX))?$", symbol):
        raise ValueError(
            f"Invalid symbol: '{symbol}'. "
            "Expected format: RELIANCE.NS (NSE) or RELIANCE.BO (BSE)"
        )
    return symbol


def get_stock_quote(symbol: str) -> Dict[str, Any]:
    """Fetch current quote for a single stock.

    Args:
        symbol: Yahoo Finance symbol (e.g. TCS.NS)

    Returns:
        Dictionary with price, change, volume and 52-week range
    """
    try:
        symbol = validate_symbol(symbol)
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="2d")
        current = float(hist["Close"].iloc[-1])
        prev = float(hist["Close"].iloc[-2]) if len(hist) > 1 else current
        change = current - prev
        change_pct = (change / prev) * 100 if prev else 0
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
    except ValueError as e:
        return {"error": str(e), "symbol": symbol}
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


def get_historical_data(symbol: str, period: str) -> Dict[str, Any]:
    """Fetch historical OHLCV data and compute return statistics.

    Args:
        symbol: Yahoo Finance symbol
        period: One of 1mo, 3mo, 6mo, 1y, 2y, 5y

    Returns:
        Dictionary with return, high, low and average volume
    """
    try:
        symbol = validate_symbol(symbol)
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        if hist.empty:
            return {"error": "No data found", "symbol": symbol}
        start_price = float(hist["Close"].iloc[0])
        end_price = float(hist["Close"].iloc[-1])
        returns = ((end_price - start_price) / start_price) * 100
        return {
            "symbol": symbol,
            "period": period,
            "start_price": round(start_price, 2),
            "end_price": round(end_price, 2),
            "return_pct": round(returns, 2),
            "period_high": round(float(hist["High"].max()), 2),
            "period_low": round(float(hist["Low"].min()), 2),
            "avg_volume": round(float(hist["Volume"].mean()), 0),
        }
    except ValueError as e:
        return {"error": str(e), "symbol": symbol}
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


def get_fundamentals(symbol: str) -> Dict[str, Any]:
    """Fetch fundamental ratios and financial metrics.

    Args:
        symbol: Yahoo Finance symbol

    Returns:
        Dictionary with P/E, ROE, margins, debt ratios and more
    """
    try:
        symbol = validate_symbol(symbol)
        info = yf.Ticker(symbol).info
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
    except ValueError as e:
        return {"error": str(e), "symbol": symbol}
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


def compare_stocks(symbols: List[str]) -> Dict[str, Any]:
    """Compare multiple stocks side by side.

    Args:
        symbols: List of Yahoo Finance symbols

    Returns:
        Dictionary with a 'comparison' list of merged quote + fundamental data
    """
    results = []
    for sym in symbols:
        quote = get_stock_quote(sym)
        fund = get_fundamentals(sym)
        hist = get_historical_data(sym, "1y")
        results.append({**quote, **fund, "1y_return": hist.get("return_pct")})
    return {"comparison": results}


def run_tool(name: str, inputs: Dict[str, Any]) -> str:
    """Dispatch a tool call and return JSON-encoded result.

    Args:
        name: Tool name
        inputs: Tool input parameters

    Returns:
        JSON string with tool result
    """
    tool_map = {
        "get_stock_quote": get_stock_quote,
        "get_historical_data": get_historical_data,
        "get_fundamentals": get_fundamentals,
        "compare_stocks": compare_stocks,
    }
    func = tool_map.get(name)
    if func is None:
        return json.dumps({"error": f"Unknown tool: {name}"})
    return json.dumps(func(**inputs))


def analyze(query: str) -> str:
    """Run the agentic analysis loop for a user query.

    Args:
        query: Natural-language question about Indian stocks

    Returns:
        Final text response from Claude
    """
    print(f"\n🔍 Analyzing: {query}\n")

    messages: List[Dict[str, Any]] = [{"role": "user", "content": query}]

    system = """You are an expert Indian stock market analyst with access to real-time NSE/BSE data.

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


def main() -> None:
    """Interactive CLI entry point."""
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


if __name__ == "__main__":
    main()
