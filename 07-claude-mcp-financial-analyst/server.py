"""
MCP Server: Financial Analyst
Connect this to Claude Desktop to get financial analysis tools inside Claude.

Install: pip install mcp yfinance anthropic pandas
Run: python server.py
Add to Claude Desktop config (see README)
"""
import asyncio
import json
import yfinance as yf
import pandas as pd
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp import types

server = Server("financial-analyst")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_stock_data",
            description="Get comprehensive stock data for any symbol (NSE: add .NS, BSE: add .BO)",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol e.g. TCS.NS, AAPL, RELIANCE.NS"},
                    "period": {"type": "string", "default": "1y", "description": "Period: 1d 5d 1mo 3mo 6mo 1y 2y 5y"}
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="screen_stocks",
            description="Screen NSE stocks by criteria like P/E, ROE, market cap",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbols": {"type": "array", "items": {"type": "string"}, "description": "List of symbols to screen"},
                    "min_roe": {"type": "number", "description": "Minimum ROE %"},
                    "max_pe": {"type": "number", "description": "Maximum P/E ratio"},
                    "min_market_cap_cr": {"type": "number", "description": "Minimum market cap in Crores"}
                },
                "required": ["symbols"]
            }
        ),
        types.Tool(
            name="calculate_returns",
            description="Calculate portfolio returns and risk metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbols": {"type": "array", "items": {"type": "string"}},
                    "weights": {"type": "array", "items": {"type": "number"}, "description": "Portfolio weights (must sum to 1)"},
                    "period": {"type": "string", "default": "1y"}
                },
                "required": ["symbols"]
            }
        ),
        types.Tool(
            name="get_sector_performance",
            description="Get performance of major NSE sector indices",
            inputSchema={
                "type": "object",
                "properties": {
                    "period": {"type": "string", "default": "1mo"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        if name == "get_stock_data":
            symbol = arguments["symbol"]
            period = arguments.get("period", "1y")
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period=period)
            
            if hist.empty:
                return [types.TextContent(type="text", text=f"No data found for {symbol}")]
            
            returns = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100)
            volatility = hist['Close'].pct_change().std() * (252 ** 0.5) * 100
            
            data = {
                "symbol": symbol,
                "name": info.get("longName", symbol),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "current_price": round(float(hist['Close'].iloc[-1]), 2),
                "period_return_pct": round(float(returns), 2),
                "annual_volatility_pct": round(float(volatility), 2),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "pb_ratio": info.get("priceToBook"),
                "roe_pct": round(info.get("returnOnEquity", 0) * 100, 2) if info.get("returnOnEquity") else None,
                "roa_pct": round(info.get("returnOnAssets", 0) * 100, 2) if info.get("returnOnAssets") else None,
                "profit_margin_pct": round(info.get("profitMargins", 0) * 100, 2) if info.get("profitMargins") else None,
                "revenue_growth_pct": round(info.get("revenueGrowth", 0) * 100, 2) if info.get("revenueGrowth") else None,
                "market_cap_cr": round(info.get("marketCap", 0) / 1e7, 0),
                "52w_high": info.get("fiftyTwoWeekHigh"),
                "52w_low": info.get("fiftyTwoWeekLow"),
                "dividend_yield_pct": round(info.get("dividendYield", 0) * 100, 2) if info.get("dividendYield") else 0,
                "debt_to_equity": info.get("debtToEquity"),
                "current_ratio": info.get("currentRatio"),
                "analyst_recommendation": info.get("recommendationKey"),
                "target_price": info.get("targetMeanPrice"),
            }
            return [types.TextContent(type="text", text=json.dumps(data, indent=2))]
        
        elif name == "screen_stocks":
            symbols = arguments["symbols"]
            min_roe = arguments.get("min_roe", 0)
            max_pe = arguments.get("max_pe", float("inf"))
            min_cap = arguments.get("min_market_cap_cr", 0)
            
            results = []
            for sym in symbols:
                try:
                    info = yf.Ticker(sym).info
                    roe = (info.get("returnOnEquity", 0) or 0) * 100
                    pe = info.get("trailingPE") or float("inf")
                    cap = (info.get("marketCap", 0) or 0) / 1e7
                    
                    if roe >= min_roe and pe <= max_pe and cap >= min_cap:
                        results.append({
                            "symbol": sym,
                            "name": info.get("longName", sym),
                            "roe_pct": round(roe, 2),
                            "pe": round(pe, 2) if pe != float("inf") else None,
                            "market_cap_cr": round(cap, 0),
                            "recommendation": info.get("recommendationKey"),
                        })
                except Exception:
                    pass
            
            results.sort(key=lambda x: x.get("roe_pct", 0), reverse=True)
            return [types.TextContent(type="text", text=json.dumps({"screened": results, "count": len(results)}, indent=2))]
        
        elif name == "calculate_returns":
            symbols = arguments["symbols"]
            weights = arguments.get("weights", [1/len(symbols)] * len(symbols))
            period = arguments.get("period", "1y")
            
            prices = {}
            for sym in symbols:
                hist = yf.Ticker(sym).history(period=period)
                if not hist.empty:
                    prices[sym] = hist['Close']
            
            df = pd.DataFrame(prices).dropna()
            returns_df = df.pct_change().dropna()
            
            individual = {}
            for sym in symbols:
                if sym in df.columns:
                    total_return = ((df[sym].iloc[-1] - df[sym].iloc[0]) / df[sym].iloc[0] * 100)
                    vol = returns_df[sym].std() * (252**0.5) * 100
                    individual[sym] = {"return_pct": round(float(total_return), 2), "volatility_pct": round(float(vol), 2)}
            
            if len(weights) == len(symbols) and sum(weights) > 0.99:
                port_returns = returns_df[list(prices.keys())] @ weights[:len(prices)]
                port_total = ((1 + port_returns).prod() - 1) * 100
                port_vol = port_returns.std() * (252**0.5) * 100
                sharpe = (port_returns.mean() * 252) / (port_returns.std() * (252**0.5)) if port_returns.std() > 0 else 0
                
                portfolio = {
                    "total_return_pct": round(float(port_total), 2),
                    "annual_volatility_pct": round(float(port_vol), 2),
                    "sharpe_ratio": round(float(sharpe), 3),
                }
            else:
                portfolio = {"error": "Weights must sum to 1 and match symbol count"}
            
            return [types.TextContent(type="text", text=json.dumps({"portfolio": portfolio, "individual": individual}, indent=2))]
        
        elif name == "get_sector_performance":
            period = arguments.get("period", "1mo")
            sectors = {
                "Nifty 50": "^NSEI",
                "Nifty Bank": "^NSEBANK",
                "Nifty IT": "^CNXIT",
                "Nifty Pharma": "^CNXPHARMA",
                "Nifty Auto": "^CNXAUTO",
                "Nifty FMCG": "^CNXFMCG",
                "Nifty Metal": "^CNXMETAL",
                "Nifty Realty": "^CNXREALTY",
            }
            results = {}
            for name_s, sym in sectors.items():
                try:
                    hist = yf.Ticker(sym).history(period=period)
                    if not hist.empty:
                        ret = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100)
                        results[name_s] = round(float(ret), 2)
                except Exception:
                    pass
            
            sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
            return [types.TextContent(type="text", text=json.dumps(sorted_results, indent=2))]
        
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(
            server_name="financial-analyst",
            server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=None,
                experimental_capabilities={}
            )
        ))

if __name__ == "__main__":
    asyncio.run(main())
