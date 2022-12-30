# import requests
# import time, os
import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock

st.title('This is title')
st.header('This is header')
st.subheader('This is subheader')
st.text('This is text')
st.caption('This is caption')

df = stock.get_market_price_change("20220901", "20221130", market='ALL')

st.dataframe(df)

