import requests
import pandas as pd
import os
from datetime import datetime, timedelta

# Clé API NewsAPI (remplace par la tienne)
api_key = "ee18e61ee3df46289184a2dbce169966"

# Dossier de sortie
output_dir = "../../data/raw/news/"
os.makedirs(output_dir, exist_ok=True)

# Liste des tickers (mots-clés)
tickers = ['Bitcoin', 'Ethereum', 'Dogecoin', 'Ripple', 'Cardano', 'Tesla', 'Apple', 'Microsoft', 'GameStop', 'Nvidia']
news_data = []

# Dates (30 jours max avec NewsAPI gratuit)
end_date = datetime(2025, 4, 6)  # Aujourd'hui
start_date = end_date - timedelta(days=30)  # 7 mars 2025

# Collecte
for ticker in tickers:
    print(f"Collecte pour {ticker}...")
    url = f"https://newsapi.org/v2/everything?q={ticker}&from={start_date.strftime('%Y-%m-%d')}&to={end_date.strftime('%Y-%m-%d')}&language=en&apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'ok' and data['articles']:
            for article in data['articles']:
                news_data.append({
                    'ticker': ticker,
                    'timestamp': article['publishedAt'],
                    'title': article['title'],
                    'description': article['description'] or '',
                    'source': article['source']['name']
                })
        else:
            print(f"Aucune donnée pour {ticker}: {data.get('message', 'Erreur inconnue')}")
    except requests.RequestException as e:
        print(f"Erreur pour {ticker}: {e}")

# Sauvegarde
if news_data:
    df = pd.DataFrame(news_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.to_csv(f"{output_dir}/news_mar_apr_2025.csv", index=False)
    print(f"News: {len(df)} rows collected")
else:
    print("Aucune donnée collectée")