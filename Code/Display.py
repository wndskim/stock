import streamlit as st
import pandas as pd
from datetime import date, timedelta
from Code import Dart, Chart
import requests
from pykrx import stock

def get_date(기준일, delta):
    return (기준일 - timedelta(days=delta)).strftime("%Y-%m-%d")

def 골든크로스_2060():

    df=pd.read_excel('./Data/이동평균120기준 위치.xlsx')
    col1,col2=st.columns([1,4])
    with col1:
        radio=st.radio('선택',['골든크로스(20/60)','데드크로스(20/60)'])
        container=st.container()
    with col2:
        if radio=='골든크로스(20/60)':
            df=df[df['position2060']==1]
        else:
            df=df[df['position2060']==-1]
        
        tickers=df['티커'].unique()
        container.write(len(tickers))
        df.sort_values(by='위치',ascending=True,inplace=False)
        st.dataframe(df)
    return

def 테마별_관심주보기(조회일):

    작업파일='관심주_테마별.xlsx'
    folder='./Data/'
    df=pd.read_excel(folder+작업파일)

    df1=pd.read_excel(folder+작업파일,sheet_name=0)
    df2=pd.read_excel(folder+작업파일,sheet_name=1)
    df3=pd.read_excel(folder+작업파일,sheet_name=2)
    if len(df1)<1: st.text('자료가 없음'); return
    df1["티커"]=df1["티커"].apply(lambda x: str(x).zfill(6))
    df2["티커"]=df2["티커"].apply(lambda x: str(x).zfill(6))
    df3["티커"]=df3["티커"].apply(lambda x: str(x).zfill(6))
    df1['해당년월']=df1['해당년월'].astype(str)

    col1, col2, col3, col4=st.columns([1,1,2,2])
    with col1:
        선정년월=['202303','202302']
        년월=st.selectbox('선택',선정년월)

        df1=df1[df1['해당년월']==년월]
        df2=df2[df2['해당년월']==년월]
        df3=df3[df3['해당년월']==년월]


        # df2=df2[df2['티커'].isin(df1['티커'])]
        # df3=df3[df3['티커'].isin(df1['티커'])]

        st.write(len(df1),len(df2),len(df3))


        # df1['날짜']=df1['날짜'].astype(str)
        # df2['날짜']=df2['날짜'].astype(str)
        # df3['날짜']=df3['날짜'].astype(str)
        # df1=df1[df1['날짜'].str.startswith(년월)]
        # df2=df2[df2['날짜'].str.startswith(년월)]
        # df3=df3[df3['날짜'].str.startswith(년월)]
    with col2:
        radio1=st.radio('선택',('테마별 보기','전체보기'))
    with col3:
        if radio1=='테마별 보기':
            if len(df3)>0:
                테마s=df3['설명'].unique().tolist()
                테마선택=st.selectbox('선택',테마s)
                df3=df3[df3['설명']==테마선택]
            else: st.text('해당년월 자료 없음..!!'); return
    with col4:
        radio2=st.radio('선택',('120이평 작은순 보기', '120이평 큰순 보기'))
        if radio2=='120이평 작은순 보기':
            df2.sort_values(by='이평120이격률',ascending=True,inplace=True)
        else: df2.sort_values(by='이평120이격률',ascending=False,inplace=True)
  
        st.write('총', str(len(df3)),'건')

    티커s=df3['티커'].tolist()
    df2=df2[df2["티커"].isin(티커s)]
    df1=df1[df1["티커"].isin(티커s)]

    st.dataframe(df2)

    ######
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
    관심주_보기(티커, 종목, 상승파동비율, 위치정보, stock.get_market_ohlcv(시작일, 종료일, 티커),'수급주')

    # 재무정보 보여주기
    시작일=str(get_date(조회일, 2000)).replace('-','')
    종료일=str(조회일).replace('-','')
    주가정보,내재가치=재무정보_보여주기(조회일, 시작일, 종료일, 티커, 종목)

    # 일간 차트 그리기
    freq='d'
    df=Dart.Stock_OHLCV_조회(시작일, 종료일, 티커,freq)
    Chart.Chart_002(df,종목,freq)

    return


def 현재위치_이격률기준(이격률120):

    위치분류 = {
        이격률120 < 75: "겨울3",
        75 <= 이격률120 < 90: "겨울2",
        90 <= 이격률120 < 100: "겨울1",
        100 <= 이격률120 < 105: "봄1",
        105 <= 이격률120 < 110: "봄2",
        110 <= 이격률120 < 115: "봄3",
        115 <= 이격률120 < 120: "여름1",
        120 <= 이격률120 < 125: "여름2",
        125 <= 이격률120 < 130: "여름3",
        130 <= 이격률120 < 135: "가을1",
        135 <= 이격률120 < 140: "가을2",
        이격률120 >= 140: "가을3"
    }
    return 위치분류.get(True, "120이격률 기준 위치산정 불가")

