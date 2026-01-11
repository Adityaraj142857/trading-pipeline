import os
import pandas as pd
import matplotlib.pyplot as plt
from src.auth import get_fyers_session, generate_access_token
from src.data_loader import fetch_data
from src.model_engine import train_model, predict_future
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv

load_dotenv()

def run_pipeline():
    # 1. Auth
    session = get_fyers_session()
    print("Login URL:", session.generate_authcode())
    auth_code = input("Enter auth_code from URL: ")
    access_token = generate_access_token(auth_code)
    fyers = fyersModel.FyersModel(client_id=os.getenv("FYERS_CLIENT_ID"), token=access_token, log_path="")

    # 2. Fetch Historical Data (Training)
    print("Fetching training data (Nov-Dec 2025)...")
    df_train = fetch_data(fyers, range_from="2025-11-01", range_to="2025-12-31")

    # 3. Train Model
    print("Training Random Forest...")
    model, features = train_model(df_train)

    # 4. Predict Future (Recursive)
    print("Predicting next 5 days...")
    preds = predict_future(df_train, model, features, steps=5)

    # 5. Fetch Real Future Data (Validation)
    print("Fetching REAL data for Jan 2026 comparison...")
    df_real = fetch_data(fyers, range_from="2026-01-01", range_to="2026-01-07")
    
    # Standardize lengths for printing
    print("\n--- RESULTS COMPARISON ---")
    for i in range(len(preds)):
        actual_str = f"{df_real.iloc[i]['close']:.2f}" if i < len(df_real) else "N/A"
        print(f"Day {i+1}: Predicted: {preds[i]:.2f} | Actual: {actual_str}")

    # 6. Final Visualization
    plt.figure(figsize=(14, 7))
    # Plot Training Tail
    plt.plot(df_train['timestamp'].tail(15), df_train['close'].tail(15), label='Historical (Dec 2025)', color='blue')
    
    # Plot Predictions
    future_dates = [df_train['timestamp'].max() + pd.Timedelta(days=i) for i in range(1, 6)]
    plt.plot(future_dates, preds, label='Model Prediction', color='red', marker='o', linestyle='--')
    
    # Plot Real Data
    if not df_real.empty:
        plt.plot(df_real['timestamp'], df_real['close'], label='Actual Market Data', color='green', marker='x')

    plt.title("IRCON Prediction vs Actual (Jan 2026)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_pipeline()