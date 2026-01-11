import pandas as pd
import numpy as np

def generate_features(df, window=5):
    df = df.copy()
    # Create Lags (Previous 5 days of prices)
    for i in range(1, window + 1):
        df[f'lag_{i}'] = df['close'].shift(i)
    
    # Technical Indicators from your notebook logic
    df['MA_5'] = df['close'].rolling(window=5).mean()
    df['MA_20'] = df['close'].rolling(window=20).mean()
    
    # Target is the next day's price
    df['Target'] = df['close'].shift(-1)
    
    return df.dropna()