import streamlit as st
import pandas as pd
from datetime import date, timedelta
from Code import Dart
import requests

def get_date(기준일, delta):
    return (기준일 - timedelta(days=delta)).strftime("%Y-%m-%d")

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

        종가='종가: '+str(주가정보['종가'].iloc[-1].round(0))+'\n'
        최고가52='52주최고가: '+str(주가정보['High52'].iloc[-1].round(0))+'\n'
        최저가52='52주최저가: '+str(주가정보['Low52'].iloc[-1].round(0))+'\n'
        이평120='120이평값: '+str(주가정보['sma120'].iloc[-1].round(2))+'\n'
        이격률120='120이격률: '+str(주가정보['이격률120'].iloc[-1].round(2))+'\n'
        rsi10='RSI10: '+str(주가정보['rsi10'].iloc[-1].round(2))+'\n'
        bbl='볼린저하단값: '+str(주가정보['bb_bbl'].iloc[-1].round(2))+'\n'

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

def 관심주_보기(티커, 종목, 상승파동비율, 위치정보, 최근주가):

    col1, col2, col3, col4=st.columns([1,1,1,1])

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

        발굴일값='발굴일: '+발굴일+'\n'
        현재가값='현재가: '+str(현재가)+'\n'

        기간최고가값='기간최고가: '+str(기간최고가)+'('+str(기간최고가일)+')'+'\n'
        기간최저가값='기간최저가: '+str(기간최저가)+'('+str(기간최저가일)+')'+'\n'
        
        최고가52값='52주최고가: '+str(최고가52)+'\n'
        최저가52값='52주최저가: '+str(최저가52)+'\n'

        위치1값='파동위치1: '+위치1+'\n'
        위치2값='파동위치2: '+위치2+'\n'

        st.text(현재가값+발굴일값+기간최고가값+기간최저가값+최고가52값+최저가52값+위치1값+위치2값)

        # 참조링크보기
        참조링크보기(티커)

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

        이동평균120값='120이동평균: '+str(이동평균120)+'('+str(이격률120)+')'

        st.text(가격+내재가치+이동평균120값)

        st.text('3년 이동평균 이격률: 차후보완')

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