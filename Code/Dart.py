import requests
import OpenDartReader
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pykrx import stock
import ta
from ta.volatility import BollingerBands
from ta.momentum import rsi

API_KEY="d538a1a0a4263cb8fbfa06a7429937ea86fc1aa1"
dart=OpenDartReader(API_KEY)
# @st.cache(suppress_st_warning=True)
def 금감원_공시내역_보기(조회일):
    # 금일 금강원 공시 내역
    # today=datetime.now().strftime('%Y%m%d')
    조회일=조회일.strftime('%Y%m%d')
    df=dart.list(start=조회일, end=조회일, final=False)
    if len(df)<1: st.text('금일 공시내역 없음..!!'); return

    df['날짜']=df['rcept_dt']
    df['티커']=df['stock_code']
    df['종목명']=df['corp_name']
    df['공시내용']=df['report_nm']

    df=df.drop(['corp_code','corp_name','stock_code','corp_cls','report_nm','rcept_no','rcept_dt'], axis=1)
    df = df.reindex(columns = ['날짜','티커','종목명','공시내용'])

    st.markdown('-----')
    st.text('금일 금감원 공시 건수:'+str(len(df))+'건')
    st.dataframe(df)
    return

def Stock_Fundamental_조회(시작일, 종료일, 티커):
    펀더멘털=stock.get_market_fundamental(시작일,종료일, 티커, freq='y')
    펀더멘털['년도'] = pd.DatetimeIndex(펀더멘털.index).year
    펀더멘털.reset_index(inplace=True)
    펀더멘털.set_index('년도', inplace=True)
    펀더멘털.drop('날짜', axis=1, inplace=True)
    펀더멘털.sort_index(inplace=True, ascending=False)
    펀더멘털.loc[:, "PER"] = 펀더멘털["PER"].map('{:.2f}'.format)
    펀더멘털.loc[:, "PBR"] = 펀더멘털["PBR"].map('{:.2f}'.format)
    펀더멘털.loc[:, "DIV"] = 펀더멘털["DIV"].map('{:.2f}'.format)
    펀더멘털.loc[:, "BPS"] = 펀더멘털["BPS"].map('{:,d}'.format)
    펀더멘털.loc[:, "EPS"] = 펀더멘털["EPS"].map('{:,d}'.format)
    펀더멘털.loc[:, "DPS"] = 펀더멘털["DPS"].map('{:,d}'.format)
    return 펀더멘털

def Index_Fundamental_조회(시작일, 종료일, 마켓):
    if 마켓=='코스피': market='1001'
    else: market='2001' # 코스닥
    df=stock.get_index_fundamental(시작일, 종료일, market)
    df.drop(['선행PER'], inplace=True, axis=1)
    df.reset_index(inplace=True)
    df.sort_values(by='날짜',ascending=False,inplace=True)
    df['날짜']=df['날짜'].dt.strftime('%Y-%m-%d')
    df['종가'] = df['종가'].map('{:,.2f}'.format)
    df['등락률'] = df['등락률'].map('{:,.2f}'.format)
    df['PER'] = df['PER'].map('{:,.2f}'.format)
    df['PBR'] = df['PBR'].map('{:,.2f}'.format)
    df['배당수익률'] = df['배당수익률'].map('{:,.2f}'.format)
    return df

def Index_OHLCV_조회(시작일, 종료일, idx):

    df=stock.get_index_ohlcv(시작일, 종료일, idx)
    df.reset_index(inplace=True)
    df['날짜']=df['날짜'].dt.strftime('%Y-%m-%d')
    df['거래대금(억)']=df['거래대금']/100000000
    df['상장시가총액(억)']=df['상장시가총액']/100000000

    df['거래대금(억)']=df['거래대금(억)'].map('{:,.2f}'.format)
    df['상장시가총액(억)']=df['상장시가총액(억)'].map('{:,.2f}'.format)
    df.drop(['거래대금','상장시가총액'], inplace=True, axis=1)

    df['rsi']=rsi(close=df['종가'],window=10)
    indicator_bb = BollingerBands(close=df["종가"], window=40, window_dev=2)
    df['bb_bbm'] = indicator_bb.bollinger_mavg()
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()

    return df

