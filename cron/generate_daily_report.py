import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# 1. Configuration
assets = ["AAPL", "BTC-USD", "EURUSD=X"]
data_dir = "/home/timothee/projet-quant/data"
os.makedirs(data_dir, exist_ok=True)

# 2. Data download
df = yf.download(assets, period="5d", interval="1d")["Close"]

# 3. Calculations (Point 6: Volatility, Open/Close, Drawdown)
report_content = (
    f"QUANT REPORT — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
)
report_content += "=" * 40 + "\n"

for asset in assets:
    prices = df[asset].dropna()
    vol = (prices.pct_change().std() * (252 ** 0.5)) * 100
    dd = ((prices / prices.cummax() - 1).min()) * 100

    report_content += f"Asset: {asset}\n"
    report_content += f" - Last price: {prices.iloc[-1]:.2f}\n"
    report_content += f" - Annualized volatility: {vol:.2f}%\n"
    report_content += f" - Max drawdown: {dd:.2f}%\n"
    report_content += "-" * 20 + "\n"

# 4. Local save (Point 6)
filename = f"report_{datetime.now().strftime('%Y%m%d')}.txt"
with open(os.path.join(data_dir, filename), "w") as f:
    f.write(report_content)

print(f"Report generated in {data_dir}")
