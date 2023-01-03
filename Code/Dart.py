import OpenDartReader
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

API_KEY="d538a1a0a4263cb8fbfa06a7429937ea86fc1aa1"
dart=OpenDartReader(API_KEY)
# @st.cache(suppress_st_warning=True)
def 금감원_공시내역_보기():
    # 금일 금강원 공시 내역
    today=datetime.now().strftime('%Y%m%d')
    df=dart.list(start=today, end=today, final=False)
    st.markdown('-----')
    st.text('금일 금감원 공시 건수:'+str(len(df))+'건')
    st.dataframe(df)
    return