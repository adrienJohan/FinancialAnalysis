import yfinance as yf
import pandas as pd
import os

def collect_forex_data(pair, start="2025-01-06", end="2025-04-06", interval="1h"):
    try:
        fx = yf.Ticker(pair)
        df = fx.history(start=start, end=end, interval=interval)
        if df.empty:
            raise ValueError(f"Aucune donnée trouvée pour {pair}")
        df = df[['Open', 'High', 'Low', 'Close']].rename(columns={'Close': 'rate'})
        return df
    except Exception as e:
        print(f"Erreur pour {pair}: {e}")
        return None

# Dossier de sortie
output_dir = "../../data/raw/forex/"
os.makedirs(output_dir, exist_ok=True)

# Liste des paires Forex (remplace XAUUSD=X par GC=F pour l'or)
forex_pairs = ['EURUSD=X', 'USDJPY=X', 'USDCHF=X', 'GC=F']
for pair in forex_pairs:
    print(f"Collecte pour {pair}...")
    df = collect_forex_data(pair)
    if df is not None:
        df.to_csv(f"{output_dir}/{pair}_jan_apr_2025.csv")
        print(f"{pair}: {len(df)} rows collected")
    else:
        print(f"Échec pour {pair}")