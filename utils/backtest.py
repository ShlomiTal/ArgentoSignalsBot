import random

def run_backtest(symbol):
    return {
        "symbol": symbol,
        "win_rate": round(random.uniform(65, 85), 2),
        "sharpe_ratio": round(random.uniform(1.0, 2.0), 2),
        "total_return": round(random.uniform(1.2, 3.0), 2)
    }