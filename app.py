import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils.ai import generate_signal, learn_from_performance
from utils.backtest import run_backtest
from utils.telegram import send_message
from utils.data import get_price

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Argento AI is running – Signals, Backtest, Learning"

@app.route("/signal")
def signal():
    symbol = request.args.get("symbol", "BTC/USD")
    signal, confidence, price = generate_signal(symbol)
    if signal in ["BUY", "SELL"]:
        send_message(f"🚨 {symbol} Signal: {signal} at ${price:.2f} (Confidence: {confidence}%)")
    return jsonify({"symbol": symbol, "signal": signal, "confidence": confidence, "price": price})

@app.route("/backtest")
def backtest():
    symbol = request.args.get("symbol", "BTC/USD")
    result = run_backtest(symbol)
    return jsonify(result)

@app.route("/learn")
def learn():
    symbol = request.args.get("symbol", "BTC/USD")
    result = learn_from_performance(symbol)
    return jsonify({"status": "updated", "symbol": symbol, "result": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)