import pandas as pd
import requests
import os

API_KEY = os.getenv("TWELVE_DATA_API_KEY")

def fetch_data(symbol, interval="1day", outputsize=500):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={API_KEY}&format=JSON"
    response = requests.get(url).json()
    if "values" in response:
        df = pd.DataFrame(response["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime")
        df.set_index("datetime", inplace=True)
        df = df.astype(float)
        return df
    else:
        raise Exception(f"Error fetching data: {response}")
