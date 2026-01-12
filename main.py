import os
import pandas as pd
from src.auth import get_fyers_session, generate_access_token
from src.data_loader import fetch_data
from src.model_engine import train_model, predict_future_recursive
from src.backtest import calculate_trading_metrics, plot_final_results
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv

load_dotenv()

def main():
    # 1. API Login
    session = get_fyers_session()
    print("Open this URL:", session.generate_authcode())
    auth_code = input("Enter auth_code: ")
    token = generate_access_token(auth_code)
    fyers = fyersModel.FyersModel(client_id=os.getenv("FYERS_CLIENT_ID"), token=token, log_path="")

    # 2. Fetch Training Data (2025)
    print("Fetching 2025 data for training...")
    df_2025 = fetch_data(fyers, range_from="2025-01-01", range_to="2025-12-31")

    # 3. Split & Train (Crucial for Sharpe accuracy)
    # We use 80% for training and 20% for backtesting
    split = int(len(df_2025) * 0.8)
    train_df = df_2025.iloc[:split]
    test_df = df_2025.iloc[split:].copy()

    print("Training Model...")
    model, features = train_model(train_df)

    # 4. Run Backtest on Test Set
    # First, generate MAs for the test set to avoid KeyError
    test_df['MA_5'] = test_df['close'].rolling(window=5).mean()
    test_df['MA_20'] = test_df['close'].rolling(window=20).mean()
    test_df = test_df.dropna()
    
    test_df['Predicted'] = model.predict(test_df[features])
    calculate_trading_metrics(test_df)

    # 5. Recursive Prediction (Future 5 Days)
    print("Forecasting Jan 2026 prices...")
    future_preds = predict_future_recursive(df_2025, model, features, steps=5)

    # 6. Fetch Real Jan 2026 Data for final validation
    print("Fetching actual market data for Jan 2026...")
    df_real = fetch_data(fyers, range_from="2026-01-01", range_to="2026-01-07")
    Predicted = pd.Series(future_preds, name="Predicted")
    df_real = pd.concat([df_real, Predicted], axis=1)
    # plot_final_results(df_2025, future_preds, df_real)
    plot_final_results(df_2025, df_real['Predicted'], df_real)


if __name__ == "__main__":
    main()