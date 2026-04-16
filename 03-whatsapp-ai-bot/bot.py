"""
WhatsApp AI Bot
Claude on WhatsApp via Twilio. Full conversation memory per phone number.

Prerequisites:
  - Free Twilio account: https://www.twilio.com/try-twilio
  - Twilio WhatsApp Sandbox (no approval needed for testing)
  - ngrok to expose your local server: https://ngrok.com

Quick start:
  pip install -r requirements.txt
  cp .env.example .env   # fill in your keys
  python bot.py
  ngrok http 5000        # copy the https URL to Twilio webhook
"""
from __future__ import annotations

import os
import sys
from typing import Dict, List

import anthropic
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# ---------------------------------------------------------------------------
# Startup validation — fail loudly so users know exactly what's missing
# ---------------------------------------------------------------------------
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print(
        "❌ ANTHROPIC_API_KEY not set.\n"
        "   Fix: add it to your .env file (see .env.example)\n"
        "   Get a key: https://console.anthropic.com",
        file=sys.stderr,
    )
    sys.exit(1)

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
    print(
        "❌ TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN not set.\n"
        "   Fix: add them to your .env file (see .env.example)\n"
        "   Get credentials: https://console.twilio.com",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = Flask(__name__)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# In-memory store keyed by phone number.
# Replace with Redis for production multi-process deployments.
conversations: Dict[str, List[Dict[str, str]]] = {}

SYSTEM = (
    "You are a helpful AI assistant on WhatsApp. "
    "Be concise — WhatsApp messages should be short. "
    "Use *bold* for emphasis, keep responses under 300 words unless asked for detail. "
    "You can help with: questions, summaries, analysis, writing, coding, math, and general knowledge."
)

MAX_HISTORY = 20  # messages to keep per conversation


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/webhook", methods=["POST"])
def webhook() -> str:
    """Receive an incoming WhatsApp message from Twilio and reply via Claude.

    Twilio POSTs form data with at minimum:
      - From: the sender's WhatsApp number (whatsapp:+91xxxxxxxxxx)
      - Body: the message text

    Returns:
        TwiML XML string that Twilio uses to send the reply.
    """
    from_number: str = request.form.get("From", "")
    body: str = request.form.get("Body", "").strip()

    twiml = MessagingResponse()

    if not body:
        twiml.message("Please send a text message.")
        return str(twiml)

    # Build / extend conversation history
    if from_number not in conversations:
        conversations[from_number] = []
    conversations[from_number].append({"role": "user", "content": body})
    history = conversations[from_number][-MAX_HISTORY:]

    # Call Claude
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system=SYSTEM,
        messages=history,
    )
    reply: str = response.content[0].text
    conversations[from_number].append({"role": "assistant", "content": reply})

    twiml.message(reply)
    return str(twiml)


@app.route("/clear", methods=["POST"])
def clear() -> Dict[str, str]:
    """Clear conversation history for a given phone number.

    Expects JSON body: {"number": "whatsapp:+91xxxxxxxxxx"}

    Returns:
        {"status": "cleared"} or {"status": "not_found"}
    """
    number: str = (request.json or {}).get("number", "")
    if number in conversations:
        del conversations[number]
        return {"status": "cleared"}
    return {"status": "not_found"}


@app.route("/health", methods=["GET"])
def health() -> Dict[str, str]:
    """Health check endpoint used by uptime monitors."""
    return {"status": "ok", "conversations_active": len(conversations)}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("✅ WhatsApp AI Bot starting on port 5000")
    print("   Expose publicly with: ngrok http 5000")
    print("   Then set your Twilio webhook to: https://<ngrok-url>/webhook")
    app.run(debug=False, port=5000)
