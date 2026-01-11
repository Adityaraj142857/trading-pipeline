from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np

def train_model(df):
    # Use features consistent with your notebook
    df['MA_5'] = df['close'].rolling(window=5).mean()
    df['MA_20'] = df['close'].rolling(window=20).mean()
    df['Target'] = df['close'].shift(-1)
    df = df.dropna()

    features = ['open', 'high', 'low', 'close', 'volume', 'MA_5', 'MA_20']
    X = df[features]
    y = df['Target']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, features

def predict_future(df, model, feature_cols, steps=5):
    future_predictions = []
    temp_df = df.copy()
    
    for i in range(steps):
        # Take the last row to build the next prediction
        last_row = temp_df.iloc[-1]
        
        # Prepare input for model
        # For a simple recursive forecast, we use the last known OHLC
        # In a real scenario, you'd estimate next OHLC, but here we use last close as proxy
        input_data = pd.DataFrame([last_row[feature_cols]], columns=feature_cols)
        
        prediction = model.predict(input_data)[0]
        future_predictions.append(prediction)
        
        # Add the prediction as a new row to temp_df to update Moving Averages
        new_date = temp_df['timestamp'].max() + pd.Timedelta(days=1)
        # Simplified new row logic
        new_row = last_row.copy()
        new_row['timestamp'] = new_date
        new_row['close'] = prediction
        new_row['open'] = last_row['close'] # Next open approx last close
        
        temp_df = pd.concat([temp_df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Re-calculate MAs for the next step
        temp_df['MA_5'] = temp_df['close'].rolling(window=5).mean()
        temp_df['MA_20'] = temp_df['close'].rolling(window=20).mean()
        
    return future_predictions