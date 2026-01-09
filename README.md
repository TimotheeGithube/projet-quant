I am Timothee and with Matheo we created this project

Financial Quant Project - Multi-Module Dashboard
This project is a modular financial analysis tool built with Python and Streamlit. It features real-time data visualization, portfolio correlation analysis, and automated daily reporting.

Features :

Module A (Single Asset): Real-time stock data fetching and technical analysis using yfinance.

Module B (Portfolio): Asset correlation matrix and portfolio performance metrics.

Automated Reporting: A background cron job that generates daily market summaries.

24/7 Deployment: Configured to run persistently on a Linux server.

Installation & Setup:

1. Clone the repository
2. Set up the Virtual Environment

"python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt"
(Note: If requirements.txt is missing, install core dependencies: pip install streamlit yfinance pandas plotly)

How to Run the App:
Manual Launch (For Testing)

""streamlit run app/main_app.py""
Production Launch (24/7 Background Mode)
To keep the app running after closing the terminal, we use nohup:

"nohup streamlit run app/main_app.py --server.port 8501 > streamlit_log.txt 2>&1 &"

Access the app: http://localhost:8501

Check logs:" tail -f streamlit_log.txt"

Stop the app:" pkill -f streamlit"

Automation (Cron Job):
The project includes a daily reporting script located in cron/generate_daily_report.py. It is scheduled to run every day at 20:00 (8:00 PM).

Current Crontab Configuration:
To view or edit the schedule, use crontab -e. The entry should look like this:

"00 20 * * * /home/timothee/projet-quant/venv/bin/python3 /home/timothee/projet-quant/cron/generate_daily_report.py"

Generated reports are saved in the /data directory.

📁 Project Structure
Plaintext

├── app/
│   ├── main_app.py      # Entry point (Navigation Menu)
│   ├── single_asset.py  # Module A logic
│   └── quant_b.py       # Module B logic
├── cron/
│   └── generate_daily_report.py # Automated script
├── data/                # Storage for generated reports
├── venv/                # Python virtual environment
└── streamlit_log.txt    # Production server logs
