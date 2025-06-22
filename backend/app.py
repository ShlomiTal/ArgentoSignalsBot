from flask import Flask, request, jsonify
import os, requests, random
from datetime import datetime, timezone
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

last_sent = {}

def send_telegram_message(text):
    if not TELEGRAM_TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_DATA_API_KEY}"
        res = requests.get(url)
        return float(res.json()["price"])
    except:
        return None

def generate_signal(symbol):
    signal = random.choice(["BUY", "SELL", "HOLD"])
    price = get_price(symbol)
    return signal, price

@app.route("/")
def index():
    return "✅ Argento Fullstack is Running"

@app.route("/scan")
def scan():
    assets = ["BTC/USD", "ETH/USD", "XAU/USD", "USD/EUR", "ZBCN/USD"]
    results = []
    for s in assets:
        sig, p = generate_signal(s)
        if sig in ["BUY", "SELL"]:
            results.append(f"{s}: {sig} @ ${p}")
    if results:
        send_telegram_message("🧠 Argento SCAN:
" + "
".join(results))
    return jsonify({"signals": results})

scheduler.add_job(scan, "interval", minutes=60)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
