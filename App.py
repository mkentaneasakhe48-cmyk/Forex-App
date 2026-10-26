import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Forex Analyser", page_icon="💱")
st.title("💱 My Forex Analyser")
st.write("Forex BUY/SELL - by you")

pairs = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "USD/ZAR (Dollar-Rand)": "ZAR=X",
    "EUR/ZAR": "EURZAR=X",
    "GBP/ZAR": "GBPZAR=X",
    "Gold (XAU/USD)": "GC=F",
}

choice = st.selectbox("Select Forex Pair", list(pairs.keys()))
symbol = pairs[choice]

data = yf.download(symbol, period="6mo", interval="1d", auto_adjust=True, progress=False)

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

close = data['Close'].dropna()

if len(close) >= 20:
    data['SMA20'] = close.rolling(20).mean()
    data['SMA50'] = close.rolling(50).mean()
    data['RSI'] = ta.momentum.RSIIndicator(close).rsi()
    
    last = data.iloc[-1]
    rsi = float(last['RSI'])
    price = float(last['Close'])
    sma20 = float(last['SMA20'])
    sma50 = float(last['SMA50'])

    if rsi < 30 and price > sma20:
        signal = "BUY 🟢"
    elif rsi > 70 and price < sma20:
        signal = "SELL 🔴"
    elif sma20 > sma50:
        signal = "BUY 🟢 - Uptrend"
    else:
        signal = "SELL 🔴 - Downtrend"
    
    st.metric(f"{choice} Price", f"{price:.5f}")
    st.header(signal)
    st.write(f"RSI: {rsi:.1f} | SMA20: {sma20:.5f} | SMA50: {sma50:.5f}")
    st.line_chart(data[['Close','SMA20','SMA50']])
else:
    st.warning("Loading data...")
