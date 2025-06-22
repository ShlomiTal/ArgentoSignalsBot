import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils.ai import generate_signal, learn_from_performance
from utils.backtest import run_backtest
from utils.telegram import send_message
from utils.data import get_price

load_dotenv()

print("✅ Argento AI starting up...")

app = Flask(__name__)

@app.route("/")
def index():
    print("📡 GET / called")
    return "✅ Argento AI is running – Signals, Backtest, Learning"

@app.route("/signal")
def signal():
    try:
        symbol = request.args.get("symbol", "BTC/USD")
        print(f"📈 Request for signal: {symbol}")
        signal, confidence, price = generate_signal(symbol)
        print(f"🔁 Signal: {signal}, Confidence: {confidence}, Price: {price}")

        if signal in ["BUY", "SELL"] and price:
            msg = f"🚨 {symbol} Signal: {signal} at ${price:.2f} (Confidence: {confidence}%)"
            print("📤 Sending to Telegram:", msg)
            send_message(msg)

        return jsonify({"symbol": symbol, "signal": signal, "confidence": confidence, "price": price})
    
    except Exception as e:
        print("❌ Error in /signal:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/backtest")
def backtest():
    try:
        symbol = request.args.get("symbol", "BTC/USD")
        print(f"🔬 Running backtest for: {symbol}")
        result = run_backtest(symbol)
        return jsonify(result)
    except Exception as e:
        print("❌ Error in /backtest:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/learn")
def learn():
    try:
        symbol = request.args.get("symbol", "BTC/USD")
        print(f"🧠 Learning for: {symbol}")
        result = learn_from_performance(symbol)
        return jsonify({"status": "updated", "symbol": symbol, "result": result})
    except Exception as e:
        print("❌ Error in /learn:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Server starting on port {port}...")
    app.run(host="0.0.0.0", port=port)
