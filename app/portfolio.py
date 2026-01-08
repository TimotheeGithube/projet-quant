import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def run_quant_b():
    st.title("📊 Module B – Multi-Asset Portfolio Management")
    st.markdown(
        "This module allows you to simulate an asset allocation and analyze correlations."
    )

    # 1. Asset selection (Requirement: at least 3)
    available_tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
        "BTC-USD", "ETH-USD", "GC=F", "EURUSD=X"
    ]
    tickers = st.multiselect(
        "Select at least 3 assets for your portfolio",
        available_tickers,
        default=["AAPL", "BTC-USD", "GC=F"]
    )

    if len(tickers) < 3:
        st.warning("⚠️ Please select at least 3 assets to validate this module.")
        return

    # 2. Market data download
    with st.spinner("Downloading market data..."):
        data = yf.download(tickers, period="1y")["Close"]

    if data.empty:
        st.error("Error while downloading market data.")
        return

    # 3. Strategy parameters (Asset weights)
    st.subheader("⚙️ Allocation settings")
    cols = st.columns(len(tickers))
    weights = []

    for i, col in enumerate(cols):
        with col:
            w = st.number_input(
                f"Weight {tickers[i]}",
                min_value=0.0,
                max_value=1.0,
                value=1.0 / len(tickers),
                step=0.05
            )
            weights.append(w)

    # Weight sum check
    total_weight = sum(weights)
    st.info(f"Total weight sum: **{total_weight:.2f}**")
    if abs(total_weight - 1.0) > 0.001:
        st.warning("⚠️ The sum of weights should ideally be equal to 1 (100%).")

    # 4. Returns and correlation calculations
    returns = data.pct_change().dropna()

    # Correlation matrix
    st.subheader("🔗 Correlation Analysis")
    corr_matrix = returns.corr()
    fig_corr, ax_corr = plt.subplots(figsize=(8, 5))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="RdYlGn",
        center=0,
        ax=ax_corr
    )
    st.pyplot(fig_corr)

    # 5. Portfolio performance simulation
    portfolio_return = (returns * weights).sum(axis=1)

    # Cumulative value (Base 100)
    portfolio_cum = (1 + portfolio_return).cumprod() * 100

    # Individual assets normalized (Base 100)
    individual_cum = (1 + returns).cumprod() * 100

    # 6. Final comparison chart
    st.subheader("📈 Performance: Portfolio vs Individual Assets")

    comparison_df = individual_cum.copy()
    comparison_df["PORTFOLIO"] = portfolio_cum

    st.line_chart(comparison_df)

    # 7. Portfolio risk metrics
    st.subheader("📉 Portfolio Risk Metrics")
    col1, col2 = st.columns(2)

    annual_vol = portfolio_return.std() * np.sqrt(252)
    cum_return_total = (portfolio_cum.iloc[-1] / 100) - 1

    with col1:
        st.metric("Cumulative Return (1Y)", f"{cum_return_total:.2%}")
    with col2:
        st.metric("Annualized Volatility", f"{annual_vol:.2%}")
