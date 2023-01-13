import streamlit as st
import pandas as pd
from datetime import date, timedelta
from Code import Dart
import requests

def get_date(기준일, delta):
    return (기준일 - timedelta(days=delta)).strftime("%Y-%m-%d")

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

def 재무정보_보여주기(조회일, 시작일, 종료일, 티커, 종목, 내재가치):

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
        df=tables[0]
        시가총액='시가총액(억):'+df.iloc[[4]][1].values[0]+'\n'
        내재가치='내재가치: '+str(내재가치)
        st.text(종목+'\n'+종가+최고가52+최저가52+이평120+이격률120+rsi10+bbl+시가총액+내재가치)

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
        except: st.write('펀더멘털 정보 없음 !!')

    return


def 관심주_보기(티커, 종목, 상승파동비율, 위치정보):

    col1, col2=st.columns([1,1])
    with col1:
        st.markdown(f'''###### :orange[{티커}]''')
        st.dataframe(상승파동비율)
    with col2:
        st.markdown(f'''###### :orange[{종목}]''')
        st.dataframe(위치정보)

    return