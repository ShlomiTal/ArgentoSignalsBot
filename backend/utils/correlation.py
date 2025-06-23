import numpy as np
import pandas as pd
from utils.data import get_historical_data

def compute_correlation_matrix(symbols, interval="1h", days=30):
    price_data = {}

    for symbol in symbols:
        df = get_historical_data(symbol, interval=interval, days=days)
        if df is not None and not df.empty:
            price_data[symbol] = df["close"]

    if len(price_data) < 2:
        return None  # Not enough data

    prices_df = pd.DataFrame(price_data).dropna()
    correlation_matrix = prices_df.corr()

    return correlation_matrix


def get_strongest_pairs(symbols, threshold=0.85):
    matrix = compute_correlation_matrix(symbols)
    if matrix is None:
        return []

    strong_pairs = []
    for sym1 in symbols:
        for sym2 in symbols:
            if sym1 != sym2:
                corr = matrix.loc[sym1, sym2]
                if abs(corr) >= threshold:
                    strong_pairs.append({
                        "pair": (sym1, sym2),
                        "correlation": round(corr, 3)
                    })

    # remove duplicates (A,B) and (B,A)
    unique_pairs = []
    seen = set()
    for item in strong_pairs:
        pair = tuple(sorted(item["pair"]))
        if pair not in seen:
            seen.add(pair)
            unique_pairs.append(item)

    return unique_pairs
