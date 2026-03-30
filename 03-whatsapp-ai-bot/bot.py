from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import anthropic
import os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# In-memory conversation store (use Redis in production)
conversations: dict[str, list] = {}

SYSTEM = """You are a helpful AI assistant on WhatsApp. Be concise — WhatsApp messages should be short.
Use *bold* for emphasis, keep responses under 300 words unless asked for detail.
You can help with: questions, summaries, analysis, writing, coding, math, and general knowledge."""

@app.route("/webhook", methods=["POST"])
def webhook():
    from_number = request.form.get("From", "")
    body = request.form.get("Body", "").strip()
    
    if from_number not in conversations:
        conversations[from_number] = []
    
    conversations[from_number].append({"role": "user", "content": body})
    
    # Keep last 20 messages to stay within context
    history = conversations[from_number][-20:]
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system=SYSTEM,
        messages=history
    )
    
    reply = response.content[0].text
    conversations[from_number].append({"role": "assistant", "content": reply})
    
    twiml = MessagingResponse()
    twiml.message(reply)
    return str(twiml)

@app.route("/clear", methods=["POST"])
def clear():
    number = request.json.get("number")
    if number in conversations:
        del conversations[number]
    return {"status": "cleared"}

if __name__ == "__main__":
    print("WhatsApp AI Bot running on port 5000")
    print("Expose with: ngrok http 5000")
    app.run(debug=True, port=5000)
