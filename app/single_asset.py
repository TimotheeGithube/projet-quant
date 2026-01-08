import streamlit as st
import yfinance as yf
import numpy as np

def run_quant_a():
    st.title("📈 Analyse Mono-Actif (Quant A)")
    ticker = st.sidebar.text_input("Ticker", "AAPL") # Sidebar pour plus de clarté
    
    # Récupération des données [cite: 15]
    data = yf.download(ticker, period="1y", interval="1d")
    
    if not data.empty:
        # Calculs [cite: 34]
        data["Return"] = data["Close"].pct_change()
        volatility = data["Return"].std() * np.sqrt(252)

        st.subheader(f"Indicateurs pour {ticker}")
        st.metric("Volatilité annuelle", f"{volatility:.2%}")

        # Exigence : Graphique du prix [cite: 35]
        st.subheader("Prix de clôture")
        st.line_chart(data["Close"])
        
        # NOTE : Tu dois encore ajouter les 2 stratégies de backtesting 
        # et le graphique combiné pour valider ce module.
