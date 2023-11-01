import streamlit as st
import pandas as pd
import yfinance as yf


def get_info():
    ticker='SCHD'
    info=yf.Ticker(ticker)

    history=info.history()
    # history=pd.DataFrame(history)
    # history.Date=history.Date.strftime('%Y-%m-%d')

    st.write(history)

    return



