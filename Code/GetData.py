import streamlit as st
from pykrx import stock
import ta

@st.cache_resource
def load_from_pykrx_해당일전체(조회일):
    return stock.get_market_ohlcv(조회일)

@st.cache_resource
def 종목별_거래대금(시작일, 종료일, 티커):
    return stock.get_market_trading_value_by_date(시작일, 종료일, 티커) # 순매수 금액