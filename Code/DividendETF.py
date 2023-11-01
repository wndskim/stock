import streamlit as st
import pandas as pd
import yfinance as yf


def get_info():
    ticker='schd'
    info=yf.Ticker(ticker)

    history=info.history(interval='1d',start='2013-01-01',end='2023-10-31')
    # history=pd.DataFrame(history)
    # history.Date=history.Date.strftime('%Y-%m-%d')

    st.write(history)

    return



