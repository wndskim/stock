# import requests
# import time, os
import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
import matplotlib as plt

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# scope=['https://www.googleapis.com/auth/spreadsheets',
#        'https://www.googleapis.com/auth/drive.file',
#        'https://spreadsheets.google.com/feeds',
#        'https://www.googleapis.com/auth/drive']
# creds=ServiceAccountCredentials.from_json_keyfile_name('wndskim/stock/credentials.json',scope)
# client=gspread.authorize(creds)





# st.title('This is title')
# st.header('This is header')
# st.subheader('This is subheader')
# st.text('This is text')
# st.caption('This is caption')


# Side Bar 생성
job=st.sidebar.selectbox('선택',['선택','코스피200','인덱스 종류', '특징주 보기'])
if job=='선택': pass

if job=='인덱스 종류':
    for ticker in stock.get_index_ticker_list():
        st.write(ticker, stock.get_index_ticker_name(ticker))

if job=='코스피200':
    tickers = stock.get_index_portfolio_deposit_file("1028")
    for i, ticker in enumerate(tickers):
        st.write(i, ticker, stock.get_market_ticker_name(ticker))

# url = 'https://gitlab.com/wndskim/repo/-/raw/master/data.xlsx'
url = 'https://gitlab.com/wndskim/상한가_300억이상_거래 종목.xlsx'

data = pd.read_excel(url)

st.dataframe(data)



# st.write('2022년12월1일부터 2022년12월29일까지 전종목 가격 변동 - 하락률 순')
# df = stock.get_market_price_change("20221201", "20221231", market='ALL')
# df.sort_values(by='등락률', ascending=True, inplace=True)

# st.write('총',len(df),'건')
# st.dataframe(df)

