from flask import Flask, jsonify, render_template_string, request, Response
import pandas as pd
import ta
from binance.client import Client
from sklearn.ensemble import RandomForestClassifier
import requests
import plotly.graph_objs as go
import plotly.io as pio
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Client()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
last_signal_sent = None

def fetch_data():
    klines = client.get_historical_klines("SOLUSDT", Client.KLINE_INTERVAL_1HOUR, "365 days ago UTC")
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades",
        "taker_base_vol", "taker_quote_vol", "ignore"
    ])
    df["close"] = pd.to_numeric(df["close"])
    df["volume"] = pd.to_numeric(df["volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    df.set_index("timestamp", inplace=True)
    return df[["close", "volume"]]

def generate_signals(send_telegram=True):
    global last_signal_sent
    df = fetch_data()
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close']).rsi()
    df['ema50'] = ta.trend.EMAIndicator(close=df['close'], window=50).ema_indicator()
    df['macd'] = ta.trend.MACD(close=df['close']).macd()
    df["future_return"] = df["close"].shift(-2) / df["close"] - 1
    df["signal"] = df["future_return"].apply(lambda x: 1 if x > 0.02 else (-1 if x < -0.02 else 0))
    df.dropna(inplace=True)

    features = ['rsi', 'ema50', 'macd', 'volume']
    X = df[features]
    y = df['signal']
    model = RandomForestClassifier(n_estimators=100, max_depth=5)
    model.fit(X, y)
    df["predicted_signal"] = model.predict(X)

    current_signal = df["predicted_signal"].iloc[-1]
    if send_telegram and current_signal != last_signal_sent:
        last_signal_sent = current_signal
        signal_text = "BUY 📈" if current_signal == 1 else ("SELL 📉" if current_signal == -1 else "HOLD 🤝")
        send_telegram_message(f"🔔 New signal: {signal_text}\nTime: {datetime.utcnow()}")
        send_telegram_plot(df.tail(100))

    return df

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram Error:", e)

def send_telegram_plot(df):
    fig = plot_signals(df)
    img_bytes = pio.to_image(fig, format="png")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    files = {"photo": ("chart.png", img_bytes)}
    data = {"chat_id": CHAT_ID}
    try:
        requests.post(url, data=data, files=files)
    except Exception as e:
        print("Telegram Image Error:", e)

def plot_signals(df):
    trace = go.Scatter(x=df.index, y=df["close"], mode='lines', name='SOL Price')
    buy_signals = df[df["predicted_signal"] == 1]
    sell_signals = df[df["predicted_signal"] == -1]
    trace_buy = go.Scatter(x=buy_signals.index, y=buy_signals["close"], mode='markers', name='BUY', marker=dict(color='green', size=10))
    trace_sell = go.Scatter(x=sell_signals.index, y=sell_signals["close"], mode='markers', name='SELL', marker=dict(color='red', size=10))
    layout = go.Layout(title="SOL Price with Signals", xaxis=dict(title="Time"), yaxis=dict(title="Price"))
    return go.Figure(data=[trace, trace_buy, trace_sell], layout=layout)

@app.route("/signals")
def signals():
    try:
        df = generate_signals()
        result = df.tail(50)[["close", "predicted_signal"]].reset_index().to_dict(orient="records")
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/plot")
def plot_chart():
    df = generate_signals(send_telegram=False).tail(100)
    fig = plot_signals(df)
    graph_html = fig.to_html(full_html=False)
    return render_template_string("<html><body>{{ graph|safe }}</body></html>", graph=graph_html)

@app.route("/backtest")
def backtest():
    df = generate_signals(send_telegram=False)
    df["strategy_return"] = df["predicted_signal"].shift(1) * df["close"].pct_change()
    df.dropna(inplace=True)
    cumulative_return = (1 + df["strategy_return"]).cumprod()
    win_rate = (df["strategy_return"] > 0).mean()
    sharpe_ratio = df["strategy_return"].mean() / df["strategy_return"].std() * (24**0.5)

    stats = {
        "Win Rate": f"{win_rate:.2%}",
        "Cumulative Return": f"{cumulative_return.iloc[-1]:.2f}x",
        "Sharpe Ratio": f"{sharpe_ratio:.2f}"
    }
    return jsonify(stats)

@app.route("/admin")
def admin():
    password = request.args.get("password")
    if password != ADMIN_PASSWORD:
        return Response("Unauthorized", status=401)
    df = generate_signals(send_telegram=False)
    signal = df["predicted_signal"].iloc[-1]
    return f"<h1>Admin Panel</h1><p>Latest Signal: {signal}</p><p>Time: {datetime.utcnow()}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)