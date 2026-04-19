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

import json
import os
import sqlite3
import sys
from datetime import datetime
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
# SQLite persistence — conversations survive restarts
# ---------------------------------------------------------------------------
DB_FILE = os.environ.get("CONVERSATIONS_DB", "conversations.db")


def _get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db() -> None:
    with _get_db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS conversations (
                phone_number TEXT PRIMARY KEY,
                messages     TEXT NOT NULL,
                updated_at   TEXT NOT NULL
            )"""
        )


def _load_history(phone_number: str) -> List[Dict[str, str]]:
    with _get_db() as conn:
        row = conn.execute(
            "SELECT messages FROM conversations WHERE phone_number = ?",
            (phone_number,),
        ).fetchone()
    return json.loads(row["messages"]) if row else []


def _save_history(phone_number: str, messages: List[Dict[str, str]]) -> None:
    with _get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO conversations (phone_number, messages, updated_at) VALUES (?, ?, ?)",
            (phone_number, json.dumps(messages), datetime.utcnow().isoformat()),
        )


def _clear_history(phone_number: str) -> bool:
    with _get_db() as conn:
        affected = conn.execute(
            "DELETE FROM conversations WHERE phone_number = ?", (phone_number,)
        ).rowcount
    return affected > 0


def _count_conversations() -> int:
    with _get_db() as conn:
        return conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
_init_db()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

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

    # Build / extend conversation history (persisted in SQLite)
    history = _load_history(from_number)
    history.append({"role": "user", "content": body})
    trimmed = history[-MAX_HISTORY:]

    # Call Claude
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system=SYSTEM,
        messages=trimmed,
    )
    reply: str = response.content[0].text
    trimmed.append({"role": "assistant", "content": reply})
    _save_history(from_number, trimmed)

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
    if _clear_history(number):
        return {"status": "cleared"}
    return {"status": "not_found"}


@app.route("/health", methods=["GET"])
def health() -> Dict[str, str]:
    """Health check endpoint used by uptime monitors."""
    return {"status": "ok", "conversations_active": _count_conversations()}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("✅ WhatsApp AI Bot starting on port 5000")
    print("   Expose publicly with: ngrok http 5000")
    print("   Then set your Twilio webhook to: https://<ngrok-url>/webhook")
    app.run(debug=False, port=5000)
