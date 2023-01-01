# import requests
# import time, os
import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
import matplotlib as plt
# import yfinance as yf

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
job=st.sidebar.selectbox('선택',['선택','종목별 OHLCV', '코스피200','인덱스 종류', '특징주 보기'])
if job=='선택': pass

if job=='인덱스 종류':
    for ticker in stock.get_index_ticker_list():
        st.write(ticker, stock.get_index_ticker_name(ticker))

if job=='코스피200':
    tickers = stock.get_index_portfolio_deposit_file("1028")
    for i, ticker in enumerate(tickers):
        st.write(i, ticker, stock.get_market_ticker_name(ticker))



# # Get the data for the stock Apple by specifying the stock ticker, start date, and end date
# data = yf.download('005930.KS', start='2020-01-01', end='2022-12-31')

# # Print the data
# print(data)


# url = 'https://gitlab.com/wndskim/repo/-/raw/master/data.xlsx'
# url = 'https://gitlab.com/wndskim/stock/main/상한가_300억이상_거래 종목.xlsx'
# url='https://github.com/wndskim/stock/blob/b9b1d3205b052c18a7a67c4c3e8b88948238b522/data.xlsx'
# data = pd.read_excel('/wndskim/stock/main/상한가_300억이상_거래 종목.xlsx','Sorted')

# url = 'https://github.com/wndskim/stock/blob/main/data.xlsx'
# data = pd.read_excel(url,'Sorted')

# st.dataframe(data)

# Read the Excel file from GitHub
# df = pd.read_excel('https://github.com/YourGitHubName/YourRepositoryName/YourExcelFileName.xlsx')

# Print the contents of the Excel file
# print(df)



# st.write('2022년12월1일부터 2022년12월29일까지 전종목 가격 변동 - 하락률 순')
# df = stock.get_market_price_change("20221201", "20221231", market='ALL')
# df.sort_values(by='등락률', ascending=True, inplace=True)

# st.write('총',len(df),'건')
# st.dataframe(df)

