📈 IRCON Stock Price Prediction & Automated Trading Pipeline
An end-to-end algorithmic trading system that integrates the FYERS API v3 with Machine Learning to predict stock prices and simulate future market movements. This project covers the entire pipeline from secure authentication and data fetching to feature engineering, model training, and recursive forecasting.

🚀 Key Features
FYERS API Integration: Automated session management and historical data fetching.

ML-Powered Predictions: Uses a RandomForestRegressor to analyze price action and volume.

Recursive Forecasting: Implements a sliding-window logic to predict the next 5 days of stock prices.

Live Comparison: Fetches real-market data (Jan 2026) to validate model accuracy against actual results.

Modular Architecture: Clean, production-ready code structure (not just a single script).

🛠 Project Structure
The repository is organized into a modular structure to ensure maintainability and reproducibility:

## 📁 Repository Structure
```text
trading-pipeline/
├── src/
│   ├── auth.py          # API Authentication logic
│   ├── data_loader.py   # Data fetching from FYERS
│   ├── features.py     # Feature engineering (MAs and Lags)
│   ├── model_engine.py  # RF Training & Recursive forecasting
│   └── backtest.py      # Validation and Visualization
├── main.py              # Entry point
├── .env                 # API Credentials (Private)
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```
⚙️ Setup and Installation
1. Prerequisites

Python 3.8+

A FYERS account with API access.

2. Installation

Clone the repository and install the required libraries:

Bash
git clone https://github.com/Adityaraj142857/trading-pipeline
cd your-repo-name
pip install -r requirements.txt
3. Environment Configuration

Create a .env file in the root directory and add your FYERS credentials:

Plaintext
FYERS_CLIENT_ID=your_client_id_here
FYERS_SECRET_KEY=your_secret_key_here
FYERS_REDIRECT_URI=https://trade.fyers.in/api-login/redirect-uri/index.html
📊 How to Run
To run the full pipeline (Data fetch ➔ Training ➔ 5-Day Prediction ➔ Comparison):

Bash
python main.py
The script will generate a login URL.

Visit the URL, log in, and copy the auth_code from the redirect URL.

Paste the code back into the terminal to continue the execution.

📈 Methodology
Data Period: Training on IRCON-EQ data from Nov 2025 to Dec 2025.

Features: 5-day Lags, 5-day Moving Average (MA), 20-day MA, and Volume.

Validation: Comparison against actual market prices from Jan 1st to Jan 7th, 2026.

📜 License
This project is for educational and research purposes only. Trading involves financial risk. Use at your own discretion.

🤝 Contributing

Feel free to fork this repository and submit pull requests for any feature improvements or bug fixes.