def 코스피200상승률하락률순으로보기():

    df=pd.read_excel("./Data/코스피200위치.xlsx")
    df["티커"]=df["티커"].apply(lambda x: str(x).zfill(6))

    radio=st.radio('선택',('상승/하락순 보기','최고가대비 하락/상승순 보기'))
    if radio=='상승/하락순 보기':
        col1,col2=st.columns([1,1])
        with col1:
            st.text('-- 상승률순 --')
            df.sort_values(by='등락률', ascending=False, inplace=True)
            df.reset_index(inplace=True)
            df.drop('index', axis=1, inplace=True)
            st.dataframe(df)
        with col2:
            st.text('-- 하락순 --')
            df.sort_values(by='등락률', ascending=True, inplace=True)
            df.reset_index(inplace=True)
            df.drop('index', axis=1, inplace=True)
            st.dataframe(df)
    else:
        col1,col2=st.columns([1,1])
        with col1:
            st.text('-- 하락률큰순(52최고가/최저가대비) --')
            df.sort_values(by='최고가대비등락률', ascending=True, inplace=True)
            df.reset_index(inplace=True)
            df.drop('index', axis=1, inplace=True)
            st.dataframe(df)
        with col2:
            st.text('-- 하락률적은순(52최고가/최저가대비) --')
            df.sort_values(by='최고가대비등락률', ascending=False, inplace=True)
            df.reset_index(inplace=True)
            df.drop('index', axis=1, inplace=True)
            st.dataframe(df)

    return

def 업종_테마가져오기(티커):
    df=pd.read_excel('./Data/2022_종목별_년간등락.xlsx',sheet_name='전체')
    업종테마=df[df['티커']==티커]
    return 업종테마

def 특징주내역가져오기(티커):
    df=pd.read_excel('./Data/상한가_300억이상_거래 종목.xlsx',sheet_name=0)
    특징주내역=df[df['티커']==티커]
    return 특징주내역

def 내재가치계산(df1,df2,펀더멘털):

    발행주식수=df1.iloc[[6]][1].values[0].replace(',','')
    pos=발행주식수.find('/')
    발행주식수=int(발행주식수[:pos])
    유통주식수=df1.iloc[[6]][3].values[0].replace(',','')
    pos=유통주식수.find('/')
    유통주식수=int(유통주식수[:pos])

    try:
        자사주수=int(df2[df2['항목']=='자사주']['보통주'].values[0])
    except: 자사주수=0

    eps1=int(펀더멘털['EPS'].iloc[0].replace(',',''))*3
    eps2=int(펀더멘털['EPS'].iloc[1].replace(',',''))*2
    eps3=int(펀더멘털['EPS'].iloc[2].replace(',',''))*1
    bps=int(펀더멘털['BPS'].iloc[0].replace(',',''))*1

    유통주식가능비율=(발행주식수-자사주수)/발행주식수

    eps=(eps1+eps2+eps3)/6
    내재가치=(bps+eps*10)/2/유통주식가능비율

    return 내재가치

def 참조링크보기(티커):
    st.write('[NICE CompanySearch](https://comp.kisline.com/hi/HI0100M010GE.nice?stockcd={}&nav=1)'.format(티커))
    st.write('[CompanyGuide](https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701)'.format(티커))
    st.write('[네이버금융(종합정보)](https://finance.naver.com/item/main.naver?code={})'.format(티커))
    st.write('[ZOOM검색](https://search.zum.com/search.zum?method=uni&query={}&qm=f_instant.top)'.format(티커))
    st.write('[다음통합검색](https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q={})'.format(티커))
    return

def 종목명_티커_선택(종목명s, df):

    종목=st.sidebar.selectbox('종목선택',종목명s)
    티커=df[df['종목']==종목]['티커'].values[0]
    col1, col2=st.columns([1,3])
    with col1:
        st.text('')
        st.text('')
        st.markdown('''
            ###### :orange[꼭 확인해야 할 사항 4가지]
            ''')
    with col2:
        st.text('')
        st.text('')
        st.markdown('''
            ###### :orange[1:부채비율, 2:유보율, 3:유통주식수, 4:적자흑자유무]
            ''')
    return 티커, 종목            

