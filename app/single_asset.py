import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

def run_quant_a():
    st.title("📈 Module A - Analyse Mono-Actif & Backtesting")

    # 1. Sélection de l'actif [cite: 32]
    ticker = st.text_input("Entrez un Ticker (ex: AAPL, BTC-USD, ENGI.PA)", "AAPL")
    
    # 2. Récupération des données [cite: 15, 19]
    data = yf.download(ticker, period="2y", interval="1d")
    
    if data.empty:
        st.error("Aucune donnée trouvée. Vérifiez le ticker.")
        return

    # Nettoyage pour yfinance multi-index si nécessaire
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # 3. Calcul des indicateurs de base [cite: 22, 34]
    data['Returns'] = data['Close'].pct_change()
    
    # 4. Choix de la stratégie de Backtesting 
    st.subheader("🛠️ Stratégie de Backtesting")
    strat_choice = st.selectbox("Choisir une stratégie", ["Buy & Hold", "Moving Average Crossover"])
    
    if strat_choice == "Buy & Hold":
        data['Strategy_Returns'] = data['Returns']
    
    elif strat_choice == "Moving Average Crossover":
        short_window = st.slider("Fenêtre courte", 10, 50, 20)
        long_window = st.slider("Fenêtre longue", 51, 200, 100)
        
        data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
        data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
        
        # Génération du signal : 1 si SMA courte > SMA longue, sinon 0 
        data['Signal'] = np.where(data['SMA_Short'] > data['SMA_Long'], 1, 0)
        data['Strategy_Returns'] = data['Signal'].shift(1) * data['Returns']

    # 5. Calcul de la performance cumulative 
    data['Cum_Asset'] = (1 + data['Returns']).cumprod()
    data['Cum_Strategy'] = (1 + data['Strategy_Returns'].fillna(0)).cumprod()

    # 6. Affichage des Métriques 
    col1, col2, col3 = st.columns(3)
    sharpe = (data['Strategy_Returns'].mean() / data['Strategy_Returns'].std()) * np.sqrt(252) if data['Strategy_Returns'].std() != 0 else 0
    drawdown = (data['Cum_Strategy'] / data['Cum_Strategy'].cummax() - 1).min()
    
    col1.metric("Sharpe Ratio", f"{sharpe:.2f}") 
    col2.metric("Max Drawdown", f"{drawdown:.2%}") 
    col3.metric("Rendement Stratégie", f"{(data['Cum_Strategy'].iloc[-1]-1):.2%}")

    # 7. Graphique principal (Prix vs Stratégie) [cite: 20, 35]
    st.subheader("📈 Comparaison : Actif vs Stratégie (Base 1)")
    st.line_chart(data[['Cum_Asset', 'Cum_Strategy']]) 

    # Option Bonus: Simple Moving Average sur le prix [cite: 36]
    if st.checkbox("Afficher les Moyennes Mobiles sur le prix"):
        st.line_chart(data[['Close', 'SMA_Short', 'SMA_Long']].dropna() if strat_choice == "Moving Average Crossover" else data['Close'])