def Stock_OHLCV_조회(시작일, 종료일, 티커, freq):
    data=stock.get_market_ohlcv(시작일,종료일, 티커, freq)
    data.reset_index(inplace=True)
    data['날짜']=data['날짜'].dt.strftime('%Y-%m-%d')
    data['등락']=data.종가.diff(periods=1)
    data['등락률']=data.종가.pct_change(periods=1)*100

    if freq=='y':
        data['sma3']=ta.trend.sma_indicator(data.종가, window=3)
        data['이격률3']=data['종가']/data['sma3']*100
        
    if freq=='d':
        data['Low52']=data.저가.rolling(min_periods=1, window=262, center=False).min()
        data['High52']=data.고가.rolling(min_periods=1, window=262, center=False).max()
        data['Mid52']=(data['High52']+data['Low52'])/2

        data['sma5']=ta.trend.sma_indicator(data.종가, window=5)
        data['sma10']=ta.trend.sma_indicator(data.종가, window=10)
        data['sma20']=ta.trend.sma_indicator(data.종가, window=20)
        data['sma60']=ta.trend.sma_indicator(data.종가, window=60)
        data['sma120']=ta.trend.sma_indicator(data.종가, window=120)
        data['sma240']=ta.trend.sma_indicator(data.종가, window=240)

        data['rsi10']=rsi(close=data['종가'],window=10)
        indicator_bb = BollingerBands(close=data["종가"], window=40, window_dev=2)
        data['bb_bbm'] = indicator_bb.bollinger_mavg()
        data['bb_bbh'] = indicator_bb.bollinger_hband()
        data['bb_bbl'] = indicator_bb.bollinger_lband()

    return data

