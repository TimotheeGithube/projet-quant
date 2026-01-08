
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.title("📈 Projet Quant – Dashboard")

ticker = st.text_input("Ticker", "AAPL")

data = yf.download(ticker, period="1y", interval="1d")

data["Return"] = data["Close"].pct_change()
volatility = data["Return"].std() * np.sqrt(252)

st.subheader("Indicateurs")
st.metric("Volatilité annuelle", f"{volatility:.2%}")

st.subheader("Prix de clôture")
st.line_chart(data["Close"])

