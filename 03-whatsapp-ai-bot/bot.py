"""
WhatsApp AI Bot
Claude on WhatsApp via Twilio. Full conversation memory per phone number.
"""
from typing import Dict, List
import os
import sys

import anthropic
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# Validate required environment variables at startup
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
    print("Get your key at: https://console.anthropic.com")
    sys.exit(1)

app = Flask(__name__)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# In-memory conversation store keyed by phone number (use Redis in production)
conversations: Dict[str, List[Dict[str, str]]] = {}

SYSTEM = """You are a helpful AI assistant on WhatsApp. Be concise — WhatsApp messages should be short.
Use *bold* for emphasis, keep responses under 300 words unless asked for detail.
You can help with: questions, summaries, analysis, writing, coding, math, and general knowledge."""


@app.route("/webhook", methods=["POST"])
def webhook() -> str:
    """Handle incoming WhatsApp messages from Twilio.

    Returns:
        TwiML response string
    """
    from_number: str = request.form.get("From", "")
    body: str = request.form.get("Body", "").strip()

    if not body:
        twiml = MessagingResponse()
        twiml.message("Please send a text message.")
        return str(twiml)

    if from_number not in conversations:
        conversations[from_number] = []

    conversations[from_number].append({"role": "user", "content": body})

    # Keep last 20 messages to stay within context limits
    history = conversations[from_number][-20:]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system=SYSTEM,
        messages=history,
    )

    reply: str = response.content[0].text
    conversations[from_number].append({"role": "assistant", "content": reply})

    twiml = MessagingResponse()
    twiml.message(reply)
    return str(twiml)


@app.route("/clear", methods=["POST"])
def clear() -> Dict[str, str]:
    """Clear conversation history for a phone number.

    Returns:
        Status dictionary
    """
    number: str = request.json.get("number", "")
    if number in conversations:
        del conversations[number]
    return {"status": "cleared"}


@app.route("/health", methods=["GET"])
def health() -> Dict[str, str]:
    """Health check endpoint.

    Returns:
        Status dictionary
    """
    return {"status": "ok"}


if __name__ == "__main__":
    print("WhatsApp AI Bot running on port 5000")
    print("Expose with: ngrok http 5000")
    print("Set Twilio webhook to: https://<your-ngrok-url>/webhook")
    app.run(debug=False, port=5000)
