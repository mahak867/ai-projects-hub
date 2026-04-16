# 💬 WhatsApp AI Bot

Claude on WhatsApp via the Twilio API. Full conversation memory per phone number, works on any phone without any app install on the recipient's side.

![Difficulty](https://img.shields.io/badge/difficulty-beginner-green?style=flat-square)

## How it works

```
WhatsApp user → Twilio → your Flask webhook → Claude → Twilio → WhatsApp user
```

Twilio receives incoming WhatsApp messages and forwards them to your server via HTTP POST. Your server sends them to Claude, gets a reply, and returns it to Twilio as TwiML. Twilio delivers the reply back to WhatsApp.

**Yes, this uses Twilio.** Twilio is the bridge between WhatsApp's closed API and your code. A free Twilio account includes a WhatsApp Sandbox that lets you test immediately with no approval process.

## Prerequisites

| Tool | Purpose | Cost |
|------|---------|------|
| [Anthropic API key](https://console.anthropic.com) | Run Claude | Pay per use |
| [Twilio account](https://www.twilio.com/try-twilio) | WhatsApp gateway | Free sandbox |
| [ngrok](https://ngrok.com/download) | Expose localhost | Free tier |

## Setup (5 minutes)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and add your keys
```

Your `.env` should look like:
```
ANTHROPIC_API_KEY=sk-ant-...
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
```

### 3. Run the bot
```bash
python bot.py
```

### 4. Expose it publicly
```bash
# In a new terminal:
ngrok http 5000
# Copy the https://xxxx.ngrok.io URL
```

### 5. Connect Twilio

1. Go to [Twilio Console → Messaging → WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)
2. Set the **"When a message comes in"** webhook to:
   ```
   https://your-ngrok-url.ngrok.io/webhook
   ```
3. Send `join <your-sandbox-word>` from WhatsApp to the Twilio number shown
4. Start chatting!

## API endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhook` | POST | Twilio posts incoming messages here |
| `/health` | GET | Uptime check |
| `/clear` | POST | Reset a conversation: `{"number": "whatsapp:+91..."}` |

## Production deployment

- **Persistence:** Replace the in-memory dict with Redis so conversations survive restarts
- **Hosting:** Deploy to [Railway](https://railway.app) or [Fly.io](https://fly.io) for 24/7 uptime (no ngrok needed)
- **Rate limiting:** Add per-number limits to prevent abuse
- **Production Twilio:** Apply for a real WhatsApp Business number through Twilio to remove sandbox restrictions
