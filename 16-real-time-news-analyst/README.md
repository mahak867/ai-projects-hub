# 📰 Real-Time News Analyst

Stream RSS feeds from ET, MoneyControl, Reuters → Claude extracts themes → sends daily email digest.

![Demo](https://img.shields.io/badge/difficulty-advanced-red?style=flat-square)

## Setup
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
export SMTP_USER=your@gmail.com      # optional for email
export SMTP_PASS=your-app-password
export DIGEST_EMAIL=recipient@email.com
```

## Usage
```bash
python analyst.py            # Run once, print results
python analyst.py --schedule # Run daily at 7 AM
```

## Output includes
- Market sentiment score (-100 to +100)
- Top themes across all sources
- Key events with sector impact
- Investment thesis
- Risks and opportunities

## Key concept: Multi-source synthesis
Claude doesn't just summarize individual articles — it synthesizes patterns across 30+ articles from 5+ sources to extract what actually matters for investors.

## ⚠️ Known Limitations
- **RSS feed stability**: Feed URLs for ET, MoneyControl, and other sources may change; broken feeds are skipped silently
- **Paywalled content**: Only the headline and RSS snippet are analysed for paywalled articles — full article text is not available
- **Email setup required**: The daily digest email requires SMTP credentials (Gmail app password or similar); defaults to console output only
- **Scheduling**: The built-in scheduler (`--schedule`) blocks the terminal; for always-on operation use a cron job or systemd service

## 🧪 Testing & Linting

```bash
# Install linter
pip install ruff

# Check for style and correctness issues
ruff check .

# Verify all dependencies install correctly
pip install -r requirements.txt

# Smoke test — confirm imports load without error
python -c "import anthropic, feedparser; print('All dependencies OK')"

# Run once (no email sent, prints to console)
python analyst.py
```
