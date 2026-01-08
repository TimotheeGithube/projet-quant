import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# 1. Config
assets = ['AAPL', 'BTC-USD', 'EURUSD=X']
data_dir = "/home/timothee/projet-quant/data"
os.makedirs(data_dir, exist_ok=True)

# 2. Récupération des données
df = yf.download(assets, period="5d", interval="1d")['Close']

# 3. Calculs (Point 6 : Volatilité, Open/Close, Drawdown)
report_content = f"RAPPORT QUANT DU {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
report_content += "="*40 + "\n"

for asset in assets:
    prices = df[asset].dropna()
    vol = (prices.pct_change().std() * (252**0.5)) * 100
    dd = ((prices / prices.cummax() - 1).min()) * 100
    
    report_content += f"Actif : {asset}\n"
    report_content += f" - Dernier prix : {prices.iloc[-1]:.2f}\n"
    report_content += f" - Volatilité Annuelle : {vol:.2f}%\n"
    report_content += f" - Max Drawdown : {dd:.2f}%\n"
    report_content += "-"*20 + "\n"

# 4. Sauvegarde locale (Point 6)
filename = f"report_{datetime.now().strftime('%Y%m%d')}.txt"
with open(os.path.join(data_dir, filename), "w") as f:
    f.write(report_content)

print(f"Rapport généré dans {data_dir}")
