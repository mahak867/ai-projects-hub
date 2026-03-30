# 📈 Open Source Screener

Self-hosted Indian stock screener with Claude AI analysis. Deploy with your own API keys.

![Demo](https://img.shields.io/badge/difficulty-advanced-red?style=flat-square)

This project contains the full Screener.in replica built in this repo.
See the main screener-replica project for the complete Next.js application.

## Quick deploy to Vercel
```bash
git clone https://github.com/mahak867/ai-projects-hub
cd ai-projects-hub/17-open-source-screener
npm install
vercel deploy
```

Add env vars in Vercel:
- `NEXT_PUBLIC_FINNHUB_API_KEY` — from finnhub.io
- `ANTHROPIC_API_KEY` — Claude API key

## Features
- Screener.in-style layout (P&L, Balance Sheet, Cash Flow, Ratios)
- Shareholding pattern with donut chart
- Analyst consensus ratings
- Claude AI analysis for Pro users
- Export to CSV

See [screener-replica](/screener-replica) for full source code.
