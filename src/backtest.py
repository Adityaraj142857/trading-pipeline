import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_trading_metrics(df, cost_per_trade=0.0007):
    """
    Calculates Net P&L, Max Drawdown, and Annualized Sharpe Ratio.
    """
    # Strategy: Buy (1) if predicted price is higher than current close
    df['Signal'] = np.where(df['Predicted'] > df['close'], 1, 0)
    df['Market_Returns'] = df['close'].pct_change()
    
    # Transaction costs: apply whenever the signal changes
    df['Trades'] = df['Signal'].diff().abs().fillna(0)
    
    # Calculate Strategy Returns
    df['Strategy_Returns'] = (df['Signal'].shift(1) * df['Market_Returns']) - (df['Trades'] * cost_per_trade)
    df = df.dropna()

    # Cumulative Returns (Equity Curve)
    cum_returns = (1 + df['Strategy_Returns']).cumprod()
    
    # Net P&L
    net_pnl = (cum_returns.iloc[-1] - 1) * 100
    
    # Sharpe Ratio (Annualized)
    sharpe = (df['Strategy_Returns'].mean() / df['Strategy_Returns'].std()) * np.sqrt(252)
    
    # Max Drawdown
    rolling_max = cum_returns.cummax()
    drawdown = (cum_returns - rolling_max) / rolling_max
    max_dd = drawdown.min() * 100

    print("\n" + "="*35)
    print(f"   BACKTEST RESULTS (Test Set)")
    print("="*35)
    print(f"Net P&L:          {net_pnl:.2f}%")
    print(f"Max Drawdown:     {max_dd:.2f}%")
    print(f"Sharpe Ratio:     {sharpe:.2f}")
    print("="*35)
    
    return cum_returns

def plot_final_results(df_history, predictions, df_real):
    """
    Plots the final comparison: History vs Model vs Actual Market.
    """
    plt.figure(figsize=(12, 6))
    
    # Plot historical tail
    plt.plot(df_history['timestamp'].tail(20), df_history['close'].tail(20), label='Dec 2025 History', color='blue')
    
    # Plot 5-day forecast
    last_date = df_history['timestamp'].max()
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, 6)]
    # plt.plot(future_dates, predictions, label='5-Day Forecast', color='red', marker='o', linestyle='--')
    
    # Plot real validation data
    if not df_real.empty:
        plt.plot(df_real['timestamp'], df_real['close'], label='Jan 2026 Actual', color='green', marker='x')
    plt.plot(df_real['timestamp'], predictions, label='5-Day Forecast', color='red', marker='o', linestyle='--')

    plt.title("IRCON Prediction Validation (Jan 2026)")
    plt.legend()
    plt.grid(True)
    plt.show()