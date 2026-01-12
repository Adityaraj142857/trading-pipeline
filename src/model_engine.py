import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def train_model(df):
    """
    Trains the model. Includes internal feature engineering to prevent KeyErrors.
    """
    # 1. Feature Engineering
    df = df.copy()
    df['MA_5'] = df['close'].rolling(window=5).mean()
    df['MA_20'] = df['close'].rolling(window=20).mean()
    df['Target'] = df['close'].shift(-1)
    df = df.dropna()

    # 2. Define Features
    features = ['open', 'high', 'low', 'close', 'volume', 'MA_5', 'MA_20']
    X = df[features]
    y = df['Target']
    
    # 3. Model with constraints to prevent overfitting (Realistic Sharpe)
    model = RandomForestRegressor(
        n_estimators=100, 
        max_depth=5, 
        min_samples_leaf=10, 
        random_state=42
    )
    model.fit(X, y)
    
    return model, features

def predict_future_recursive(df, model, feature_cols, steps=5):
    """
    Predicts next N days by re-calculating MAs at every step.
    """
    future_predictions = []
    temp_df = df.copy()
    
    for i in range(steps):
        # Always ensure MAs are calculated for the latest data
        temp_df['MA_5'] = temp_df['close'].rolling(window=5).mean()
        temp_df['MA_20'] = temp_df['close'].rolling(window=20).mean()
        
        last_row = temp_df.iloc[-1:]
        
        # Predict the next day's price
        prediction = model.predict(last_row[feature_cols])[0]
        future_predictions.append(prediction)
        
        # Create a dummy row for the next day to feed back into the loop
        new_date = temp_df['timestamp'].max() + pd.Timedelta(days=1)
        new_row = {
            'timestamp': new_date,
            'open': temp_df.iloc[-1]['close'],
            'high': prediction, # Approximation
            'low': prediction,  # Approximation
            'close': prediction,
            'volume': temp_df.iloc[-1]['volume']
        }
        temp_df = pd.concat([temp_df, pd.DataFrame([new_row])], ignore_index=True)
        
    return future_predictions