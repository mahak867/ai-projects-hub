<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=28&pause=1000&color=00B386&center=true&vCenter=true&width=700&lines=AI+Projects+Hub+%F0%9F%A4%96;20+projects+that+actually+run.;Built+with+Claude+%C2%B7+India-first.;Clone.+Install.+Ship." alt="Typing SVG" />

<br/>

<img src="https://img.shields.io/github/stars/mahak867/ai-projects-hub?style=for-the-badge&logo=github&color=00b386&labelColor=0d1117" />
<img src="https://img.shields.io/github/forks/mahak867/ai-projects-hub?style=for-the-badge&logo=github&color=0ea5e9&labelColor=0d1117" />
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0d1117" />
<img src="https://img.shields.io/badge/Built%20with-Claude%20API-D97706?style=for-the-badge&labelColor=0d1117" />
<img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge&labelColor=0d1117" />
<img src="https://img.shields.io/badge/India--first-%F0%9F%87%AE%F0%9F%87%B3-FF9933?style=for-the-badge&labelColor=0d1117" />

<br/><br/>

> I built this because most AI tutorials either don't run or teach you nothing real.  
> Every project here is something I actually wanted to use — and most are **India-first**  
> because tools like these almost always ignore ₹ and NSE.

</div>

---

## ⚡ Get running in 3 commands

```bash
git clone https://github.com/mahak867/ai-projects-hub.git
cd ai-projects-hub/01-pdf-chat-claude
pip install -r requirements.txt && streamlit run app.py
```

