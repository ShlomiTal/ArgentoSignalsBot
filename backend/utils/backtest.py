import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.data import get_historical_data
from utils.features import extract_features
from ml.model_train import load_or_train_model

def run_backtest(symbol):
    try:
        df = get_historical_data(symbol, interval="1h", days=90)
        if df is None or df.empty:
            return {"error": "No data"}

        model = load_or_train_model(symbol)

        initial_balance = 10000
        balance = initial_balance
        position = None
        entry_price = 0
        trades = []

        for i in range(10, len(df)):  # skip first 10 for indicators
            row = df.iloc[i]
            features = extract_features(symbol, df.iloc[i - 10:i])
            prediction = model.predict([features])[0]

            current_price = row["close"]

            # Buy
            if prediction == 2 and not position:
                position = "LONG"
                entry_price = current_price

            # Sell
            elif prediction == 0 and position == "LONG":
                profit = (current_price - entry_price) / entry_price
                balance *= 1 + profit
                trades.append(profit)
                position = None

        # Finalize if still in position
        if position == "LONG":
            final_price = df.iloc[-1]["close"]
            profit = (final_price - entry_price) / entry_price
            balance *= 1 + profit
            trades.append(profit)

        win_trades = [t for t in trades if t > 0]
        loss_trades = [t for t in trades if t <= 0]
        win_rate = len(win_trades) / len(trades) if trades else 0
        sharpe = np.mean(trades) / (np.std(trades) + 1e-6) * np.sqrt(252) if trades else 0

        return {
            "symbol": symbol,
            "initial_balance": initial_balance,
            "final_balance": round(balance, 2),
            "trades": len(trades),
            "win_rate": round(win_rate * 100, 2),
            "sharpe_ratio": round(sharpe, 2)
        }

    except Exception as e:
        return {"error": str(e)}
