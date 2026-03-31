<div align="center">

# AI Projects Hub

**20 AI projects that actually run. No fluff, no fake demos.**

[![Stars](https://img.shields.io/github/stars/mahak867/ai-projects-hub?style=flat-square)](https://github.com/mahak867/ai-projects-hub/stargazers)
[![Forks](https://img.shields.io/github/forks/mahak867/ai-projects-hub?style=flat-square)](https://github.com/mahak867/ai-projects-hub/forks)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

</div>

---

I built this because I kept finding AI tutorials with code that either doesn't run or teaches you nothing useful. Every project here is something I actually wanted to use â€” most of them are India-first because tools like these almost always ignore â‚¹ and NSE.

You need a [free Claude API key](https://console.anthropic.com) for most projects. Each one runs in under 5 minutes.

---

## Projects

### Beginner

| # | Project | What it does |
|---|---------|-------------|
| 01 | [pdf-chat-claude](./01-pdf-chat-claude/) | Chat with any PDF. Claude answers with exact page references. |
| 02 | [indian-stock-agent](./02-indian-stock-agent/) | Ask plain-English questions about NSE/BSE stocks. Claude fetches real data and gives analysis. |
| 03 | [whatsapp-ai-bot](./03-whatsapp-ai-bot/) | Claude on WhatsApp via Twilio. Full conversation memory per number. |
| 04 | [youtube-summarizer](./04-youtube-summarizer/) | Paste a YouTube URL, get structured notes with key points and quotes. |
| 05 | [resume-analyzer](./05-resume-analyzer/) | Upload resume + paste JD â†’ match score, gaps, and rewrite suggestions. |

### Intermediate

| # | Project | What it does |
|---|---------|-------------|
| 06 | [nse-earnings-monitor](./06-nse-earnings-monitor/) | Watches NSE earnings, runs Claude analysis, sends Telegram alerts. |
| 07 | [claude-mcp-financial-analyst](./07-claude-mcp-financial-analyst/) | MCP server for Claude Desktop â€” gives it live NSE/BSE data, screening, portfolio math. |
| 08 | [multi-agent-research](./08-multi-agent-research/) | Three Claude agents: Researcher â†’ Critic â†’ Writer. Better output than any single prompt. |
| 09 | [rag-annual-reports](./09-rag-annual-reports/) | Ingest NSE annual report PDFs, ask questions, get answers with page citations. |
| 10 | [computer-use-demo](./10-computer-use-demo/) | Working Claude computer use examples â€” screenshot, bash, file editing. |
| 11 | [ai-code-reviewer](./11-ai-code-reviewer/) | GitHub Action that reviews every PR with Claude. Add it to any repo in 2 minutes. |
| 12 | [voice-journal-ai](./12-voice-journal-ai/) | Record your day â†’ Claude extracts mood, wins, todos, themes â†’ saves to JSON. |

### Advanced

| # | Project | What it does |
|---|---------|-------------|
| 13 | [claude-trading-signals](./13-claude-trading-signals/) | RSI, MACD, Bollinger â†’ Claude interprets â†’ BUY/SELL/HOLD with entry, SL, target. Paper trading only. |
| 14 | [build-your-own-perplexity](./14-build-your-own-perplexity/) | Web search + Claude streaming = AI answers with citations. Needs Brave Search API (free). |
| 15 | [agentic-data-analyst](./15-agentic-data-analyst/) | Upload any CSV â†’ Claude writes analysis code â†’ executes it â†’ explains results. |
| 16 | [real-time-news-analyst](./16-real-time-news-analyst/) | Pulls ET, MoneyControl, Reuters RSS â†’ Claude finds themes â†’ daily email digest. |
| 17 | [open-source-screener](./17-open-source-screener/) | Self-hosted Screener.in replica with Claude AI analysis. Deploy with your own keys. |
| 18 | [document-intelligence](./18-document-intelligence/) | Extract structured data from PDFs and compare multiple documents side by side. |
| 19 | [ai-interview-coach](./19-ai-interview-coach/) | Mock interviews with scoring. Claude rates every answer and shows you a better version. |
| 20 | [context-engineering-cookbook](./20-context-engineering-cookbook/) | 10 prompting patterns that work in production, with runnable code for each. |

---

## Getting started

```bash
git clone https://github.com/mahak867/ai-projects-hub.git
cd ai-projects-hub/01-pdf-chat-claude   # or any project
pip install -r requirements.txt
# follow the README in that folder
```

You need Python 3.10+ and a Claude API key from [console.anthropic.com](https://console.anthropic.com).

---

## What each folder has

Every project has three things:
- The working code (no stubs, no pseudocode)
- A `requirements.txt`
- A README explaining setup, how it works, and what to learn from it

---

## Contributing

Found a bug, want to add a project, or improve an existing one? See [CONTRIBUTING.md](CONTRIBUTING.md). PRs are open.

Issues tagged [`good first issue`](https://github.com/mahak867/ai-projects-hub/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) are a good place to start.

---

## Disclaimer

Projects 13 (trading signals) is for paper trading and learning only. Not financial advice.

---

MIT License Â· Built by [mahak867](https://github.com/mahak867)
