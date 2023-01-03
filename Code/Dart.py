import OpenDartReader
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

API_KEY="d538a1a0a4263cb8fbfa06a7429937ea86fc1aa1"
dart=OpenDartReader(API_KEY)
# @st.cache(suppress_st_warning=True)
def 금감원_공시내역_보기(조회일):
    # 금일 금강원 공시 내역
    # today=datetime.now().strftime('%Y%m%d')
    조회일=datetime.now().strftime('%Y%m%d')
    df=dart.list(start=조회일, end=조회일, final=False)

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