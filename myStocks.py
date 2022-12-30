# import requests
# import time, os
import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
import matplotlib as plt

st.subheader('민정희 이것  잘 보여?????')
st.title('This is title')
st.header('This is header')
st.subheader('This is subheader')
st.text('This is text')
st.caption('This is caption')

st.subheader('2022년12월1일부터 2022년12월29일까지 전종목 가격 변동 - 하락률 순')
df = stock.get_market_price_change("20221201", "20221231", market='ALL')
df.sort_values(by='등락률', ascending=True, inplace=True)

st.dataframe(df)

