# import requests
# import time, os
import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
import matplotlib as plt
import yfinance as yf
import openpyxl

@st.cache(suppress_st_warning=True)
def 전종목_등락률(sYear):
    startDate=sYear+'0101'; endDate=sYear+'1231'
    st.write(startDate,'부터', endDate,'까지 전종목 가격 변동')
    df = stock.get_market_price_change(startDate, endDate, market='ALL')
    df=df[df['거래량']>0]
    df['거래대금(억)']=df['거래대금']/100000000
    df['거래대금(억)']=df['거래대금(억)'].round(0)
    df.sort_values(by='등락률', ascending=False, inplace=True)
    return df

@st.cache(suppress_st_warning=True)
def 코스피200_등락률(sYear):
    tickers = stock.get_index_portfolio_deposit_file("1028")
    df_all=전종목_등락률(sYear)
    df=df_all.loc[df_all.index.isin(tickers)]
    df.sort_values(by='등락률', ascending=False, inplace=True)
    return df

##############################################################
# ##### Main
##############################################################
def main():
    # st.set_page_config(page_title='My Stock Management',
    # st.set_page_config(layout='wide'
    #                 )

    version=st.__version__
    st.markdown(f'''
                #### My Stock Management System(Web Version)
                streamlit version is {version}
                ''')

    # Side Bar 생성
    job=st.sidebar.selectbox('선택',['선택','가격 변동률','종목별 OHLCV','인덱스 종류', '특징주 보기'])
    if job=='선택': pass

    if job=='인덱스 종류':
        for ticker in stock.get_index_ticker_list():
            st.write(ticker, stock.get_index_ticker_name(ticker))

    if job=='가격 변동률':
        s선택=st.sidebar.selectbox('선택',['전체','코스피200','코스피','코스닥'])
        sYear=st.selectbox('선택',['2023','2022','2021','2020','2019','2018'])

        if s선택=='전체':
            df=전종목_등락률(sYear)
        elif s선택=='코스피200':
            df=코스피200_등락률(sYear)

        else: pass


        건수=len(df)+1
        st.write('총',str(건수),'건')
        st.text('상승률순')
        st.dataframe(df)

        st.text('하락률순')
        df.sort_values(by='등락률', ascending=True, inplace=True)
        st.dataframe(df)


    return

#####################################################
##### Main ##########################################
#####################################################
if __name__ == '__main__':
    main()





# df=yf.download('005930.KS', start='2012-01-01', end='2022-12-31', interval='1mo')

# st.dataframe(df)




######################################################################################################################
# file_upload = st.file_uploader("data", type="xlsx")
# st.write(pd.read_excel(file_upload), index=False)
######################################################################################################################
# st.write('Download 삼성 Historical Data..!!')

# # Get the data for the stock Apple by specifying the stock ticker, start date, and end date
# data = yf.download('005930.KS', start='2020-01-01', end='2022-12-31')
# data.reset_index(inplace=True)
# data.to_csv('./samsung.csv', index=False)

# # data.to

# # Print the data
# st.dataframe(data)
#####################################################################################################################
# url = 'https://github.com/wndskim/stock/blob/main/data.xlsx'
# data = pd.read_excel(url)

# st.dataframe(data)
######################################################################################################################

# Read the Excel file from GitHub
# df = pd.read_excel('https://github.com/YourGitHubName/YourRepositoryName/YourExcelFileName.xlsx')

# Print the contents of the Excel file
# print(df)





