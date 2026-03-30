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
