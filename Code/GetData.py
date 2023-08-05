import streamlit as st
from pykrx import stock
import ta
import requests
from lxml import html
import pandas as pd
from bs4 import BeautifulSoup


def 업종소속종목가져오기(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data_rows=soup.find('table',attrs={'class':'type_5'})

    종목s,심볼s,대중소=[],[],[]
    for rows in data_rows.find_all('tr'):
        columns=rows.find_all('a',href=True, text=True)
        종목명s=[column.text for column in columns if len(column) > 0]
        티커s=[column['href'][-6:] for column in columns]

        for 종목명 in 종목명s: 종목s.append(종목명)
        for 티커 in 티커s:
            심볼s.append(티커)

            # if 티커 in 코스피대형주: 대중소.append('대형주')
            # elif 티커 in 코스피중형주: 대중소.append('중형주')
            # elif 티커 in 코스피소형주: 대중소.append('소형주')
            # elif 티커 in 코스닥대형주: 대중소.append('대형주')
            # elif 티커 in 코스닥중형주: 대중소.append('중형주')
            # elif 티커 in 코스닥소형주: 대중소.append('소형주')
            # else: 대중소.append('무소속')

    return pd.DataFrame({'티커':심볼s,'종목':종목s})

def 종목소속업종가져오기(종목):
    df=pd.read_excel('./Data/업종별_종목별_등락순위.xlsx')
    return df[df.종목==종목][['업종','대중소','업종순위']]

# @st.cache_resource
def 종목별_펀더멘털_기간(시작일,종료일,티커):
    return stock.get_market_fundamental(시작일, 종료일, 티커)

def 종목별_시가총액_기간(시작일,종료일,티커):
    return stock.get_market_cap(시작일, 종료일, 티커)

# @st.cache_resource
def load_from_pykrx_해당일전체(조회일):
    return stock.get_market_ohlcv(조회일)

# @st.cache_resource
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
    # data['atr']=talib.ATR(data.고가, data.저가, data.종가, timeperiod=14)
    # # Volume indicator Functions
    # data['adosc']=talib.ADOSC(data.고가, data.저가, data.종가, data.Volume, fastperiod=3, s저가period=10)

    return data

def 종목별_현재_재무정보(티커):
    # 자본총계
    url=f'https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{티커}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701'
    page=requests.get(url)
    tables=pd.read_html(page.text)
    재무상태표=tables[2]
    재무상태표=재무상태표.set_index(재무상태표.columns[0])
    자본총계=재무상태표.loc[['자본']]['2022/12'].values[0]
    # 자본총계=자본총계.astype(int)

    # 시가총액
    url=f'https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{티커}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701'
    page=requests.get(url)
    tables=pd.read_html(page.text)
    시세현황=tables[0]
    시가총액=시세현황.iloc[[4]][1].values[0]

    return int(자본총계),int(시가총액)

def 적정주가계산용자료가져오기(티커):
    url = f'https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{티커}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701'
    response = requests.get(url)
    tree = html.fromstring(response.content)

    try:
        종목_per=float(tree.xpath('//*[@id="corp_group2"]/dl[1]/dd')[0].text)
    except:
        종목_per=tree.xpath('//*[@id="corp_group2"]/dl[1]/dd')[0].text
    try:
        업종_per=float(tree.xpath('//*[@id="corp_group2"]/dl[3]/dd')[0].text)
    except:
        업종_per=tree.xpath('//*[@id="corp_group2"]/dl[3]/dd')[0].text

    ### Snapshot
    url = f'https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{티커}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701'
    tables = pd.read_html(url)
    try: 시가총액=int(tables[0].loc[4][1])*100000000
    except: return 0,0,0,0,0,0

    발행주식수=tables[0].loc[6][1]
    pos=발행주식수.find('/')
    발행주식수=int(발행주식수[:pos].replace(',',''))
    try:
        영업이익=int(tables[10].loc[1]['Annual'][3])
    except:
        영업이익=tables[10].loc[1]['Annual'][3]

    try:
        EPS=int(tables[10].loc[18]['Annual'][3])
    except:
        EPS=tables[10].loc[18]['Annual'][3]

    return 종목_per,업종_per,시가총액,발행주식수,영업이익,EPS