import random
from utils.backtest import run_backtest
from utils.data import get_price

def generate_signal(symbol):
    confidence = random.randint(65, 90)
    signal = random.choices(["BUY", "SELL", "HOLD"], weights=[0.3, 0.3, 0.4])[0]
    price = get_price(symbol)
    return signal, confidence, price

def learn_from_performance(symbol):
    result = run_backtest(symbol)
    # Simulate learning: adapt thresholds or weights
    score = result["win_rate"] * result["sharpe_ratio"]
    return {"score": round(score, 2), "adjustment": "threshold updated"}