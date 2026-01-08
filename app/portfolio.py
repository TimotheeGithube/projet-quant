import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run_quant_b():
    st.title("📊 Module B – Gestion de Portefeuille Multi-Actifs")
    st.markdown("Ce module permet de simuler une allocation d'actifs et d'analyser les corrélations.")

    # 1. Sélection des actifs (Exigence: au moins 3) 
    available_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "BTC-USD", "ETH-USD", "GC=F", "EURUSD=X"]
    tickers = st.multiselect(
        "Sélectionnez au moins 3 actifs pour votre portefeuille",
        available_tickers,
        default=["AAPL", "BTC-USD", "GC=F"]
    )

    if len(tickers) < 3:
        st.warning("⚠️ Veuillez sélectionner au moins 3 actifs pour valider ce module.")
        return

    # 2. Récupération des données [cite: 15]
    with st.spinner('Récupération des données de marché...'):
        data = yf.download(tickers, period="1y")["Close"]

    if data.empty:
        st.error("Erreur lors de la récupération des données.")
        return

    # 3. Paramètres de stratégie (Poids des actifs) [cite: 43]
    st.subheader("⚙️ Configuration de l'allocation")
    cols = st.columns(len(tickers))
    weights = []
    
    for i, col in enumerate(cols):
        with col:
            w = st.number_input(f"Poids {tickers[i]}", min_value=0.0, max_value=1.0, value=1.0/len(tickers), step=0.05)
            weights.append(w)

    # Vérification de la somme des poids
    total_weight = sum(weights)
    st.info(f"Somme totale des poids : **{total_weight:.2f}**")
    if abs(total_weight - 1.0) > 0.001:
        st.warning("⚠️ La somme des poids devrait idéalement être égale à 1 (100%).")

    # 4. Calculs des rendements et corrélations 
    returns = data.pct_change().dropna()
    
    # Matrice de Corrélation
    st.subheader("🔗 Analyse des Corrélations")
    corr_matrix = returns.corr()
    fig_corr, ax_corr = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr_matrix, annot=True, cmap="RdYlGn", center=0, ax=ax_corr)
    st.pyplot(fig_corr)

    # 5. Simulation de la performance du portefeuille [cite: 42, 44]
    # Calcul du rendement du portefeuille
    portfolio_return = (returns * weights).sum(axis=1)
    # Valeur cumulative (Base 100)
    portfolio_cum = (1 + portfolio_return).cumprod() * 100
    
    # Normalisation des actifs individuels pour comparaison (Base 100)
    individual_cum = (1 + returns).cumprod() * 100

    # 6. Graphique de comparaison final 
    st.subheader("📈 Performance : Portefeuille vs Actifs Individuels")
    
    comparison_df = individual_cum.copy()
    comparison_df['PORTEFEUILLE'] = portfolio_cum
    
    st.line_chart(comparison_df)

    # 7. Métriques de Risque 
    st.subheader("📉 Métriques de Risque du Portefeuille")
    col1, col2 = st.columns(2)
    
    annual_vol = portfolio_return.std() * np.sqrt(252)
    cum_return_total = (portfolio_cum.iloc[-1] / 100) - 1
    
    with col1:
        st.metric("Rendement Cumulé (1an)", f"{cum_return_total:.2%}")
    with col2:
        st.metric("Volatilité Annuelle", f"{annual_vol:.2%}")
