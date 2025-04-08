import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="India Macro Dashboard", layout="wide")
st.title("India Macro Market Dashboard")
st.markdown("Real-time trends in macroeconomic indicators impacting Indian stock markets.")

@st.cache_data(ttl=3600)
def get_data():
    data = {}
    nifty = yf.Ticker("^NSEI")
    data["Nifty"] = nifty.history(period="6mo")["Close"]
    
    usd_inr = yf.Ticker("INR=X")
    data["USDINR"] = usd_inr.history(period="6mo")["Close"]
    
    return data

data = get_data()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Nifty 50 Trend")
    st.line_chart(data["Nifty"])

with col2:
    st.subheader("USD/INR Trend")
    st.line_chart(data["USDINR"])

st.subheader("Market Insight Summary")

nifty_change = data["Nifty"].iloc[-1] - data["Nifty"].iloc[0]
inr_change = data["USDINR"].iloc[-1] - data["USDINR"].iloc[0]

nifty_trend = "increased" if nifty_change > 0 else "decreased"
inr_trend = "weakened" if inr_change > 0 else "strengthened"

st.markdown(f"""
- **Nifty 50** has {nifty_trend} by **{nifty_change:.2f} points** in the last 6 months.
- **INR** has {inr_trend} against USD by **{abs(inr_change):.2f}**.
""")

if inr_change > 0:
    st.info("Rupee weakening: Export-oriented sectors (IT, Pharma) may benefit.")
else:
    st.info("Rupee strength: Positive for importers and broader market stability.")

if nifty_change < 0:
    st.warning("Equity market appears under pressure. Consider defensive sectors.")
