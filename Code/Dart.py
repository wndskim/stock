import OpenDartReader
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pykrx import stock


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

def Index_Fundamental_조회(시작일, 종료일, 마켓):
    if 마켓=='코스피': market='1001'
    else: market='2001' # 코스닥
    df=stock.get_index_fundamental(시작일, 종료일, market)
    df.reset_index(inplace=True)
    df['날짜']=df['날짜'].dt.strftime('%Y-%m-%d')
    df['종가'] = df['종가'].map('{:,.2f}'.format)
    # df['종가']=df['종가'].round(2)
    # df['PBR']=df['PBR'].round(2)

    # df['종가']=df['종가'].astype(float)
    # df['종가']=df['종가'].apply(lambda x: round(x, 2))
    df['PBR']=df['PBR'].apply(lambda x: round(x, 2))
    # df['column_name'] = df['column_name'].apply(lambda x: round(x, 2))


    return df