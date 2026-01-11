import pandas as pd
from fyers_apiv3 import fyersModel
import os

def fetch_data(fyers, symbol="NSE:IRCON-EQ", range_from="2025-11-01", range_to="2025-12-31"):
    data = {
        "symbol": symbol,
        "resolution": "D",
        "date_format": "1",
        "range_from": range_from,
        "range_to": range_to,
        "cont_flag": "1"
    }
    
    response = fyers.history(data=data)
    if response["s"] == "ok":
        df = pd.DataFrame(response["candles"], 
                          columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        return df
    else:
        return pd.DataFrame() # Return empty if no data found