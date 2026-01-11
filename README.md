# Trading Pipeline Project

# End-to-End Algorithmic Trading Pipeline

This repository implements a machine learning-based trading strategy using the FYERS API v3.

## Features
- **Data:** Automated historical data fetching via FYERS.
- **ML Model:** Random Forest Regressor for price prediction.
- **Strategy:** Moving Average Crossover with ML-filtered signals.
- **Backtesting:** Evaluation using R-Squared, MAE, and Cumulative Returns.

## Setup Instructions
1. **Clone the repo:** `https://github.com/Adityaraj142857/trading-pipeline.git`
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Configure Environment:** Create a `.env` file with your FYERS credentials.
4. **Run Pipeline:** `python main.py`

