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
import datetime
from datetime import date, timedelta
from Code import Dart, Chart, Strategy

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

def 참조링크보기(티커):
    st.write('[NICE CompanySearch](https://comp.kisline.com/hi/HI0100M010GE.nice?stockcd={}&nav=1)'.format(티커))
    st.write('[CompanyGuide](https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701)'.format(티커))
    st.write('[네이버금융(종합정보)](https://finance.naver.com/item/main.naver?code={})'.format(티커))
    st.write('[ZOOM검색](https://search.zum.com/search.zum?method=uni&query={}&qm=f_instant.top)'.format(티커))
    st.write('[다음통합검색](https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q={})'.format(티커))
    return

def get_date(기준일, delta):
    return (기준일 - timedelta(days=delta)).strftime("%Y-%m-%d")

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
    job=st.sidebar.selectbox('선택',['선택','년도별 가격 변동률 조회','관심주 및 보유주','특징주','매매기술 설명 보기',\
                             '가격 변동률(년간)','종목별 OHLCV','인덱스 종류'])

    if job=='매매기술 설명 보기':
        Strategy.Define_매매기술_설명()
        return

    조회일=st.date_input('조회일')

    if job=='선택':

        # chk0=st.checkbox('2023년 1분기 매매 전략 보기',value=False)
        # if chk0:
        #     col1, col2=st.columns(2)
        #     with col1:
        #         st.markdown('''
        #                 ##### :orange[시장평가 기준]
        #                 ###### :red[1. 코스피의 PBR이 1.2 이상이면 미친 고평가]
        #                 ###### :blue[2. 코스피의 PBR이 1 이하이면 저평가]
        #                 ###### :green[3. 코스피의 PBR이 0.9 이하이면 폭락장/하락장]
        #             ''')
        #     with col2:
        #         st.markdown('''
        #                 ##### :orange[2023년 1월9일 현재 바닥을 확인후 반등중임]
        #                 ###### :orange[기술적 지표(rsi(10): 침체구간(30이하), 볼린저밴드(40,2): 하단선 하향 돌파)]
        #                 ###### :orange[주식시장의 저평가: 0.9이하 + 기술적 저점일때 적극적으로 매매]
        #                 ###### :orange[위의 3가지 요건이 만족되면 몰빵한다.]
        #                 ##### :violet[일반적 통계를 활용한 매매 방법]
        #                 ###### :green[1월 진입 3,4월 매도(코스닥이 코스피보다 좋다, 개별주(중소형주)위주로 매매)]
        #                 ###### :green[1월~3월 매수, 4월에 매도]
        #                 ###### :green[장단기 금리차 역전이 해소 된 후 3~7개월내에 폭락장 나올 수 있음]
        #                 ###### :green[5월~10월은 폭락장이 나올 수 있으므로 콥버스 매수하거나, 조심해야 된다]
        #                 ###### :green[폭락장 나오면 매수 후 12월까지 보유하면 큰 수익이 가능할 것으로 생각된다]
        #             ''')

        chk1=st.checkbox('금감원 공시내역을 확일할려면 틱 하세요..!!', value=False)
        if chk1:
            Dart.금감원_공시내역_보기(조회일)

        chk2=st.checkbox('시장지표를 확인할려면 틱 하세요..!!', value=False)
        if chk2:
            시작일=str(get_date(조회일, 20)).replace('-','')  # 조회일로부터 20일전 부터 데이타 가져오기
            종료일=str(조회일).replace('-','')
            df_kospi=Dart.Index_Fundamental_조회(시작일,종료일,'코스피')
            df_kosdaq=Dart.Index_Fundamental_조회(시작일,종료일,'코스닥')

            # kospi_pbr=df_kospi._get_value(13, 'PBR')
            df_kospi['PBR']=df_kospi['PBR'].astype(float)
            kospi_pbr=df_kospi['PBR'].iloc[0]

            df_index=Dart.Index_OHLCV_조회(str(get_date(조회일, 250)).replace('-',''),종료일, '1001') # 250일전 날짜 구해서 작업 수행

            kospi_rsi=df_index['rsi'].iloc[-1].round(2)
            kospi_bbl=df_index['bb_bbl'].iloc[-1].round(2)
            kospi_지수=df_index['종가'].iloc[-1].round(2)

            if (kospi_pbr < 0.9): 시장상태='폭락장인 상태이다'
            elif (kospi_pbr > 0.89999) and (kospi_pbr < 1.0): 시장상태='정상적인 상태이다'
            elif (kospi_pbr > 0.99999) and (kospi_pbr < 1.2): 시장상태=' 고평가 상태이다'
            else: 시장상태=' 매우 고평가 상태이다'
            st.markdown(f'''###### :orange[{조회일}일 기준으로 PBR이 {kospi_pbr}이므로 {시장상태}]''')

            col1, col2, col3, col4, col5=st.columns(5)
            with col1:
                st.markdown(f'''
                            ###### :orange[1. 코스피지수: {kospi_지수}]
                    ''')
            with col2:
                st.markdown(f'''
                            ###### :violet[4. 볼리저밴드 하단선: {kospi_bbl}]
                    ''')
            with col3:
                st.markdown(f'''
                            ###### :green[2. PBR: {kospi_pbr}]
                    ''')
            with col4:
                st.markdown(f'''
                            ###### :blue[3. RSI: {kospi_rsi}]
                    ''')

            # st.dataframe(df_index)

            col1, col2=st.columns(2)
            with col1:
                # st.dataframe(df_kospi)
                chk3=st.checkbox('코스피 PBR 차트보기',value=False)
                if chk3: Chart.Chart_001(df_kospi)
            # with col2:
                # st.dataframe(df_kosdaq)

            chk4=st.checkbox('2023년 투자전략 보기', value=False)
            if chk4:
                Strategy.Strategy_2023_01(kospi_pbr)

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
            df["티커"] = df["티커"].apply(lambda x: str(x).zfill(6))
        except: st.write(년도,'년도는 준비되지 않았습니다.'); return

        if 상승하락=='하락순':
            df.sort_values(by=['등락률'], ascending=False, inplace=False)
        
        # 발굴종목s=df['티커'].unique()
        종목명s=df['종목'].unique()
        st.write(시트선택, len(종목명s),'종목')
        st.dataframe(df)

        종목=st.selectbox('발굴종목',종목명s)
        티커=df[df['종목']==종목]['티커'].values[0]
        col1, col2, col3=st.columns(3)
        with col1:
            참조링크보기(티커)
        with col2:
            재무정보=Dart.get_CompanyGuide자료(티커).transpose()
            col_names=재무정보.columns

            if len(재무정보)>0:
                for col_name in col_names:
                    재무정보.loc[:, col_name] = 재무정보[col_name].map('{:.2f}'.format)

                st.dataframe(재무정보)
        with col3:
            시작일=str(get_date(조회일, 2000)).replace('-','')
            종료일=str(조회일).replace('-','')
            펀더멘털=Dart.Stock_Fundamental_조회(시작일, 종료일, 티커)

            st.dataframe(펀더멘털)
    
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





