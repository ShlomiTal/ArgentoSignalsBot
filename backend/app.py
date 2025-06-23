import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils.data import get_price
from utils.telegram import send_message
from utils.backtest import run_backtest
from ai import generate_signal, learn_from_performance
import json
import datetime

load_dotenv()
app = Flask(__name__)

# Load settings.json
with open("backend/settings.json", "r") as f:
    SETTINGS = json.load(f)

@app.route("/")
def home():
    return "✅ Argento AI is running."

@app.route("/signal")
def signal():
    symbol = request.args.get("symbol", "BTC/USD")
    try:
        signal, confidence, price = generate_signal(symbol)
        response = {
            "symbol": symbol,
            "signal": signal,
            "confidence": confidence,
            "price": price
        }

        if confidence >= SETTINGS["confidence_threshold"]:
            msg = f"📊 Signal for {symbol}: {signal} at ${price:.2f} (Confidence: {confidence}%)"
            send_message(msg)

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/backtest")
def backtest():
    symbol = request.args.get("symbol", "BTC/USD")
    try:
        result = run_backtest(symbol)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/learn")
def learn():
    symbol = request.args.get("symbol", "BTC/USD")
    try:
        result = learn_from_performance(symbol)
        return jsonify({"symbol": symbol, "learning": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/custom-message", methods=["POST"])
def custom_message():
    data = request.json
    message = data.get("message")
    image_url = data.get("image_url")
    target_chat = data.get("chat_id", os.getenv("CHAT_ID"))

    if not message:
        return jsonify({"error": "Missing message"}), 400

    send_message(message, image_url=image_url, chat_id=target_chat)
    return jsonify({"status": "sent", "to": target_chat})

@app.route("/market-open")
def market_open():
    region = request.args.get("region", "us").lower()
    key = f"market_open_{region}"
    if key in SETTINGS:
        send_message(SETTINGS[key])
        return jsonify({"status": "sent", "message": SETTINGS[key]})
    return jsonify({"error": "Region not supported"}), 400

@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": datetime.datetime.utcnow().isoformat()})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
