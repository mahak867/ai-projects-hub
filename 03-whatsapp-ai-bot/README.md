# 💬 WhatsApp AI Bot

Connect Claude to WhatsApp. Real conversations, full memory, works on any phone.

![Demo](https://img.shields.io/badge/difficulty-beginner-green?style=flat-square)

## Setup

### 1. Install & configure
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
export TWILIO_ACCOUNT_SID=...
export TWILIO_AUTH_TOKEN=...
```

### 2. Run & expose
```bash
python bot.py
# In another terminal:
ngrok http 5000
```

### 3. Connect Twilio
- Go to Twilio Console → WhatsApp Sandbox
- Set webhook URL to: `https://your-ngrok-url.ngrok.io/webhook`
- Send "join [your-sandbox-word]" from WhatsApp

## How it works
- Twilio receives WhatsApp messages and POSTs them to your Flask webhook
- Flask passes the conversation history to Claude
- Claude's response goes back through Twilio to WhatsApp
- Each phone number gets its own conversation thread

## Production tips
- Replace in-memory dict with Redis for persistence
- Add rate limiting per number
- Deploy to Railway or Fly.io for 24/7 uptime
- Add command parsing (e.g., "!clear" to reset conversation)
