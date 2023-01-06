# import requests
# import time, os
# import openpyxl
# import OpenDartReader
# from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
import matplotlib as plt
import yfinance as yf

from Code import Dart

# @st.cache(suppress_st_warning=True)
def 전종목_등락률(sYear, sort_order):
    startDate=sYear+'0101'; endDate=sYear+'1231'
    st.write(startDate,'부터', endDate,'까지 가격 변동')
    df = stock.get_market_price_change(startDate, endDate, market='ALL')
    df=df[df['거래량']>0]
    df['거래대금(억)']=df['거래대금']/100000000
    df['거래대금(억)']=df['거래대금(억)'].round(0)
    df['거래대금(억)']=df['거래대금(억)'].astype(int)
    df.drop(columns =['거래대금'], inplace = True) 
    df.sort_values(by='등락률', ascending=sort_order, inplace=True)
    return df

# @st.cache(suppress_st_warning=True)
def 코스피200_등락률(sYear, sort_order):
    tickers = stock.get_index_portfolio_deposit_file("1028")
    df_all=전종목_등락률(sYear, sort_order)
    df=df_all.loc[df_all.index.isin(tickers)]
    df.sort_values(by='등락률', ascending=sort_order, inplace=True)
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
    job=st.sidebar.selectbox('선택',['선택','년도별 가격 변동률 조회','관심주 및 보유주','특징주','가격 변동률(년간)','종목별 OHLCV','인덱스 종류'])
    if job=='선택':
        schk=st.checkbox('금감원 공시내역을 확일할려면 틱 하세요..!!', value=False)
        조회일=st.date_input('조회일')
        if schk: Dart.금감원_공시내역_보기(조회일)

    if job=='년도별 가격 변동률 조회':
        년도=st.sidebar.selectbox('년도선택',('2023','2022','2021','2020','2019','2018'))
        col1, col2, col3=st.columns(3)
        with col1:
            상승하락=st.radio('상승하락선택',('상승순','하락순'))
        if 상승하락=='상승순':
            with col2:
                상승률=['상승50%까지','상승50%~100%','상승100%~150%','상승150%~200%','상승200%이상','전체']
                시트선택=st.selectbox('선택',상승률)

            if 시트선택=='상승50%까지': sheet_name=0
            elif 시트선택=='상승50%~100%': sheet_name=1
            elif 시트선택=='상승100%~150%': sheet_name=2
            elif 시트선택=='상승150%~200%': sheet_name=3
            elif 시트선택=='상승200%이상': sheet_name=4
            else: sheet_name=11

        else:
            with col2:
                하락률=['하락0%~10%','하락11%~20%','하락21%~30%','하락31%~40%','하락41%~50%','하락50%이상']
                시트선택=st.selectbox('선택',하락률)

            if 시트선택=='하락0%~10%': sheet_name=5
            elif 시트선택=='하락11%~20%': sheet_name=6
            elif 시트선택=='하락21%~30%': sheet_name=7
            elif 시트선택=='하락31%~40%': sheet_name=8
            elif 시트선택=='하락41%~50%': sheet_name=9
            else: sheet_name=10


        try:
            df=pd.read_excel(f'./Data/{년도}_종목별_년간등락.xlsx',sheet_name=sheet_name)
        except: st.write(년도,'년도는 준비되지 않았습니다.'); return

        if 상승하락=='하락순':
            df.sort_values(by=['등락률'], ascending=True, inplace=False)
        
                # df_상승률_0050.to_excel(writer, sheet_name='상승00_50', index=False, freeze_panes=(1,1)) 0
                # df_상승률_50100.to_excel(writer, sheet_name='상승50_100', index=False, freeze_panes=(1,1)) 1
                # df_상승률_100150.to_excel(writer, sheet_name='상승100_150', index=False, freeze_panes=(1,1)) 2
                # df_상승률_150200.to_excel(writer, sheet_name='상승150_200', index=False, freeze_panes=(1,1)) 3
                # df_상승률_200.to_excel(writer, sheet_name='상승200이상', index=False, freeze_panes=(1,1)) 4
                # df_하락률_0010.to_excel(writer, sheet_name='하락10까지', index=False, freeze_panes=(1,1)) 5
                # df_하락률_1120.to_excel(writer, sheet_name='하락11_20', index=False, freeze_panes=(1,1)) 6
                # df_하락률_2130.to_excel(writer, sheet_name='하락21_30', index=False, freeze_panes=(1,1)) 7
                # df_하락률_3140.to_excel(writer, sheet_name='하락31_40', index=False, freeze_panes=(1,1)) 8
                # df_하락률_4150.to_excel(writer, sheet_name='하락41_50', index=False, freeze_panes=(1,1)) 9
                # df_하락률_50.to_excel(writer, sheet_name='하락50이상', index=False, freeze_panes=(1,1)) 10
                # df_merge.to_excel(writer, sheet_name='전체', index=False, freeze_panes=(1,1)) 11

        발굴종목s=df['티머'].unique()
        st.write(시트선택, len(발굴종목s),'건')
        st.dataframe(df)

        st.selectbox('발굴종목',발굴종목s)
    
    if job=='관심주 및 보유주':
        df=pd.read_excel('./Data/관심종목.xlsx')
        df['날짜']=df['날짜'].dt.strftime('%Y-%m-%d')

        st.write('[경기상황정리](https://docs.google.com/spreadsheets/d/14OhuYvmkb3dZUIpxP9mu9uS1zNxUY3gFnafHOWOYs5o/edit#gid=719655173)')
        st.write('[기법정리](https://docs.google.com/spreadsheets/d/1tJg4kfIIpt17LNKXoKwzzallnXPmyCzMF1DhIIw1Q-8/edit#gid=1186881965)')
        st.write('[KT(030200) 보유주](https://docs.google.com/spreadsheets/d/1A_8rYBwU35sfWJezUcKGaFiofMc0cp39TZQCkdSA6Rw/edit#gid=0)')
        st.write('[유라테크(048430) 관심주](https://docs.google.com/spreadsheets/d/1IwcqZpn8_yiw-ZwX8kJW3na9d5Xy_aLY9Bv4X1WruLY/edit#gid=743352833)')

        st.dataframe(df)

    if job=='특징주':
        st.text('특징주 내역')
        df=pd.read_excel('./Data/상한가_300억이상_거래 종목.xlsx')
        df['날짜']=df['날짜'].dt.strftime('%Y-%m-%d')
        st.dataframe(df)

        종목명s=df['종목명'].unique().tolist()
        종목명=st.selectbox('티커선택',종목명s)

        df_종목=df[df['종목명']==종목명]
        st.dataframe(df_종목[['날짜','티커','종목명','사유_뉴스']])

    if job=='가격 변동률(년간)':
        s선택=st.sidebar.selectbox('선택',['전체','코스피200','코스피','코스닥'])
        sYear=st.sidebar.selectbox('선택',['선택하세요','2023','2022','2021','2020','2019','2018'])
        s_radio=st.radio("정렬순서 선택", ('상승률순', '하락률순'))
        if s_radio=='상승률순': sort_order=False
        else: sort_order=True

        if sYear=='선택하세요': return

        if s선택=='전체':
            df=전종목_등락률(sYear, sort_order)
        elif s선택=='코스피200':
            df=코스피200_등락률(sYear,sort_order)
        else: pass

        건수=len(df)+1
        st.write('총',str(건수),'건 /', s선택, s_radio)
        df.reset_index(inplace=True)
        st.dataframe(df)

        col1, col2=st.columns([1,2])
        with col1:
            티커s=df['티커'].to_list()
            티커=st.selectbox('티커선택',티커s)
        with col2:
            st.write('[NICE CompanySearch](https://comp.kisline.com/hi/HI0100M010GE.nice?stockcd={}&nav=1)'.format(티커))
            st.write('[CompanyGuide](https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701)'.format(티커))
            st.write('[네이버금융(종합정보)](https://finance.naver.com/item/main.naver?code={})'.format(티커))
            st.write('[ZOOM검색](https://search.zum.com/search.zum?method=uni&query={}&qm=f_instant.top)'.format(티커))
            st.write('[다음통합검색](https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q={})'.format(티커))

    if job=='인덱스 종류':
        for ticker in stock.get_index_ticker_list():
            st.write(ticker, stock.get_index_ticker_name(ticker))

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





