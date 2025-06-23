import os
import requests
import pandas as pd
from datetime import datetime, timedelta

TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_DATA_API_KEY}"
        res = requests.get(url)
        data = res.json()
        return float(data["price"])
    except Exception as e:
        print(f"[Data Error] {symbol} price fetch failed:", e)
        return None


def get_historical_data(symbol, interval="1h", days=30):
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)

        url = (
            f"https://api.twelvedata.com/time_series?symbol={symbol}"
            f"&interval={interval}&start_date={start_time.strftime('%Y-%m-%d')}"
            f"&end_date={end_time.strftime('%Y-%m-%d')}&apikey={TWELVE_DATA_API_KEY}&outputsize=5000"
        )
        res = requests.get(url)
        data = res.json()

        if "values" not in data:
            print(f"[Data Error] No values returned for {symbol}")
            return None

        df = pd.DataFrame(data["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime")
        df.set_index("datetime", inplace=True)
        df = df.astype(float)

        return df

    except Exception as e:
        print(f"[Data Error] {symbol} historical fetch failed:", e)
        return None
