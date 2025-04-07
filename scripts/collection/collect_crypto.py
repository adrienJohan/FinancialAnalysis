import requests
import pandas as pd
import os
import time

def get_cryptocompare_data(symbol, days=90):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={symbol}&tsym=USD&limit=2000"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['Data']['Data']
        if not data:
            raise ValueError(f"Aucune donnée pour {symbol}")
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['time'], unit='s')
        df = df[['timestamp', 'open', 'high', 'low', 'close', 'volumefrom', 'volumeto']]
        df = df.rename(columns={'close': 'price'})
        return df
    except requests.RequestException as e:
        print(f"Erreur réseau pour {symbol}: {e}")
        return None
    except ValueError as e:
        print(e)
        return None

output_dir = "../../data/raw/financial/"
os.makedirs(output_dir, exist_ok=True)

coins = {'BTC': 'BTC', 'ETH': 'ETH', 'DOGE': 'DOGE', 'XRP': 'XRP', 'ADA': 'ADA'}
for ticker, symbol in coins.items():
    print(f"Collecte pour {ticker}...")
    df = get_cryptocompare_data(symbol)
    if df is not None:
        df.to_csv(f"{output_dir}/{ticker}_prices_jan_apr_2025.csv", index=False)
        print(f"{ticker}: {len(df)} rows collected")
    else:
        print(f"Échec pour {ticker}")
    time.sleep(2)