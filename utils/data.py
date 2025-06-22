import os
import requests

TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_DATA_API_KEY}"
        res = requests.get(url)
        data = res.json()

        if "price" in data:
            return float(data["price"])
        else:
            print(f"[Data Error] No price in response: {data}")
            return None

    except Exception as e:
        print(f"[Data Error] {symbol}:", e)
        return None
