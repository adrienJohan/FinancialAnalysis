import yfinance as yf
import pandas as pd
import os

output_dir = "../../data/raw/financial/"
os.makedirs(output_dir, exist_ok=True)

tickers = ['TSLA', 'AAPL', 'MSFT', 'GME', 'NVDA']
for ticker in tickers:
    print(f"Collecte pour {ticker}...")
    stock = yf.Ticker(ticker)
    df = stock.history(start="2025-01-06", end="2025-04-06", interval="1h")
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df.to_csv(f"{output_dir}/{ticker}_prices_jan_apr_2025.csv")
    print(f"{ticker}: {len(df)} rows collected")