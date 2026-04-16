"""
Open Source Screener
Self-hosted Indian stock screener with Claude AI analysis.
Screen NSE/BSE stocks by fundamentals and get AI-powered insights.
"""
from typing import Any, Dict, List, Optional
import json
import os
import sys

import anthropic
import yfinance as yf

# Validate API key at startup
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
    print("Get your key at: https://console.anthropic.com")
    print("Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
    sys.exit(1)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Default Nifty 50 watchlist
NIFTY50 = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "WIPRO.NS", "BAJFINANCE.NS", "AXISBANK.NS", "TATAMOTORS.NS",
    "MARUTI.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "TITAN.NS", "NESTLEIND.NS",
    "POWERGRID.NS", "NTPC.NS", "COALINDIA.NS", "ONGC.NS", "SBIN.NS",
]


def fetch_stock_data(symbol: str) -> Dict[str, Any]:
    """Fetch comprehensive stock data for screening.

    Args:
        symbol: Yahoo Finance symbol (e.g. TCS.NS)

    Returns:
        Dictionary with price, fundamentals, and financial ratios
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="1y")

        if hist.empty:
            return {"symbol": symbol, "error": "No price data available"}

        current_price = float(hist["Close"].iloc[-1])
        year_start = float(hist["Close"].iloc[0])
        yearly_return = ((current_price - year_start) / year_start) * 100

        return {
            "symbol": symbol,
            "name": info.get("longName", symbol),
            "sector": info.get("sector", "Unknown"),
            "industry": info.get("industry", "Unknown"),
            "current_price": round(current_price, 2),
            "yearly_return_pct": round(yearly_return, 2),
            "market_cap_cr": round((info.get("marketCap") or 0) / 1e7, 0),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "pb_ratio": info.get("priceToBook"),
            "ps_ratio": info.get("priceToSalesTrailing12Months"),
            "roe_pct": round((info.get("returnOnEquity") or 0) * 100, 2),
            "roa_pct": round((info.get("returnOnAssets") or 0) * 100, 2),
            "profit_margin_pct": round((info.get("profitMargins") or 0) * 100, 2),
            "revenue_growth_pct": round((info.get("revenueGrowth") or 0) * 100, 2),
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "dividend_yield_pct": round((info.get("dividendYield") or 0) * 100, 2),
            "eps": info.get("trailingEps"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "analyst_recommendation": info.get("recommendationKey", "none"),
            "target_price": info.get("targetMeanPrice"),
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}


def screen_stocks(
    symbols: List[str],
    min_roe: float = 0.0,
    max_pe: float = float("inf"),
    min_market_cap_cr: float = 0.0,
    max_debt_to_equity: float = float("inf"),
    min_profit_margin: float = -float("inf"),
) -> List[Dict[str, Any]]:
    """Screen stocks by fundamental criteria.

    Args:
        symbols: List of Yahoo Finance symbols to screen
        min_roe: Minimum return on equity (%)
        max_pe: Maximum trailing P/E ratio
        min_market_cap_cr: Minimum market cap in Crores
        max_debt_to_equity: Maximum debt-to-equity ratio
        min_profit_margin: Minimum profit margin (%)

    Returns:
        Filtered and sorted list of stock data dictionaries
    """
    results = []
    total = len(symbols)

    for i, symbol in enumerate(symbols, 1):
        print(f"  [{i}/{total}] Fetching {symbol}...", end="\r")
        data = fetch_stock_data(symbol)

        if "error" in data:
            continue

        # Apply filters
        pe = data.get("pe_ratio") or float("inf")
        roe = data.get("roe_pct") or 0
        cap = data.get("market_cap_cr") or 0
        d2e = data.get("debt_to_equity") or 0
        margin = data.get("profit_margin_pct") or 0

        if (
            roe >= min_roe
            and pe <= max_pe
            and cap >= min_market_cap_cr
            and d2e <= max_debt_to_equity
            and margin >= min_profit_margin
        ):
            results.append(data)

    print()  # newline after progress
    results.sort(key=lambda x: x.get("roe_pct") or 0, reverse=True)
    return results


def ai_analysis(stocks: List[Dict[str, Any]], context: str = "") -> str:
    """Run Claude AI analysis on a list of screened stocks.

    Args:
        stocks: List of stock data dictionaries from screen_stocks()
        context: Optional additional context for the analysis

    Returns:
        Claude's analysis as a string
    """
    if not stocks:
        return "No stocks to analyze."

    # Trim to top 15 to stay within token limits
    top_stocks = stocks[:15]

    prompt = f"""You are an expert Indian equity analyst. Analyze these screened NSE stocks and provide insights.

