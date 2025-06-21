import os
import time
import pandas as pd
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SETTINGS_PASSWORD = os.getenv("SETTINGS_PASSWORD")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

# Track last sent signals
last_sent = {}

# === Telegram Messaging ===
def send_telegram_message(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram Error:", e)

# === Simulated Signal Function ===
def generate_signal(asset):
    import random
    choices = ["BUY", "SELL", "HOLD"]
    return random.choice(choices), round(random.uniform(100, 10000), 2)

# === Signal Route ===
@app.route("/signals")
def signals():
    symbol = request.args.get("symbol", "BTC")
    signal, price = generate_signal(symbol)

    # Control HOLD spam
    now = time.time()
    if signal == "HOLD":
        last_hold = last_sent.get(f"{symbol}_HOLD", 0)
        if now - last_hold < 6 * 3600:
            return jsonify({"symbol": symbol, "signal": signal, "price": price})
        last_sent[f"{symbol}_HOLD"] = now

    if signal in ["BUY", "SELL"]:
        message = f"📊 Argento AI Signal – {symbol}
\n💰 Price: ${price}\nSignal: {signal}"
        send_telegram_message(message)
        last_sent[symbol] = signal

    return jsonify({"symbol": symbol, "signal": signal, "price": price})

# === Backtest Simulation ===
@app.route("/backtest")
def backtest():
    symbol = request.args.get("symbol", "BTC")
    result = {
        "symbol": symbol,
        "win_rate": round(70 + 20 * (hash(symbol) % 10) / 10, 2),
        "sharpe": round(1.2 + (hash(symbol) % 5) * 0.2, 2),
        "return": round(1.5 + (hash(symbol) % 3) * 0.5, 2)
    }
    return jsonify(result)

# === Admin Dashboard ===
@app.route("/admin")
def admin():
    if request.args.get("password") != ADMIN_PASSWORD:
        return "Unauthorized", 401
    return jsonify({
        "status": "OK",
        "tracked_assets": ["BTC", "ETH", "XAUUSD"],
        "last_signals": last_sent
    })

# === Settings Page (stub) ===
@app.route("/settings")
def settings():
    if request.args.get("password") != SETTINGS_PASSWORD:
        return "Unauthorized", 401
    return jsonify({
        "features": {
            "telegram_alerts": True,
            "auto_backtest": True,
            "csv_export": True,
            "market_alerts": True
        },
        "logo": "default"
    })

# === Market Alerts (simulated) ===
def check_market_alerts():
    from datetime import datetime
    now = datetime.utcnow()
    market_times = {
        "us_open": (13, 30),
        "us_close": (20, 0),
        "eu_open": (7, 0),
        "eu_close": (15, 30),
        "asia_open": (0, 0),
        "asia_close": (6, 0)
    }
    for key, (h, m) in market_times.items():
        tag = f"alert_{key}"
        if (now.hour, now.minute) == (h, m) and last_sent.get(tag) != now.date():
            name = key.replace("_", " ").upper()
            msg = f"🕒 Market Update: {name.replace('_', ' ').title()} just triggered."
            send_telegram_message(msg)
            last_sent[tag] = now.date()

scheduler.add_job(check_market_alerts, "interval", minutes=1)

# === Auto Scan & Report ===
def auto_scan():
    tracked = ["BTC", "ETH", "XAUUSD", "USD/EUR", "ZBCN"]
    for symbol in tracked:
        signal, price = generate_signal(symbol)
        if signal in ["BUY", "SELL"]:
            summary = (
                f"📊 Signal Scan – {symbol}
"
                f"💰 Price: ${price}
"
                f"Signal: {signal}
"
                f"Trend: Simulated
"
                f"Sentiment: Neutral
"
                f"Backtest: WinRate 75%, Sharpe 1.9
"
                f"⏰ Time: {time.strftime('%H:%M UTC')}"
            )
            send_telegram_message(summary)

scheduler.add_job(auto_scan, "interval", hours=1)

# === Root Ping ===
@app.route("/")
def index():
    return "✅ Argento is Live. Backend is running."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)