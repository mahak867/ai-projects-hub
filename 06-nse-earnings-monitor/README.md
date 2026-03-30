# 📊 NSE Earnings Monitor

Automatically monitor NSE earnings announcements, analyze results with Claude, and get Telegram alerts.

![Demo](https://img.shields.io/badge/difficulty-intermediate-orange?style=flat-square)

## Setup

```bash
pip install -r requirements.txt

export ANTHROPIC_API_KEY=sk-ant-...
export TELEGRAM_BOT_TOKEN=...      # from @BotFather
export TELEGRAM_CHAT_ID=...        # your chat ID
```

### Create Telegram Bot
1. Message @BotFather → `/newbot` → get token
2. Message @userinfobot → get your chat ID

## Run

```bash
# Test with 3 stocks, print results
python monitor.py --once

# Run continuously (checks every 30 min)
python monitor.py
```

## Alert format
```
🔔 NSE Earnings Alert

🟢 Infosys (INFY)
📈 ₹1,842 (+3.2%)

EPS: 21.3 vs 19.8 est.
Surprise: +7.5%

Claude Analysis:
Infosys beat estimates by 7.5%...
```

## Extend it
- Add email alerts via SendGrid
- Store history in SQLite
- Add sector-level summaries
- Web dashboard with Streamlit
