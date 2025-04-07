from fredapi import Fred
import pandas as pd
import os

# Remplace par ta clé API FRED
fred = Fred(api_key="b9218e19bcff7d0f141da9f66b1a11d0")

# Dossier de sortie
output_dir = "../../data/raw/economic/"
os.makedirs(output_dir, exist_ok=True)

# Collecte des séries économiques (quotidiennes où possible)
data = {
    'inflation_rate': fred.get_series('CPIAUCSL'),      # Mensuel (indice des prix)
    'interest_rate': fred.get_series('FEDFUNDS'),       # Mensuel (taux fédéral)
    'unemployment_rate': fred.get_series('UNRATE'),     # Mensuel (chômage)
    'treasury_10y': fred.get_series('DGS10'),           # Quotidien (rendement 10 ans)
    'treasury_2y': fred.get_series('DGS2'),             # Quotidien (rendement 2 ans)
    'yield_spread_10y_2y': fred.get_series('T10Y2Y'),   # Quotidien (écart 10y-2y)
    'usd_aud_rate': fred.get_series('DEXUSAL')          # Quotidien (USD/AUD)
}

# Créer un DataFrame
df = pd.DataFrame(data)

# Filtrer pour 3 mois jusqu'à aujourd'hui (2024-12-06 à 2025-04-06)
df = df.loc['2024-12-06':'2025-04-06']

# Sauvegarde
df.to_csv(f"{output_dir}/economic_data_dec_apr_2025.csv")
print(f"Economic data: {len(df)} rows collected")
print(df.head())  # Aperçu des premières lignes pour vérification