def 재무정보_보여주기(조회일, 시작일, 종료일, 티커, 종목):

    col1, col2, col3=st.columns([1,2,2])
    with col1:
        st.text('')
        # 개별종목 주가 가져오기

        주가정보=Dart.Stock_OHLCV_조회(시작일, 종료일, 티커,'d')

        이격률120=int(주가정보['이격률120'].iloc[-1])
        위치=현재위치_이격률기준(이격률120)

        종가='종가: '+str(int(주가정보['종가'].iloc[-1]))+'\n'
        최고가52='52주최고가: '+str(int(주가정보['High52'].iloc[-1]))+'\n'
        최저가52='52주최저가: '+str(int(주가정보['Low52'].iloc[-1]))+'\n'
        이평120='120이평값: '+str(int(주가정보['sma120'].iloc[-1]))+'\n'
        이격률120='120이격률: '+str(이격률120)+'('+위치+')'+'\n'
        rsi10='RSI10: '+str(주가정보['rsi10'].iloc[-1].round(2))+'\n'
        bbl='볼린저하단값: '+str(int(주가정보['bb_bbl'].iloc[-1]))+'\n'

        url=f'https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{티커}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701'
        page=requests.get(url)
        tables=pd.read_html(page.text)
        df1=tables[0]
        df2=tables[3]
        시가총액='시가총액(억):'+df1.iloc[[4]][1].values[0]+'\n'

        st.text(종목+'\n'+종가+최고가52+최저가52+이평120+이격률120+rsi10+bbl+시가총액)

        # 참조링크보기
        참조링크보기(티커)

    with col2:
        재무정보=Dart.get_CompanyGuide자료(티커).transpose()
        col_names=재무정보.columns
        if len(재무정보)>0:
            st.text('재무정보')
            for col_name in col_names:
                재무정보.loc[:, col_name]=재무정보[col_name].map('{:.2f}'.format)
            st.dataframe(재무정보)
    with col3:
        try:
            시작일=str(get_date(조회일, 2000)).replace('-','')
            종료일=str(조회일).replace('-','')
            펀더멘털=Dart.Stock_Fundamental_조회(시작일, 종료일, 티커)
            st.text('펀더멘털 정보')
            st.dataframe(펀더멘털)

            내재가치=int(내재가치계산(df1,df2,펀더멘털))
            내재가치값='내재가치: '+str(내재가치)
            st.text(내재가치값)
        except:
            st.write('펀더멘털 정보 없음 !!')
            st.write('내재가치 계산 못함 !!')
            내재가치=-9999999999

    return 주가정보.iloc[-1],내재가치

