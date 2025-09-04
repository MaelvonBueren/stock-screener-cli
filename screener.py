import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Input: tickers + date range
tickers = [t.strip().upper() for t in input("Enter tickers (comma separated): ").split(",")]
start_date = input("Start date (YYYY-MM-DD): ")
end_date = input("End date (YYYY-MM-DD): ")

# Download adjusted close prices
data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"].dropna(axis=1, how="all")

# Daily returns & cumulative performance
returns = data.pct_change().dropna()
cumulative = (1 + returns).cumprod()

# Performance metrics
metrics = pd.DataFrame(index=data.columns)
metrics["Last Price"] = data.iloc[-1]
metrics["CAGR"] = (cumulative.iloc[-1] ** (252 / len(returns))) - 1
metrics["Volatility"] = returns.std() * np.sqrt(252)
metrics["Sharpe"] = metrics["CAGR"] / metrics["Volatility"]

# Technical signals
ma50 = data.rolling(50).mean()
ma200 = data.rolling(200).mean()
metrics["Above 200MA"] = data.iloc[-1] > ma200.iloc[-1]

# Screening filters
screened = metrics[
    (metrics["CAGR"] > 0) &
    (metrics["Sharpe"] > 1) &
    (metrics["Above 200MA"])
]

print("\n=== Metrics ===")
print(metrics.round(3))
print("\n=== Screened Stocks ===")
print(screened.round(3))

# Plot screened stocks with moving averages
for ticker in screened.index:
    plt.figure(figsize=(10, 6))
    data[ticker].plot(label="Price")
    ma50[ticker].plot(label="50-day MA")
    ma200[ticker].plot(label="200-day MA")
    plt.title(f"{ticker} Price with Moving Averages")
    plt.legend()
    plt.show()