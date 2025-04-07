


import mysql.connector
import pandas as pd
import os

# Connexion à MySQL
db = mysql.connector.connect(
    host="localhost",
    user="Analysis_user",  
    password="SuperMotDePasse!123",  
    database="FinancialAnalysis"
)

cursor = db.cursor()

# Chemins des données
base_dir = "../data/raw/"

# Mapping des tickers (News → Prices)
ticker_mapping = {
    'Bitcoin': 'BTC',
    'Ethereum': 'ETH',
    'Dogecoin': 'DOGE',
    'Ripple': 'XRP',
    'Cardano': 'ADA',
    'Tesla': 'TSLA',
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'GameStop': 'GME',
    'Nvidia': 'NVDA'
}

# 1. Importer Prices (Cryptos et Actions)
tickers = ['BTC', 'ETH', 'DOGE', 'XRP', 'ADA', 'TSLA', 'AAPL', 'MSFT', 'GME', 'NVDA']
crypto_tickers = ['BTC', 'ETH', 'DOGE', 'XRP', 'ADA']
stock_tickers = ['TSLA', 'AAPL', 'MSFT', 'GME', 'NVDA']

for ticker in tickers:
    file = f"{base_dir}/financial/{ticker}_prices_jan_apr_2025.csv"
    if os.path.exists(file):
        df = pd.read_csv(file)
        print(f"Importation de {ticker}...")
        for _, row in df.iterrows():
            sql = """
            INSERT INTO Prices (ticker, timestamp, open, high, low, close, volume, volume_from)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            if ticker in crypto_tickers:
                values = (
                    ticker,
                    row['timestamp'],
                    row['open'],
                    row['high'],
                    row['low'],
                    row['price'],
                    row['volumeto'],
                    row.get('volumefrom', None)
                )
            else:  # Actions
                values = (
                    ticker,
                    row['Datetime'],
                    row['Open'],
                    row['High'],
                    row['Low'],
                    row['Close'],
                    row['Volume'],
                    None
                )
            cursor.execute(sql, values)
        db.commit()
        print(f"{ticker}: {len(df)} lignes insérées")

# 2. Importer ForexData
pairs = ['EURUSD=X', 'USDJPY=X', 'USDCHF=X', 'GC=F']
for pair in pairs:
    file = f"{base_dir}/forex/{pair}_jan_apr_2025.csv"
    if os.path.exists(file):
        df = pd.read_csv(file)
        print(f"Importation de {pair}...")
        for _, row in df.iterrows():
            sql = """
            INSERT INTO ForexData (pair, timestamp, open, high, low, rate)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (pair, row['Datetime'], row['Open'], row['High'], row['Low'], row['rate'])
            cursor.execute(sql, values)
        db.commit()
        print(f"{pair}: {len(df)} lignes insérées")

# 3. Importer EconomicData
file = f"{base_dir}/economic/economic_data_dec_apr_2025.csv"
if os.path.exists(file):
    df = pd.read_csv(file)
    print("Importation des données économiques...")
    for _, row in df.iterrows():
        sql = """
        INSERT INTO EconomicData (timestamp, inflation_rate, interest_rate, unemployment_rate,
                                  treasury_10y, treasury_2y, yield_spread_10y_2y, usd_aud_rate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            row['DATE'],
            row['inflation_rate'] if pd.notna(row['inflation_rate']) else None,
            row['interest_rate'] if pd.notna(row['interest_rate']) else None,
            row['unemployment_rate'] if pd.notna(row['unemployment_rate']) else None,
            row['treasury_10y'] if pd.notna(row['treasury_10y']) else None,
            row['treasury_2y'] if pd.notna(row['treasury_2y']) else None,
            row['yield_spread_10y_2y'] if pd.notna(row['yield_spread_10y_2y']) else None,
            row['usd_aud_rate'] if pd.notna(row['usd_aud_rate']) else None
        )
        cursor.execute(sql, values)
    db.commit()
    print(f"EconomicData: {len(df)} lignes insérées")

# 4. Importer News (avec mapping des tickers)
file = f"{base_dir}/news/news_mar_apr_2025.csv"
if os.path.exists(file):
    df = pd.read_csv(file)
    print("Importation des nouvelles...")
    for _, row in df.iterrows():
        # Mapper le ticker de News (ex. : "Bitcoin" → "BTC")
        news_ticker = row['ticker']
        mapped_ticker = ticker_mapping.get(news_ticker, news_ticker)
        sql = """
        INSERT INTO News (ticker, timestamp, title, description, source)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            mapped_ticker,
            row['timestamp'],
            row['title'],
            row['description'] if pd.notna(row['description']) else None,
            row['source']
        )
        cursor.execute(sql, values)
    db.commit()
    print(f"News: {len(df)} lignes insérées")

# 5. Peupler PriceNews (gérer les timezones)
print("Peuplement de PriceNews...")
sql = """
INSERT INTO PriceNews (price_id, news_id)
SELECT p.price_id, n.news_id
FROM Prices p
JOIN News n
ON p.ticker = n.ticker
AND DATE(CONVERT_TZ(p.timestamp, '+00:00', '+00:00')) = DATE(CONVERT_TZ(n.timestamp, '+00:00', '+00:00'))
"""
cursor.execute(sql)
db.commit()
print(f"PriceNews: {cursor.rowcount} lignes insérées")

# Si 0 lignes, essayer une jointure élargie (±1 jour)
if cursor.rowcount == 0:
    print("Aucune correspondance exacte, tentative avec ±1 jour...")
    sql = """
    INSERT INTO PriceNews (price_id, news_id)
    SELECT p.price_id, n.news_id
    FROM Prices p
    JOIN News n
    ON p.ticker = n.ticker
    AND DATE(CONVERT_TZ(p.timestamp, '+00:00', '+00:00')) 
        BETWEEN DATE_SUB(DATE(CONVERT_TZ(n.timestamp, '+00:00', '+00:00')), INTERVAL 1 DAY) 
        AND DATE_ADD(DATE(CONVERT_TZ(n.timestamp, '+00:00', '+00:00')), INTERVAL 1 DAY)
    """
    cursor.execute(sql)
    db.commit()
    print(f"PriceNews (élargi): {cursor.rowcount} lignes insérées")

# Fermer la connexion
cursor.close()
db.close()
print("Importation terminée !")