def 관심주_보기(티커, 종목, 상승파동비율, 위치정보, 최근주가,보기기준):

    ################################
    col1, col2=st.columns([1,1])
    with col1:
        st.text('테마들')
        st.dataframe(업종_테마가져오기(티커)[['테마','업종']])
    with col2:
        st.text('상한가 또는 1000만주 이상 거래 사유')
        st.dataframe(특징주내역가져오기(티커)[['마켓','종류','등락률','사유_뉴스']])

    col1, col2, col3, col4=st.columns([2,2,2,1])
    with col1:
        st.markdown(f'''###### :orange[{종목}]''')
        st.text('(이동평균120 기준)')

        현재가=최근주가['종가'].iloc[-1]

        발굴일=위치정보.loc['날짜'].values[0]
        기간최고가=위치정보.loc['기간최고가'].values[0]
        기간최고가일=위치정보.loc['기간최고가일'].values[0]
        기간최저가=위치정보.loc['기간최저가'].values[0]
        기간최저가일=위치정보.loc['기간최저가일'].values[0]

        최고가52=위치정보.loc['최고가52주'].values[0]
        최저가52=위치정보.loc['최저가52주'].values[0]

        위치1=위치정보.loc['파동위치1'].values[0]
        위치2=위치정보.loc['파동위치2'].values[0]

        발굴일값='발굴일: '+ str(발굴일)+'\n'
        현재가값='현재가: '+str(현재가)+'(실시간)'+'\n'

        기간최고가값='기간최고가: '+str(기간최고가)+'('+str(기간최고가일)+')'+'\n'
        기간최저가값='기간최저가: '+str(기간최저가)+'('+str(기간최저가일)+')'+'\n'
        
        최고가52값='52주최고가: '+str(최고가52)+'\n'
        최저가52값='52주최저가: '+str(최저가52)+'\n'

        위치1값='파동위치1: '+위치1+'\n'
        위치2값='파동위치2: '+위치2+'\n'

        st.text(현재가값+발굴일값+기간최고가값+기간최저가값+최고가52값+최저가52값+위치1값+위치2값)

        st.write('[경기상황정리](https://docs.google.com/spreadsheets/d/14OhuYvmkb3dZUIpxP9mu9uS1zNxUY3gFnafHOWOYs5o/edit#gid=719655173)')
        st.write('[기법정리](https://docs.google.com/spreadsheets/d/1tJg4kfIIpt17LNKXoKwzzallnXPmyCzMF1DhIIw1Q-8/edit#gid=1186881965)')
        st.write('[KT(030200) 보유주](https://docs.google.com/spreadsheets/d/1A_8rYBwU35sfWJezUcKGaFiofMc0cp39TZQCkdSA6Rw/edit#gid=0)')
        st.write('[유라테크(048430) 관심주](https://docs.google.com/spreadsheets/d/1IwcqZpn8_yiw-ZwX8kJW3na9d5Xy_aLY9Bv4X1WruLY/edit#gid=743352833)')

    with col2:
        st.markdown(f'''###### :orange[{티커}]''')
        종가=상승파동비율.loc['종가'].values[0]
        숙향가치=상승파동비율.loc['내재가치'].values[0]
        가격='종가: '+str(종가)+'\n'
        내재가치='내재가치: '+str(숙향가치)+'\n'+'\n'

        이동평균120=위치정보.loc['이평120'].values[0]
        이격률120=위치정보.loc['이평120이격률'].values[0]
        if (보기기준=='전월 10이평 돌파 종목') or (보기기준=='수급주'):
            주봉60시가=위치정보.loc['주봉60시가'].values[0]
            주봉60종가=위치정보.loc['주봉60종가'].values[0]
            차이3년='n/a'
        else:
            이동평균3년=위치정보.loc['3년이평'].values[0]
            이격률3년=위치정보.loc['3년이평이격률'].values[0]
            차이3년=현재가-이동평균3년
        이동평균3년최근=위치정보.loc['3년이평최근'].values[0]
        이격률3년최근=위치정보.loc['3년이격률최근'].values[0]
        차이120=현재가-이동평균120
        차이3년최근=현재가-이동평균3년최근

        이동평균120값='120이동평균: '+str(이동평균120)+'('+str(이격률120)+')'+'\n'
        if (보기기준=='전월 10이평 돌파 종목') or (보기기준=='수급주'):
            주봉60시가종가값='주봉60시가/종가: '+str(주봉60시가)+'/'+str(주봉60종가)+'\n'
        else:
            이동평균3년값='3년이동평균: '+str(이동평균3년)+'('+str(이격률3년)+')'+'\n'
        이동평균3년최근값='3년이동평균(최근): '+str(이동평균3년최근)+'('+str(이격률3년최근)+')'+'\n'+'\n'
        차이120값='120이동평균과 현재가의 차이: '+str(차이120)+'\n'
        차이3년값='3년이동평균과 현재가의 차이: '+str(차이3년)+'\n'
        차이3년최근값='3년이동평균최근과 현재가의 차이: '+str(차이3년최근)

        if (보기기준=='전월 10이평 돌파 종목') or (보기기준=='수급주'):
            st.text(가격+내재가치+이동평균120값+주봉60시가종가값+이동평균3년최근값+차이120값+차이3년값+차이3년최근값)
        else:
            st.text(가격+내재가치+이동평균120값+이동평균3년값+이동평균3년최근값+차이120값+차이3년값+차이3년최근값)

    with col3:
        st.markdown('''###### :orange[상승파동비율(피보나치비율)위치]''')
        파동001=상승파동비율.loc['PCT001'].values[0]
        파동007=상승파동비율.loc['PCT007'].values[0]
        파동014=상승파동비율.loc['PCT014'].values[0]
        파동021=상승파동비율.loc['PCT021'].values[0]
        파동025=상승파동비율.loc['PCT025'].values[0]
        파동382=상승파동비율.loc['PCT382'].values[0]
        파동050=상승파동비율.loc['PCT050'].values[0]
        파동618=상승파동비율.loc['PCT618'].values[0]
        파동832=상승파동비율.loc['PCT832'].values[0]
        파동100=상승파동비율.loc['PCT100'].values[0]
        파동1382=상승파동비율.loc['PCT1382'].values[0]
        파동1618=상승파동비율.loc['PCT1618'].values[0]
        파동200=상승파동비율.loc['PCT200'].values[0]

        파동001값='1%값(봄1): '+str(파동001)+'\n'
        파동007값='7%값(봄1): '+str(파동007)+'\n'+'\n'
        파동014값='14%값(봄2): '+str(파동014)+'\n'
        파동021값='21%값(봄2): '+str(파동021)+'\n'+'\n'
        파동025값='25%값(여름1): '+str(파동025)+'\n'
        파동382값='38.20%값(여름1): '+str(파동382)+'\n'+'\n'
        파동050값='50%값(여름2): '+str(파동050)+'\n'
        파동618값='61.80%값(여름2): '+str(파동618)+'\n'+'\n'
        파동832값='83.20%값(여름3): '+str(파동832)+'\n'
        파동100값='100%값(여름3): '+str(파동100)+'\n'+'\n'
        파동1382값='1.382%값(매도): '+str(파동1382)+'\n'
        파동1618값='1.618%값(매도): '+str(파동1618)+'\n'
        파동200값='200%값(매도): '+str(파동200)+'\n'
        
        st.text(파동001값+파동007값+파동014값+파동021값+파동025값+파동382값+파동050값+파동618값+파동832값+파동100값+파동1382값+파동1618값+파동200값)


    return