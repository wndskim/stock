import streamlit as st
from pykrx import stock
import ta

@st.cache_resource
def load_from_pykrx_해당일전체(조회일):
    return stock.get_market_ohlcv(조회일)

@st.cache_resource
def 종목별_거래대금(시작일, 종료일, 티커):
    return stock.get_market_trading_value_by_date(시작일, 종료일, 티커) # 순매수 금액

def set_indicator(data):

    data['등락']=data.종가.diff(periods=1)
    data['등락률']=data.종가.pct_change(periods=1)*100
    data['Low52']=data.저가.rolling(min_periods=1, window=262, center=False).min()
    data['High52']=data.고가.rolling(min_periods=1, window=262, center=False).max()
    data['Mid52']=(data['High52']+data['Low52'])/2
    data['sma5']=ta.trend.sma_indicator(data.종가, window=5)
    data['sma10']=ta.trend.sma_indicator(data.종가, window=10)
    data['sma20']=ta.trend.sma_indicator(data.종가, window=20)
    data['sma60']=ta.trend.sma_indicator(data.종가, window=60)
    data['sma120']=ta.trend.sma_indicator(data.종가, window=120)
    data['sma150']=ta.trend.sma_indicator(data.종가, window=150)
    data['sma240']=ta.trend.sma_indicator(data.종가, window=240)
    data['거래량20평균']=ta.trend.sma_indicator(data.거래량, window=20)
    data['거래대금20평균']=ta.trend.sma_indicator(data.거래대금, window=20)

    data['거래량20대비']=data['거래량']/data['거래량20평균']
    data['거래대금20대비']=data['거래대금']/data['거래대금20평균']
    data['diff5120']=data['sma5']/data['sma120']*100
    data['diff10120']=data['sma10']/data['sma120']*100
    data['diff20120']=data['sma20']/data['sma120']*100
    data['diff60120']=data['sma60']/data['sma120']*100
    
    # upperband, middleband, lowerband = talib.BBANDS(data.종가, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    # data['bb_upper']=upperband
    # data['bb_middle']=middleband
    # data['bb_lower']=lowerband
    # # Momentum Indocatio Functions
    # macd, macdsignal, macdhist = talib.MACD(data.종가, fastperiod=12, slowperiod=26, signalperiod=9)
    # data['macd']=macd
    # data['macdsignal']=macdsignal
    # data['macdhist']=macdhist
    # data['rsi']=talib.RSI(data.종가, timeperiod=10)
    # data['rsi14']=talib.RSI(data.종가, timeperiod=14)
    # slowk, slowd = talib.STOCH(data.고가, data.저가, data.종가, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    # data['slowk']=slowk
    # data['slowd']=slowd
    # Volatility Indicator Functions
    data['atr']=talib.ATR(data.고가, data.저가, data.종가, timeperiod=14)
    # # Volume indicator Functions
    # data['adosc']=talib.ADOSC(data.고가, data.저가, data.종가, data.Volume, fastperiod=3, s저가period=10)

    return data