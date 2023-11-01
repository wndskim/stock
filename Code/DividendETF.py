import streamlit as st
import pandas as pd
import yfinance as yf


def get_info():
    ticker='TSLY'
    info=yf.Ticker(ticker)

    history=info.history()

    st.write(history)

    return