{f"Context: {context}" if context else ""}

SCREENED STOCKS (sorted by ROE):
{json.dumps(top_stocks, indent=2, default=str)}

Provide:
1. **Top 3 Picks** — best risk/reward among these stocks with reasoning
2. **Sector Trends** — what sectors are well-represented and why
3. **Valuation Summary** — which stocks look cheap vs expensive
4. **Red Flags** — any concerns in the data
5. **One-liner** on each stock

Keep analysis data-driven and specific. Mention actual P/E, ROE numbers."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def print_table(stocks: List[Dict[str, Any]]) -> None:
    """Print a formatted table of screened stocks.

    Args:
        stocks: List of stock data dictionaries
    """
    if not stocks:
        print("No stocks match the criteria.")
        return

    print(f"\n{'Symbol':<16} {'Name':<30} {'Price':>8} {'ROE%':>7} {'P/E':>7} {'MarCap Cr':>12} {'1Y Ret%':>9}")
    print("-" * 95)
    for s in stocks:
        pe = f"{s['pe_ratio']:.1f}" if s.get("pe_ratio") else "N/A"
        print(
            f"{s['symbol']:<16} "
            f"{(s.get('name') or s['symbol'])[:29]:<30} "
            f"{s.get('current_price', 0):>8.2f} "
            f"{s.get('roe_pct', 0):>7.1f} "
            f"{pe:>7} "
            f"{s.get('market_cap_cr', 0):>12,.0f} "
            f"{s.get('yearly_return_pct', 0):>9.1f}"
        )


def main() -> None:
    """Interactive CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Open Source NSE Stock Screener with Claude AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python screener.py                                    # Screen Nifty50 with defaults
  python screener.py --min-roe 15 --max-pe 25          # Quality screen
  python screener.py --symbols TCS.NS INFY.NS WIPRO.NS # Specific stocks
  python screener.py --min-roe 20 --no-ai              # Screen only, skip AI
        """,
    )
    parser.add_argument("--symbols", nargs="*", default=NIFTY50, help="Symbols to screen")
    parser.add_argument("--min-roe", type=float, default=10.0, help="Min ROE %% (default: 10)")
    parser.add_argument("--max-pe", type=float, default=50.0, help="Max P/E ratio (default: 50)")
    parser.add_argument("--min-cap", type=float, default=5000.0, help="Min market cap Cr (default: 5000)")
    parser.add_argument("--max-de", type=float, default=3.0, help="Max debt/equity (default: 3)")
    parser.add_argument("--no-ai", action="store_true", help="Skip Claude AI analysis")
    parser.add_argument("--output", help="Save results to JSON file")
    args = parser.parse_args()

    print("=" * 60)
    print("📈 Open Source NSE Screener")
    print("=" * 60)
    print(f"Screening {len(args.symbols)} stocks with filters:")
    print(f"  Min ROE: {args.min_roe}% | Max P/E: {args.max_pe} | Min Cap: ₹{args.min_cap:,.0f} Cr")
    print()

    results = screen_stocks(
        symbols=args.symbols,
        min_roe=args.min_roe,
        max_pe=args.max_pe,
        min_market_cap_cr=args.min_cap,
        max_debt_to_equity=args.max_de,
    )

    print(f"\n✓ {len(results)} stocks passed filters")
    print_table(results)

    if not args.no_ai and results:
        print("\n🤖 Claude AI Analysis:\n")
        analysis = ai_analysis(results)
        print(analysis)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to {args.output}")


if __name__ == "__main__":
    main()