def get_CompanyGuide자료(ticker):

    df=pd.DataFrame()

    try:
        ### 재무제표
        url=f'https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701'
        page=requests.get(url)
        tables=pd.read_html(page.text)

        손익계산서=tables[0]
        손익계산서=손익계산서.set_index(손익계산서.columns[0])

        재무상태표=tables[2]
        재무상태표=재무상태표.set_index(재무상태표.columns[0])

        현금흐름표=tables[4]
        현금흐름표=현금흐름표.set_index(현금흐름표.columns[0])

        ### 재무비율
        url=f'https://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=104&stkGb=701'
        page=requests.get(url)
        tables=pd.read_html(page.text)
        재무비율=tables[0]
        재무비율=재무비율.set_index(재무비율.columns[0])

        ### 재무제표
        # 팻도시 5원칙 체크사항용(ROE>15%, ROA>7%, ROIC>7%~15%, 당기순이익/매출액*100>15, 잉여현금흐름(FCF)/매출액*100>5, 재고자산회전율)
        매출액=손익계산서.loc[['매출액']]
        당기순이익=손익계산서.loc[['당기순이익']]

        영업활동FCF=현금흐름표.loc[['영업활동으로인한현금흐름']]
        영업활동FCF=영업활동FCF.astype(float)
        투자활동FCF=현금흐름표.loc[['투자활동으로인한현금흐름']]
        투자활동FCF=투자활동FCF.astype(float)

        # st.write(영업활동FCF)
        # st.write(투자활동FCF)
        
        # 벤자민 그레이엄 적정가치 계산용 항목
        # 유동자산
        # 총부채
        # 유동부채
        유동자산=재무상태표.loc[['유동자산계산에 참여한 계정 펼치기']]
        유동자산=유동자산.astype(float)
        유동부채=재무상태표.loc[['유동부채계산에 참여한 계정 펼치기']]
        유동부채=유동부채.astype(float)
        총부채=재무상태표.loc[['부채']]
        총부채=총부채.astype(float)

        # 안정성비율(재무건전성)
        # 유동비율=유동자산/유동부채 > 150%
        # 당좌비율=(유동자산-재고자산)/유동부채 > 100%
        # 부채비율 < 100%
        # 이자보상배율 > 2
        유동비율=재무비율.loc[['유동비율계산에 참여한 계정 펼치기']]
        col_name=유동비율.columns.to_list()[:1][0]
        유동비율.drop(col_name, axis=1, inplace=True)
        유동비율=유동비율.astype(float)

        당좌비율=재무비율.loc[['당좌비율계산에 참여한 계정 펼치기']]
        col_name=당좌비율.columns.to_list()[:1][0]
        당좌비율.drop(col_name, axis=1, inplace=True)
        당좌비율=당좌비율.astype(float)

        부채비율=재무비율.loc[['부채비율계산에 참여한 계정 펼치기']]
        col_name=부채비율.columns.to_list()[:1][0]
        부채비율.drop(col_name, axis=1, inplace=True)
        부채비율=부채비율.astype(float)

        이자보상배율=재무비율.loc[['이자보상배율계산에 참여한 계정 펼치기']]
        col_name=이자보상배율.columns.to_list()[:1][0]
        이자보상배율.drop(col_name, axis=1, inplace=True)
        이자보상배율=이자보상배율.astype(float)

        # 성장성 비율
        # 매출액증가율
        # 판매관리비증가율
        # 영업이익증가율
        매출액증가율=재무비율.loc[['매출액증가율계산에 참여한 계정 펼치기']]
        col_name=매출액증가율.columns.to_list()[:1][0]
        매출액증가율.drop(col_name, axis=1, inplace=True)
        매출액증가율=매출액증가율.astype(float)

        판매비와관리비증가율=재무비율.loc[['판매비와관리비증가율계산에 참여한 계정 펼치기']]
        col_name=판매비와관리비증가율.columns.to_list()[:1][0]
        판매비와관리비증가율.drop(col_name, axis=1, inplace=True)
        판매비와관리비증가율=판매비와관리비증가율.astype(float)

        영업이익증가율=재무비율.loc[['영업이익증가율계산에 참여한 계정 펼치기']]
        col_name=영업이익증가율.columns.to_list()[:1][0]
        영업이익증가율.drop(col_name, axis=1, inplace=True)
        영업이익증가율=영업이익증가율.astype(float)
        # 수익성 비율
        # 매출총이익율
        # 세전계속사업이익률
        # 영업이익률
        # ROA > 7%
        # ROE > 15%
        # ROIC > 7%~15%
        매출총이익율=재무비율.loc[['매출총이익율계산에 참여한 계정 펼치기']]
        col_name=매출총이익율.columns.to_list()[:1][0]
        매출총이익율.drop(col_name, axis=1, inplace=True)
        매출총이익율=매출총이익율.astype(float)

        세전계속사업이익률=재무비율.loc[['세전계속사업이익률계산에 참여한 계정 펼치기']]
        col_name=세전계속사업이익률.columns.to_list()[:1][0]
        세전계속사업이익률.drop(col_name, axis=1, inplace=True)
        세전계속사업이익률=세전계속사업이익률.astype(float)

        영업이익률=재무비율.loc[['영업이익률계산에 참여한 계정 펼치기']]
        col_name=영업이익률.columns.to_list()[:1][0]
        영업이익률.drop(col_name, axis=1, inplace=True)
        영업이익률=영업이익률.astype(float)

        ROA=재무비율.loc[['ROA계산에 참여한 계정 펼치기']]
        col_name=ROA.columns.to_list()[:1][0]
        ROA.drop(col_name, axis=1, inplace=True)
        ROA=ROA.astype(float)

        ROE=재무비율.loc[['ROE계산에 참여한 계정 펼치기']]
        col_name=ROE.columns.to_list()[:1][0]
        ROE.drop(col_name, axis=1, inplace=True)
        ROE=ROE.astype(float)

        ROIC=재무비율.loc[['ROIC계산에 참여한 계정 펼치기']]
        col_name=ROIC.columns.to_list()[:1][0]
        ROIC.drop(col_name, axis=1, inplace=True)
        ROIC=ROIC.astype(float)

        df=pd.concat([매출액, 당기순이익, 유동자산, 유동부채, 총부채, 유동비율, 당좌비율, 부채비율, 이자보상배율, \
                        매출액증가율, 판매비와관리비증가율, 영업이익증가율, 매출총이익율, \
                        세전계속사업이익률, 영업이익률, 영업활동FCF, 투자활동FCF, ROA, ROE, ROIC], axis=0)

        df.drop(['전년동기','전년동기(%)'], axis=1, inplace=True)
        
        df=df.transpose()
        df=df.rename(columns={'유동자산계산에 참여한 계정 펼치기':'유동자산','유동부채계산에 참여한 계정 펼치기':'유동부채','부채':'총부채'})
        df=df.rename(columns={'유동비율계산에 참여한 계정 펼치기':'유동비율','당좌비율계산에 참여한 계정 펼치기':'당좌비율','부채비율계산에 참여한 계정 펼치기':'부채비율','이자보상배율계산에 참여한 계정 펼치기':'이자보상배율'})
        df=df.rename(columns={'매출액증가율계산에 참여한 계정 펼치기':'매출액증가율','판매비와관리비증가율계산에 참여한 계정 펼치기':'판매비와관리비증가율','영업이익증가율계산에 참여한 계정 펼치기':'영업이익증가율'})
        df=df.rename(columns={'매출총이익율계산에 참여한 계정 펼치기':'매출총이익율','세전계속사업이익률계산에 참여한 계정 펼치기':'세전계속사업이익률','영업이익률계산에 참여한 계정 펼치기':'영업이익률'})
        df=df.rename(columns={'ROA계산에 참여한 계정 펼치기':'ROA','ROE계산에 참여한 계정 펼치기':'ROE','ROIC계산에 참여한 계정 펼치기':'ROIC'})
        df=df.rename(columns={'영업활동으로인한현금흐름':'영업활동FCF','투자활동으로인한현금흐름':'투자활동FCF'})

        df['잉여현금FCF']=df['영업활동FCF']+df['투자활동FCF']
        df['잉여현금비율']=df['잉여현금FCF']/df['매출액']*100

        # 이익수익률=EPS/주가 > 채권수익률(현재 3년 국채 수익률 또는 10년 국채 수익률)
        # 안전마진(순유동자산, 적정주가) => (유동자산 - 유동부채) / 총발행주식수
        # 안전마진(순순유동자산, 적정주가) => (유동자산 - 부채총계) / 총발행주식수
        # df=df.transpose()
    except:
        return df

    return df