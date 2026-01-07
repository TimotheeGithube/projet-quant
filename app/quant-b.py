
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Projet Quant B – Dashboard Portefeuille")

# 1. Sélection multi-actifs (Minimum 3 pour le module B) [cite: 41]
tickers = st.multiselect("Sélectionnez vos actifs", 
                         ["AAPL", "MSFT", "GOOGL", "BTC-USD", "GC=F"], 
                         default=["AAPL", "BTC-USD", "GC=F"])

if len(tickers) >= 3:
    # 2. Récupération des données [cite: 15]
    data = yf.download(tickers, period="1y")["Close"]
    
    # 3. Calculs quantitatifs (Rendements et Corrélation) 
    returns = data.pct_change().dropna()
    corr_matrix = returns.corr()

    # 4. Affichage des métriques de corrélation 
    st.subheader("🔗 Matrice de Corrélation")
    fig, ax = plt.subplots()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # 5. Graphique des prix normalisés (Base 100) 
    st.subheader("📈 Comparaison des actifs (Base 100)")
    data_norm = (data / data.iloc[0]) * 100
    st.line_chart(data_norm)

else:
    st.warning("Veuillez sélectionner au moins 3 actifs pour valider le module Quant B[cite: 41].")


