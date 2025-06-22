import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

last_sent = {}

def send_telegram_message(text):
    try:
        if not TELEGRAM_TOKEN or not CHAT_ID:
            print("Telegram: Missing Telegram credentials.")
            return
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": text}
        response = requests.post(url, data=data)
        print("Telegram response:", response.text)
    except Exception as e:
        print("Telegram Error:", e)

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_DATA_API_KEY}"
        response = requests.get(url)
        return float(response.json()["price"])
    except Exception as e:
        print(f"[Price Error] {symbol}:", e)
        return None

def generate_signal(symbol):
    import random
    signal = random.choice(["BUY", "SELL", "HOLD"])
    price = get_price(symbol)
    return signal, price

def auto_scan():
    tracked = ["BTC/USD", "ETH/USD", "BNB/USD", "XRP/USD", "VIRTUAL/USD", "ZBCN/USD",
               "USD/EUR", "USD/GBP", "GBP/USD", "XAU/USD"]
    summaries = []
    for symbol in tracked:
        try:
            signal, price = generate_signal(symbol)
            if signal in ["BUY", "SELL"]:
                summaries.append(f"📊 {symbol}: {signal} at ${price}")
        except Exception as e:
            print(f"[SCAN ERROR] {symbol} –", e)
    if summaries:
        msg = "🧠 Argento AI SCAN Report (Every 30 Min):\n\n" + "\n".join(summaries)
        send_telegram_message(msg)

scheduler.add_job(auto_scan, "interval", minutes=30)

@app.route("/")
def index():
    return "✅ Argento is Live – SCAN Every 30 Minutes Active."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
