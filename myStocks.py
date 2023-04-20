import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
import yfinance as yf
import datetime
from datetime import date, timedelta
from Code import Dart, Chart, Strategy, Display

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

def get_date(기준일, delta):
    return (기준일 - timedelta(days=delta)).strftime("%Y-%m-%d")

##############################################################
# ##### Main
##############################################################
def main():

    # hide_menu_style="""
    #         <style>
    #         #MainMenu {visibility: hidden; }
    #         footer {visibility: hidden; }
    #         </style>
    # """
    # st.markdown(hide_menu_style, unsafe_allow_html=True)


    version=st.__version__
    st.markdown(f'''
                #### My Stock Management System(Web Version)
                streamlit version is {version}
                ''')
    
    # Side Bar 생성
    job=st.sidebar.selectbox('선택',['선택','시장 상황 확인','년도별 가격 변동률 조회','관심주','특징주','체크 리스트',\
                             '조회','가격 변동률(년간)'])

    if job=='시장 상황 확인':
        Strategy.주식시장순환원리_나바로()
        return

    if job=='체크 리스트':
        Strategy.매매기술_설명()
        return

    조회일=st.sidebar.date_input('조회일')

    if job=='조회':
        시작일=str(get_date(조회일, 20)).replace('-','')  # 조회일로부터 20일전 부터 데이타 가져오기
        종료일=str(조회일).replace('-','')
        조회선택=st.sidebar.selectbox('선택',['선택','코스피200','인덱스종류','종목별 OHLCV'])
        if 조회선택=='인덱스종류':
            col1,col2=st.columns(2)
            with col1:
                for ticker in stock.get_index_ticker_list(market='KOSPI'):
                    st.write(ticker, stock.get_index_ticker_name(ticker))
            with col2:
                for ticker in stock.get_index_ticker_list(market='KOSDAQ'):
                    st.write(ticker, stock.get_index_ticker_name(ticker))
            return
        
        if 조회선택=='코스피200':
            Display.코스피200상승률하락률순으로보기()
            return

    if job=='선택':
        chk00=st.checkbox('미연방은행(FRED) 주요지표 보기',value=False)
        if chk00:
            Display.연방은행주요지표보기()
            return

        chk0=st.checkbox('증시관련 주요 뉴스 링크 보기',value=False)
        if chk0:
            st.write('[2023-03-15(수): 경기 용인에 세계 최대 규모 반도체클러스터 조성](https://m.sedaily.com/NewsView/29N1BNH3JZ#cb)')
            st.write('[2023-03-14(화): 이엔플러스, 사우디아라비아 SIIVC 실사 진행 확인...2차전지 대규모 투자 검토](https://m.sedaily.com/NewsView/29N0V55N2B#cb)')
            st.write('[2023-03-14(화): 가온셀, 사우디 1조4,000억원 규모 투자 기대](http://www.todayenergy.kr/news/articleView.html?idxno=258514)')
            st.write('[2023-03-08(화): 尹정부 첫 수주 "이집트 원전" 법률자문 우선협상자로 율촌 가닥](https://www.ajunews.com/view/20230307122709675)')
            st.write('[2023-03-08(화): 하나기술, 올해 매출 2배 성장 목표..."노르웨이서만 1조 수주 전망"](https://m.newspim.com/news/view/20230304000030)')
            st.write('[2023-03-07(월): 700조 규모 "네옴시티"도 결국은 "물"…수처리 건설사들 노났다](https://biz.newdaily.co.kr/site/data/html/2023/03/06/2023030600073.html)')
            return

        chk1=st.checkbox('금감원 공시내역을 확인', value=False)
        if chk1:
            Dart.금감원_공시내역_보기(조회일)
            return

        chk2=st.checkbox('시장지표를 확인', value=False)
        if chk2:
            시작일=str(get_date(조회일, 20)).replace('-','')  # 조회일로부터 20일전 부터 데이타 가져오기
            종료일=str(조회일).replace('-','')
            df_kospi=Dart.Index_Fundamental_조회(시작일,종료일,'코스피')
            df_kosdaq=Dart.Index_Fundamental_조회(시작일,종료일,'코스닥')

            # kospi_pbr=df_kospi._get_value(13, 'PBR')
            df_kospi['PBR']=df_kospi['PBR'].astype(float)
            df_kospi['PER']=df_kospi['PER'].astype(float)
            kospi_pbr=df_kospi['PBR'].iloc[0]
            kospi_per=df_kospi['PER'].iloc[0]

            freq='d'
            df_index=Dart.Index_OHLCV_조회(str(get_date(조회일, 250)).replace('-',''),종료일, '1001', freq=freq) # 250일전 날짜 구해서 작업 수행

            kospi_rsi=df_index['rsi'].iloc[-1].round(2)
            kospi_bbl=df_index['bb_bbl'].iloc[-1].round(2)
            kospi_지수=df_index['종가'].iloc[-1].round(2)

            if (kospi_pbr < 0.9): 시장상태='폭락장인 상태이다'
            elif (kospi_pbr > 0.89999) and (kospi_pbr < 1.0): 시장상태='정상적인 상태이다'
            elif (kospi_pbr > 0.99999) and (kospi_pbr < 1.2): 시장상태=' 고평가 상태이다'
            else: 시장상태=' 매우 고평가 상태이다'
            st.markdown(f'''###### :orange[{조회일}일 기준으로 PBR이 {kospi_pbr}이므로 {시장상태}]''')

            col1, col2, col3, col4=st.columns(4)
            with col1:
                st.markdown(f'''###### :orange[1. 코스피지수: {kospi_지수}]''')
            with col2:
                st.markdown(f'''###### :violet[2. 볼리저밴드 하단선: {kospi_bbl}]''')
            with col3:
                st.markdown(f'''###### :green[3. PBR: {kospi_pbr}]''')
                st.markdown(f'''###### :green[4. PER: {kospi_per}]''')
            with col4:
                st.markdown(f'''###### :blue[5. RSI: {kospi_rsi}]''')

            st.markdown('-----')
            st.markdown('''
                ###### :orange[2023-03-09(목) 새로운 종목이 나타남(코스피200 종목 기준)]
                ###### :blue[-한미사이언스/HDC현대산업개발/한전기술/두산에너빌리티/SK바이오사이언스/에스엘]
            ''')

            col1, col2=st.columns(2)
            with col1:
                chk3=st.checkbox('코스피 PBR 차트보기',value=False)
                if chk3: Chart.Chart_001(df_kospi)
            return
        
        chk01=st.checkbox('급등 예상주 발굴 매매 기법',value=False)
        if chk01:
            Strategy.급등예상주발굴매매법()
            return
        
        chk02=st.checkbox('강영현 투자법',value=False)
        if chk02:
            Strategy.강영현투자법()
            return
        
        chk03=st.checkbox('강영현 투자법',value=False)
        if chk03:
            Display.고객예탁금_신용잔고()
            return
    
    if job=='년도별 가격 변동률 조회':
        년도=st.sidebar.selectbox('년도선택',('2023','2022','2021','2020','2019','2018'))
        col1, col2, col3=st.columns([1,1,2])
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
                시트선택=st.sidebar.selectbox('선택',하락률)

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
        
        # 상승률 50%까지는 건수가 많어서 10%단위로 보여준다
        with col3:
            if 시트선택=='상승50%까지':
                범위=st.selectbox('선택',['0%~10%','11%~20%','21%~30%','31%~40%','41%~50%'])
                if 범위=='0%~10%': df=df.loc[(df['등락률'] >= 0) & (df['등락률'] < 11)]
                elif 범위=='11%~20%': df=df.loc[(df['등락률'] >= 11) & (df['등락률'] < 21)]
                elif 범위=='21%~30%': df=df.loc[(df['등락률'] >= 21) & (df['등락률'] < 31)]
                elif 범위=='31%~40%': df=df.loc[(df['등락률'] >= 31) & (df['등락률'] < 41)]
                else: df=df[(df['등락률'] >= 41)]

        # 종목선택 후 조회
        종목명s=(df['종목'].unique()).tolist()
        st.write(시트선택, len(종목명s),'종목')
        st.dataframe(df)

        # 재무정보 보여주기
        티커, 종목=Display.종목명_티커_선택(종목명s, df)
        시작일=str(get_date(조회일, 2000)).replace('-','')
        종료일=str(조회일).replace('-','')
        주가정보,내재가치=Display.재무정보_보여주기(조회일, 시작일, 종료일, 티커, 종목)

        # 년간 차트 그리기
        시작일=str(get_date(조회일, 2500)).replace('-','') # 10년전 일자 산출
        freq='y'
        df=Dart.Stock_OHLCV_조회(시작일, 종료일, 티커,freq)
        이평3년=df['sma3'].iloc[-1].round(0)
        Chart.Chart_002(df,종목,freq)

        # 월간 차트 그리기
        freq='m'
        df=Dart.Stock_OHLCV_조회(시작일, 종료일, 티커,freq)
        Chart.Chart_002(df,종목,freq)
        return

    if job=='관심주':
        보기기준=st.sidebar.selectbox('선택',['선택','거래량 폭증 종목 보기','차트영웅 저평가 종목','골든크로스 20/60','테마별 발굴 종목','전월 10이평 돌파 종목','전년도 상승 종목','수급주'])
        folder='./Data/'
        if 보기기준=='선택': return
        elif 보기기준=='거래량 폭증 종목 보기':
            Display.거래량폭증_종목보기(조회일)
            return
        elif 보기기준=='차트영웅 저평가 종목':
            Display.차트영웅_저평가종목(조회일)
            return
        elif 보기기준=='골든크로스 20/60':
            Display.골든크로스_2060(조회일)
            return
        elif 보기기준=='테마별 발굴 종목':
            Display.테마별_관심주보기(조회일)
            return
            
        elif 보기기준=='수급주':
            작업파일='관심주_수급주.xlsx'
        elif 보기기준=='전월 10이평 돌파 종목':
            작업파일='관심주_전월10이평돌파.xlsx'
        elif 보기기준=='전년도 상승 종목':
            작업파일='관심주_년도별.xlsx'

        df1=pd.read_excel(folder+작업파일,sheet_name=0)
        df2=pd.read_excel(folder+작업파일,sheet_name=1)
        df3=pd.read_excel(folder+작업파일,sheet_name=2)
        if len(df1)<1: st.text('자료가 없음'); return
        df1["티커"]=df1["티커"].apply(lambda x: str(x).zfill(6))
        df2["티커"]=df2["티커"].apply(lambda x: str(x).zfill(6))
        df3["티커"]=df3["티커"].apply(lambda x: str(x).zfill(6))

        if 보기기준=='수급주':
            df2.sort_values(by=['날짜','이평120이격률'], ascending=[False,True], inplace=True)

        elif 보기기준=='전년도 상승 종목':
            df1['날짜']=df1['날짜'].dt.strftime('%Y-%m-%d')
            df2['날짜']=df2['날짜'].dt.strftime('%Y-%m-%d')
            df3['날짜']=df3['날짜'].dt.strftime('%Y-%m-%d')
            보기순서=st.sidebar.radio('보기순서',['최근3년 이격률이 적은순으로 보기','최근3년 이격률이 큰순으로 보기'])
            if 보기순서=='최근3년 이격률이 적은순으로 보기': df2.sort_values(by='3년이격률최근', ascending=True, inplace=True)
            else: df2.sort_values(by='3년이격률최근', ascending=False, inplace=True)

        종목s=df2['종목'].unique().tolist()
        종목=st.sidebar.selectbox('선택',종목s)
        티커=df2[df2['종목']==종목]['티커'].values[0]

        상승파동비율=df1[df1['티커']==티커].transpose()
        위치정보=df2[df2['티커']==티커].transpose()

        # 발굴사유 보여주기
        st.text('발굴사유')
        발굴사유=df3[df3['티커']==티커]
        st.dataframe(발굴사유)

        # 최근주가 가져오기
        시작일=str(get_date(조회일, 5)).replace('-','')  # 조회일로부터 5일전 부터 데이타 가져오기
        종료일=str(조회일).replace('-','')
        Display.관심주_보기(티커, 종목, 상승파동비율, 위치정보, stock.get_market_ohlcv(시작일, 종료일, 티커),보기기준)

        # 재무정보 보여주기
        시작일=str(get_date(조회일, 2000)).replace('-','')
        종료일=str(조회일).replace('-','')
        # 티커=df[df['종목명']==종목]['티커'].values[0]
        주가정보,내재가치=Display.재무정보_보여주기(조회일, 시작일, 종료일, 티커, 종목)

        # 일간 차트 그리기
        freq='d'
        df=Dart.Stock_OHLCV_조회(시작일, 종료일, 티커,freq)
        Chart.Chart_002(df,종목,freq)
        return

    if job=='특징주':
        st.markdown(''' ##### :orange[상한가/1000만주 이상 거래 종목]''')
        df=pd.read_excel('./Data/상한가_300억이상_거래 종목.xlsx',sheet_name=0)
        df_특징주=pd.read_excel('./Data/특징주.xlsx',sheet_name=0)
        df['날짜']=df['날짜'].dt.strftime('%Y-%m-%d')
        df["티커"] = df["티커"].apply(lambda x: str(x).zfill(6))
        df_특징주["티커"] = df_특징주["티커"].apply(lambda x: str(x).zfill(6))

        col1, col2, col3=st.columns([1,1,3])
        with col1:
            선택일=st.date_input('날짜선택')
            # 전체 또는 해당일자 보기
            df_선택일=df[df['날짜']==str(선택일)]
        with col2:
            radio1=st.radio("선택", ('선택일 보기', '전체 보기'))

        # 종목선택
        종목명s=df_선택일['종목명'].unique().tolist()
        종목=st.sidebar.selectbox('선택',종목명s)
        df_종목=df[df['종목명']==종목]

        # 화면에 전송
        if radio1=='전체 보기': st.dataframe(df)
        else:
            if len(df_선택일)<1: st.write('해당일에는 특징주 정보가 없음'); return
            else: st.dataframe(df_선택일)

        # 선택된 종목 보기
        st.dataframe(df_종목[['날짜','티커','종목명','사유_뉴스']])

        # 재무정보 보여주기
        시작일=str(get_date(조회일, 2000)).replace('-','')
        종료일=str(조회일).replace('-','')
        티커=df[df['종목명']==종목]['티커'].values[0]
        주가정보,내재가치=Display.재무정보_보여주기(조회일, 시작일, 종료일, 티커, 종목)

        # 년간 차트 그리기
        시작일=str(get_date(조회일, 2500)).replace('-','') # 10년전 일자 산출
        freq='y'
        df=Dart.Stock_OHLCV_조회(시작일, 종료일, 티커,freq)
        Chart.Chart_002(df,종목,freq)

        # 월간 차트 그리기
        freq='m'
        df=Dart.Stock_OHLCV_조회(시작일, 종료일, 티커,freq)
        Chart.Chart_002(df,종목,freq)  
        return      

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



    chk4=st.sidebar.checkbox('2023년 투자전략 보기', value=False)
    if chk4:
        선택=st.sidebar.selectbox('선택',['선택','2023년2월 이후','2023년1월'])
        if 선택=='선택': return
        if 선택=='2023년2월 이후': Strategy.Strategy_2023()
        else: Strategy.Strategy_2023_01(kospi_pbr)
        return

    return





#####################################################
##### Main ##########################################
#####################################################
if __name__ == '__main__':
    main()

