import streamlit as st
import pandas as pd
import yfinance as yf

ticker='TSLY'
info=yf.Ticker(ticker)

history=info.history()

st.write(history)



