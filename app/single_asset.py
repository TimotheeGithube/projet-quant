import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

def run_quant_a():
    st.title("📈 Module A – Single Asset Analysis & Backtesting")

    # 1. Asset selection
    ticker = st.text_input(
        "Enter a ticker (e.g. AAPL, BTC-USD, ENGI.PA)",
        "AAPL"
    )

    # 2. Data download
    data = yf.download(ticker, period="2y", interval="1d")

    if data.empty:
        st.error("No data found. Please check the ticker.")
        return

    # Clean multi-index columns if needed
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # 3. Basic indicators
    data["Returns"] = data["Close"].pct_change()

    # 4. Backtesting strategy choice
    st.subheader("🛠️ Backtesting Strategy")
    strat_choice = st.selectbox(
        "Choose a strategy",
        ["Buy & Hold", "Moving Average Crossover"]
    )

    if strat_choice == "Buy & Hold":
        data["Strategy_Returns"] = data["Returns"]

    elif strat_choice == "Moving Average Crossover":
        short_window = st.slider("Short window", 10, 50, 20)
        long_window = st.slider("Long window", 51, 200, 100)

        data["SMA_Short"] = data["Close"].rolling(window=short_window).mean()
        data["SMA_Long"] = data["Close"].rolling(window=long_window).mean()

        # Signal generation: 1 if short SMA > long SMA, else 0
        data["Signal"] = np.where(
            data["SMA_Short"] > data["SMA_Long"],
            1,
            0
        )
        data["Strategy_Returns"] = data["Signal"].shift(1) * data["Returns"]

    # 5. Cumulative performance
    data["Cum_Asset"] = (1 + data["Returns"]).cumprod()
    data["Cum_Strategy"] = (1 + data["Strategy_Returns"].fillna(0)).cumprod()

    # 6. Metrics display
    col1, col2, col3 = st.columns(3)
    sharpe = (
        (data["Strategy_Returns"].mean() / data["Strategy_Returns"].std()) * np.sqrt(252)
        if data["Strategy_Returns"].std() != 0
        else 0
    )
    drawdown = (data["Cum_Strategy"] / data["Cum_Strategy"].cummax() - 1).min()

    col1.metric("Sharpe Ratio", f"{sharpe:.2f}")
    col2.metric("Max Drawdown", f"{drawdown:.2%}")
    col3.metric(
        "Strategy Return",
        f"{(data['Cum_Strategy'].iloc[-1] - 1):.2%}"
    )

    # 7. Main chart (Asset vs Strategy)
    st.subheader("📈 Comparison: Asset vs Strategy (Base 1)")
    st.line_chart(data[["Cum_Asset", "Cum_Strategy"]])

    # Bonus option: Moving averages on price
    if st.checkbox("Display moving averages on price"):
        st.line_chart(
            data[["Close", "SMA_Short", "SMA_Long"]].dropna()
            if strat_choice == "Moving Average Crossover"
            else data["Close"]
        )
