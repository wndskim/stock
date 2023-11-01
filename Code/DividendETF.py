import streamlit as st
import pandas as pd
import yfinance as yf


def get_info():
    ticker='TSLY'
    info=yf.Ticker(ticker)

    history=pd.DataFrame(info.history())
    history.Date=history.Date.strftime('%Y-%m-%d')

    st.write(history)

    return