You need Python 3.10+ and a **free Claude API key** → [console.anthropic.com](https://console.anthropic.com)

---

## ⭐ Featured Projects

Three projects that show the full range — from a tool anyone can use in 5 minutes to India-first financial infrastructure an investor can evaluate immediately.

<table>
<tr>
<td width="33%" valign="top">

### 🏆 05 · Resume Analyzer

Upload resume + job description → match score, gap analysis, cover letter points, interview prep — in one click.

**Success metrics**
- Match score 0–100 with letter grade
- Skills gap list with actionable recommendations
- Section-by-section rewrite suggestions
- Average runtime: ~4 seconds per analysis

**Demo output**
```
Match Score: 74 / 100  (Good)
Missing skills: Kubernetes, dbt, Spark
Strengths: Python, SQL, ML pipeline design
Interview topics: System design, MLOps
```

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Structured Output](https://img.shields.io/badge/Structured_Output-D97706?style=flat)

**[→ Try it now](./05-resume-analyzer/)**

</td>
<td width="33%" valign="top">

### 🏆 14 · Build Your Own Perplexity

Live web search + Claude streaming = cited AI answers that update in real time. Two free API keys, no infrastructure.

**Success metrics**
- First token in < 1.5 seconds
- Inline citations [1] [2] [3] from real URLs
- Full conversation history
- 2,000 free searches/month (Brave free tier)

**Demo output**
```
Q: What is India's current repo rate?

RBI held repo rate at 6.5% in its April 2025
policy review [1], citing sticky core inflation.
Analysts expect a cut in Q3 FY26 [2][3].

Sources: [1] rbi.org.in  [2] economictimes.com
         [3] moneycontrol.com
```

![Brave Search](https://img.shields.io/badge/Brave_Search-FB542B?style=flat)
![Streaming](https://img.shields.io/badge/Streaming-D97706?style=flat)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit)

**[→ Try it now](./14-build-your-own-perplexity/)**

</td>
<td width="33%" valign="top">

### 🏆 17 · Open Source Screener

Self-hosted Screener.in for NSE/BSE. Filter by ROE, P/E, market cap, debt → Claude ranks picks and flags risks.

**Success metrics**
- Screens 50 stocks in < 10 seconds
- Filters: ROE, P/E, market cap, D/E ratio
- Claude AI analysis: top picks + red flags
- India-first: native ₹ and NSE/BSE symbols

**Demo output**
```
$ python screener.py --min-roe 20 --max-pe 25

✓ 6 stocks passed filters
TCS.NS    ROE 45%  PE 24  ↑12% 1Y
INFY.NS   ROE 31%  PE 23  ↑ 8% 1Y

Claude: "TCS leads on capital efficiency;
INFY trades at a discount — watch for
margin recovery in H2 FY26."
```

![NSE/BSE](https://img.shields.io/badge/NSE%2FBSE-FF9933?style=flat)
![yfinance](https://img.shields.io/badge/yfinance-green?style=flat)
![Claude AI](https://img.shields.io/badge/Claude_AI-D97706?style=flat)

**[→ Try it now](./17-open-source-screener/)**

</td>
</tr>
</table>

---

## 📦 Projects

### 🟢 Beginner — start here

<table>
<tr>
  <td width="50%">
    <h3>01 · PDF Chat with Claude</h3>
    <p>Upload any PDF, ask questions in plain English. Claude answers with exact page references — not hallucinated ones.</p>
    <p>
      <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white"/>
      <img src="https://img.shields.io/badge/PyPDF2-blue?style=flat"/>
      <img src="https://img.shields.io/badge/Claude_API-D97706?style=flat"/>
    </p>
    <a href="./01-pdf-chat-claude/"><strong>→ View project</strong></a>
  </td>
  <td width="50%">
    <h3>02 · Indian Stock Agent</h3>
    <p>Ask plain-English questions about NSE/BSE stocks. Claude fetches real data via tool use and gives structured analysis.</p>
    <p>
      <img src="https://img.shields.io/badge/yfinance-green?style=flat"/>
      <img src="https://img.shields.io/badge/NSE%2FBSE-FF9933?style=flat"/>
      <img src="https://img.shields.io/badge/Tool_Use-D97706?style=flat"/>
    </p>
    <a href="./02-indian-stock-agent/"><strong>→ View project</strong></a>
  </td>
</tr>
<tr>
  <td width="50%">
    <h3>03 · WhatsApp AI Bot</h3>
    <p>Claude on WhatsApp via Twilio. Full conversation memory per phone number. Deploy to any server.</p>
    <p>
      <img src="https://img.shields.io/badge/Twilio-F22F46?style=flat&logo=twilio&logoColor=white"/>
      <img src="https://img.shields.io/badge/Flask-000000?style=flat&logo=flask"/>
      <img src="https://img.shields.io/badge/ngrok-1F1E37?style=flat"/>
    </p>
    <a href="./03-whatsapp-ai-bot/"><strong>→ View project</strong></a>
  </td>
  <td width="50%">
    <h3>04 · YouTube Summarizer</h3>
    <p>Paste a YouTube URL → structured notes with key points, quotes, and action items. Works with auto-generated subtitles.</p>
    <p>
      <img src="https://img.shields.io/badge/yt--dlp-FF0000?style=flat&logo=youtube&logoColor=white"/>
      <img src="https://img.shields.io/badge/Claude_API-D97706?style=flat"/>
    </p>
    <a href="./04-youtube-summarizer/"><strong>→ View project</strong></a>
  </td>
</tr>
<tr>
  <td colspan="2">
    <h3>05 · Resume Analyzer</h3>
    <p>Upload resume + paste job description → match score out of 100, missing skills, section-by-section rewrite suggestions, cover letter points, and interview prep topics.</p>
    <p>
      <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white"/>
      <img src="https://img.shields.io/badge/JSON_Schema-grey?style=flat"/>
      <img src="https://img.shields.io/badge/Structured_Output-D97706?style=flat"/>
    </p>
    <a href="./05-resume-analyzer/"><strong>→ View project</strong></a>
  </td>
</tr>
</table>

---

### 🟡 Intermediate

<table>
<tr>
  <td width="50%">
    <h3>06 · NSE Earnings Monitor</h3>
    <p>Watches NSE/BSE earnings announcements, runs Claude analysis on each result, fires Telegram alerts with EPS beat/miss summary.</p>
    <p>
      <img src="https://img.shields.io/badge/Telegram_Bot-26A5E4?style=flat&logo=telegram&logoColor=white"/>
      <img src="https://img.shields.io/badge/NSE-FF9933?style=flat"/>
      <img src="https://img.shields.io/badge/schedule-grey?style=flat"/>
    </p>
    <a href="./06-nse-earnings-monitor/"><strong>→ View project</strong></a>
  </td>
  <td width="50%">
    <h3>07 · Claude MCP Financial Analyst</h3>
    <p>MCP server for Claude Desktop. Gives Claude live NSE/BSE data, stock screening, and portfolio math — usable in every conversation.</p>
    <p>
      <img src="https://img.shields.io/badge/MCP-7C3AED?style=flat"/>
      <img src="https://img.shields.io/badge/Claude_Desktop-D97706?style=flat"/>
      <img src="https://img.shields.io/badge/yfinance-green?style=flat"/>
    </p>
    <a href="./07-claude-mcp-financial-analyst/"><strong>→ View project</strong></a>
  </td>
</tr>
<tr>
  <td width="50%">
    <h3>08 · Multi-Agent Research Pipeline</h3>
    <p>Three agents in sequence: Researcher gathers data → Critic finds gaps → Writer synthesises. Better output than any single prompt.</p>
    <p>
      <img src="https://img.shields.io/badge/Multi--Agent-7C3AED?style=flat"/>
      <img src="https://img.shields.io/badge/Claude_API-D97706?style=flat"/>
    </p>
    <a href="./08-multi-agent-research/"><strong>→ View project</strong></a>
  </td>
  <td width="50%">
    <h3>09 · RAG over Annual Reports</h3>
    <p>Ingest NSE annual report PDFs, ask questions across multiple years, get answers with page-level citations.</p>
    <p>
      <img src="https://img.shields.io/badge/ChromaDB-FF6B6B?style=flat"/>
      <img src="https://img.shields.io/badge/RAG-blue?style=flat"/>
      <img src="https://img.shields.io/badge/NSE_PDFs-FF9933?style=flat"/>
    </p>
    <a href="./09-rag-annual-reports/"><strong>→ View project</strong></a>
  </td>
</tr>
<tr>
  <td width="50%">
    <h3>10 · Computer Use Demo</h3>
    <p>Working examples of Claude's computer use API — screenshot analysis, bash execution, and file editing in a safe sandbox.</p>
    <p>
      <img src="https://img.shields.io/badge/Computer_Use-0d1117?style=flat&logo=anthropic"/>
      <img src="https://img.shields.io/badge/Beta_API-D97706?style=flat"/>
    </p>
    <a href="./10-computer-use-demo/"><strong>→ View project</strong></a>
  </td>
  <td width="50%">
    <h3>11 · AI Code Reviewer</h3>
    <p>GitHub Action that reviews every PR with Claude. Posts structured feedback with severity levels. 2-minute setup on any repo.</p>
    <p>
      <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=github-actions&logoColor=white"/>
      <img src="https://img.shields.io/badge/PR_Review-grey?style=flat"/>
    </p>
    <a href="./11-ai-code-reviewer/"><strong>→ View project</strong></a>
  </td>
</tr>
<tr>
  <td colspan="2">
    <h3>12 · Voice Journal AI</h3>
    <p>Record your day as voice or text → Claude extracts mood score, wins, todos, recurring themes → saves structured JSON → 30-day trend analysis.</p>
    <p>
      <img src="https://img.shields.io/badge/Whisper-grey?style=flat&logo=openai"/>
      <img src="https://img.shields.io/badge/Structured_Extraction-D97706?style=flat"/>
    </p>
    <a href="./12-voice-journal-ai/"><strong>→ View project</strong></a>
  </td>
</tr>
</table>

---

### 🔴 Advanced

<table>
<tr>
  <td width="50%">
    <h3>13 · Claude Trading Signals</h3>
    <p>Computes RSI, MACD, Bollinger Bands with pandas → Claude interprets the pattern → BUY/SELL/HOLD with entry, stop loss, target, and R:R ratio.</p>
    <p>
      <img src="https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white"/>
      <img src="https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite"/>
      <img src="https://img.shields.io/badge/%E2%9A%A0%EF%B8%8F_Paper_Trading_Only-red?style=flat"/>
    </p>
    <a href="./13-claude-trading-signals/"><strong>→ View project</strong></a>
  </td>
  <td width="50%">
    <h3>14 · Build Your Own Perplexity</h3>
    <p>Web search (Brave API, free tier) + Claude streaming = cited AI answers that update in real time. Full conversation history.</p>
    <p>
      <img src="https://img.shields.io/badge/Brave_Search-FB542B?style=flat"/>
      <img src="https://img.shields.io/badge/Streaming-D97706?style=flat"/>
      <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit"/>
    </p>
    <a href="./14-build-your-own-perplexity/"><strong>→ View project</strong></a>
  </td>
</tr>
<tr>
  <td width="50%">
    <h3>15 · Agentic Data Analyst</h3>
    <p>Upload any CSV → Claude writes pandas analysis code tailored to your data → executes it in a sandbox → explains results in plain English.</p>
    <p>
      <img src="https://img.shields.io/badge/Code_Generation-7C3AED?style=flat"/>
      <img src="https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas"/>
      <img src="https://img.shields.io/badge/Sandbox_Execution-grey?style=flat"/>
    </p>
    <a href="./15-agentic-data-analyst/"><strong>→ View project</strong></a>
  </td>
  <td width="50%">
    <h3>16 · Real-Time News Analyst</h3>
    <p>Pulls ET, MoneyControl, Reuters, Bloomberg RSS → Claude finds cross-source themes → daily email digest with investment thesis and risk flags.</p>
    <p>
      <img src="https://img.shields.io/badge/feedparser-grey?style=flat"/>
      <img src="https://img.shields.io/badge/Email_Digest-0ea5e9?style=flat"/>
      <img src="https://img.shields.io/badge/Scheduled-green?style=flat"/>
    </p>
    <a href="./16-real-time-news-analyst/"><strong>→ View project</strong></a>
  </td>
</tr>
<tr>
  <td width="50%">
    <h3>17 · Open Source Screener</h3>
    <p>Self-hosted Screener.in replica. P&L, Balance Sheet, Cash Flow, Shareholding, Analyst Ratings. Claude AI analysis panel for Pro users.</p>
    <p>
      <img src="https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js"/>
      <img src="https://img.shields.io/badge/Finnhub-blue?style=flat"/>
      <img src="https://img.shields.io/badge/India_Markets-FF9933?style=flat"/>
    </p>
    <a href="./17-open-source-screener/"><strong>→ View project</strong></a>
  </td>
  <td width="50%">
    <h3>18 · Document Intelligence</h3>
    <p>Extract structured data from PDFs using a JSON schema. Compare multiple documents — e.g. 3 years of annual reports — side by side.</p>
    <p>
      <img src="https://img.shields.io/badge/PyMuPDF-grey?style=flat"/>
      <img src="https://img.shields.io/badge/Schema_Extraction-D97706?style=flat"/>
      <img src="https://img.shields.io/badge/Multi--doc-blue?style=flat"/>
    </p>
    <a href="./18-document-intelligence/"><strong>→ View project</strong></a>
  </td>
</tr>
<tr>
  <td width="50%">
    <h3>19 · AI Interview Coach</h3>
    <p>Mock interviews for any role and difficulty level. Every answer gets a score out of 10, a grade, specific feedback, and a sample strong answer.</p>
    <p>
      <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit"/>
      <img src="https://img.shields.io/badge/Scoring-D97706?style=flat"/>
      <img src="https://img.shields.io/badge/Session_State-grey?style=flat"/>
    </p>
    <a href="./19-ai-interview-coach/"><strong>→ View project</strong></a>
  </td>
  <td width="50%">
    <h3>20 · Context Engineering Cookbook</h3>
    <p>10 prompting patterns that work in production — structured output, self-critique loops, constitutional constraints, retrieval formatting — each with runnable code.</p>
    <p>
      <img src="https://img.shields.io/badge/Reference-7C3AED?style=flat"/>
      <img src="https://img.shields.io/badge/10_Patterns-D97706?style=flat"/>
      <img src="https://img.shields.io/badge/Runnable_Examples-green?style=flat"/>
    </p>
    <a href="./20-context-engineering-cookbook/"><strong>→ View project</strong></a>
  </td>
</tr>
</table>

---

## 🏗️ Structure

Every folder has exactly three things — no more, no less:

```
project-name/
├── main_script.py      ← working code, no stubs
├── requirements.txt    ← exact deps
└── README.md           ← setup, how it works, what to learn
```

---

## 🇮🇳 Why India-first?

Projects 02, 06, 07, 09, 13, 16, 17 are built specifically around NSE/BSE data, ₹ denominations, and Indian market structure. The majority of AI finance repos treat the US market as default and everything else as an afterthought. These don't.

---

## 🤝 Contributing

Found a bug or want to add a project? See [CONTRIBUTING.md](CONTRIBUTING.md).  
Issues tagged [`good first issue`](https://github.com/mahak867/ai-projects-hub/issues) are a good place to start.

---

<div align="center">

Built by [mahak867](https://github.com/mahak867) · MIT License

**If this saved you time, a ⭐ helps others find it**

<img src="https://img.shields.io/badge/Made%20in-India%20🇮🇳-FF9933?style=flat-square&labelColor=138808"/>

</div>
