import streamlit as st
import pandas as pd
from datetime import date, timedelta
from Code import Dart, Chart, Strategy, GetData
import requests, os, datetime
from pykrx import stock

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

def get_date(기준일, delta):
    return (기준일 - timedelta(days=delta)).strftime("%Y-%m-%d")

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

def scrap_고객예탁금_신용잔고(page):
    url = f'https://finance.naver.com/sise/sise_deposit.naver?&page={page}'
    print(url)
    return pd.read_html(url,encoding='utf-8')

def 고객예탁금_신용잔고():
    st.text('고객예탁금 대비 신용잔고 비율이 35%이상이면 과열신호로 관심을 가지고 본다(35%는 확인 필요)')
    df_concat=pd.DataFrame()
    for i in range(1,6):
        dfs=scrap_고객예탁금_신용잔고(i)[0]
        날짜=dfs.iloc[:,0].dropna().tolist()
        고객예탁금1=dfs.iloc[:,1].dropna().tolist()
        고객예탁금2=dfs.iloc[:,2].dropna().tolist()
        신용잔고1=dfs.iloc[:,3].dropna().tolist()
        신용잔고2=dfs.iloc[:,4].dropna().tolist()
        df = pd.DataFrame({'날짜': 날짜, '고객예탁금1': 고객예탁금1, '고객예탁금2': 고객예탁금2, '신용잔고1': 신용잔고1, '신용잔고2': 신용잔고2})
        df['고객예탁금']=df['고객예탁금1']+df.고객예탁금2
        df['신용잔고']=df['신용잔고1']+df.신용잔고2
        df['신용잔고비율']=df.신용잔고/df.고객예탁금
        df['날짜']='20'+df['날짜']
        df['날짜']=pd.to_datetime(df.날짜)
        df['날짜']=df.날짜.dt.strftime('%Y/%m/%d')
        df_concat=pd.concat([df_concat,df],axis=0)

    columns=['날짜','고객예탁금','신용잔고','신용잔고비율']
    df_concat=df_concat.reindex(columns = columns)
    df_concat.sort_values(by='날짜',ascending=True,inplace=True)

    df_concat['예탁금증감']=df_concat['고객예탁금'].diff()
    df_concat['신용잔고증감']=df_concat['신용잔고'].diff()
    df_concat.sort_values(by='날짜',ascending=False,inplace=True)

    df_concat.set_index('날짜',inplace=True)
    예탁금최고='{:,}'.format(int(df_concat['고객예탁금'].max()))
    예탁금최저='{:,}'.format(int(df_concat['고객예탁금'].min()))
    신용잔고최고='{:,}'.format(int(df_concat['신용잔고'].max()))
    신용잔고최저='{:,}'.format(int(df_concat['신용잔고'].min()))
    신용잔고비율최고='{:.2f}'.format(df_concat['신용잔고비율'].max())
    신용잔고비율최저='{:.2f}'.format(df_concat['신용잔고비율'].min())

    예탁금최고일=df_concat['고객예탁금'].idxmax()
    예탁금최저일=df_concat['고객예탁금'].idxmin()
    신용잔고최고일=df_concat['신용잔고'].idxmax()
    신용잔고최저일=df_concat['신용잔고'].idxmin()
    신용잔고비율최고일=df_concat['신용잔고비율'].idxmax()
    신용잔고비율최저일=df_concat['신용잔고비율'].idxmin()

    고객예탁금최고='고객예탁금최고: '+str(예탁금최고)+' ('+str(예탁금최고일)+')\n'
    고객예탁금최저='고객예탁금최저: '+str(예탁금최저)+' ('+str(예탁금최저일)+')\n'
    신용잔고최고='신용잔고최고: '+str(신용잔고최고)+' ('+str(신용잔고최고일)+')\n'
    신용잔고최저='신용잔고최저: '+str(신용잔고최저)+' ('+str(신용잔고최저일)+')\n'
    신용잔고비율최고='신용잔고비율최고: '+str(신용잔고비율최고)+' ('+str(신용잔고비율최고일)+')\n'
    신용잔고비율최저='신용잔고비율최저: '+str(신용잔고비율최저)+' ('+str(신용잔고비율최저일)+')\n'

    col1,col2=st.columns([1,3])
    with col1:
        st.write('[참고 웹사이트](https://m.blog.naver.com/jongy0644/222845544363)')
        st.text(고객예탁금최고+고객예탁금최저+신용잔고최고+신용잔고최저+신용잔고비율최고+신용잔고비율최저)
    with col2:
        df_sort=df_concat.sort_values(by='날짜')
        Chart.Chart_003(df_sort)

    st.dataframe(df_concat)
    return

def 연방은행주요지표보기():

    st.text('미연방은행 주요지표 보기..!!')
    st.write('[10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity](https://fred.stlouisfed.org/series/{})'.format('T10Y2Y'))
    st.write('[Continued Claims (Insured Unemployment)(실업수당 청구 건수)](https://fred.stlouisfed.org/series/{})'.format('CCSA'))
    st.write('[ Consumer Price Index for All Urban Consumers: All Items in U.S. City Average](https://fred.stlouisfed.org/series/{})'.format('CPIAUCSL'))

    # fred = Fred(api_key=fred_api)

    return

def 참조링크보기(티커,종목):

    st.write('[NICE CompanySearch](https://comp.kisline.com/hi/HI0100M010GE.nice?stockcd={}&nav=1)'.format(티커))
    st.write('[CompanyGuide](https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701)'.format(티커))
    st.write('[네이버금융(선도주확인용)](https://finance.naver.com/item/coinfo.naver?code={})'.format(티커))
    st.write('[네이버(통합검색)](https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=0&acr=1&acq=%EB%94%94%EC%BC%80%EC%9D%B4%EC%95%A4&qdt=0&ie=utf8&query={})'.format(종목))
    st.write('[ZOOM검색](https://search.zum.com/search.zum?method=uni&query={}&qm=f_instant.top)'.format(종목))
    st.write('[다음통합검색](https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&sug=&sugo=&sq=&o=&q={})'.format(종목))
    return

def 공용화면보기1(조회일,종목선택,티커,종목,df_종목,최고가,최저가,계산값1,계산값2,피보값):

    col1,col2,col3,col4=st.columns([2,2,3,3])
    with col1:
        참조링크보기(티커,종목)
    with col2:
        종가='{:,}'.format(df_종목['종가'].tail(1).values[0])
        등락='{:,}'.format(df_종목['등락'].tail(1).values[0])
        등락률=format(float(df_종목['등락률'].tail(1).values[0]),f'.2f')
        이동평균120='{:,}'.format(df_종목['sma120'].tail(1).values[0])
        이격률120=format(float(df_종목['이격률120'].tail(1).values[0]),f'.0f')

        최고가=df_종목['기간최고가'].values[0]
        최저가=df_종목['기간최저가'].values[0]
        기간최고가일=df_종목['기간최고가일'].values[0]
        기간최저가일=df_종목['기간최저가일'].values[0]

        str종가='종가: '+종가+'\n'
        str등락='등락: '+등락+'\n'
        str등락률='등락률: '+등락률+'\n'
        str이동평균120='이동평균120: '+이동평균120+'\n'
        str이격률120='이격률120: '+이격률120+'\n'
        str기간최고가='기간최고가: '+str(최고가)+'('+str(기간최고가일)+')'+'\n'
        str기간최저가='기간최저가: '+str(최저가)+'('+str(기간최저가일)+')'+'\n'

        st.text('기본정보'+'\n--------------------')
        자본총계,시가총액=GetData.종목별_현재_재무정보(티커)
        시총자본비율=format(시가총액/자본총계,'.2f')
        자본총계대비시총비율='자본총계대비 시총비율: '+시총자본비율
        st.text(자본총계대비시총비율)
        st.text(str종가+str등락+str등락률+str이동평균120+str이격률120+str기간최고가+str기간최저가)
    with col3:
        값=''
        for i,value in enumerate(피보값):
            if value==100: 값+='피보값('+str(value)+'):'+'{:,}'.format(int(계산값1[i]))+'(**2배상승**)'+'\n'
            elif value==200: 값+='피보값('+str(value)+'):'+'{:,}'.format(int(계산값1[i]))+'(***3배상승***)'+'\n'
            else: 값+='피보값('+str(value)+'):'+'{:,}'.format(int(계산값1[i]))+'\n'
        
        st.text('피보나치비율값(최저가기준)'+'\n--------------------')
        st.text(값)
    with col4:
        값=''
        for i,value in enumerate(피보값):
            if value==100: 값+='피보값('+str(value)+'):'+'{:,}'.format(int(계산값2[i]))+'(**기간최고가)'+'\n'
            elif value==200: 값+='피보값('+str(value)+'):'+'{:,}'.format(int(계산값2[i]))+'(***매우과매수)'+'\n'
            else: 값+='피보값('+str(value)+'):'+'{:,}'.format(int(계산값2[i]))+'\n'

        st.text('피보나치비율값(최고가/최저가 차액기준(영웅문))'+'\n--------------------')
        st.text(값)

    # 재무정보 보여주기
    시작일=str(get_date(조회일, 260*2)).replace('-','')
    종료일=str(조회일).replace('-','')
    주가정보,내재가치=재무정보_보여주기(조회일, 시작일, 종료일, 티커, 종목선택)

    return

def 적정주가와괴리율보기():
    folder='./Data/'
    file='이동평균120기준 위치.xlsx'
    df=pd.read_excel(folder+file)
    df["티커"]=df["티커"].apply(lambda x: str(x).zfill(6))

    df=df.query('적정주가괴리율1>0').sort_values(by='적정주가괴리율1', ascending=True)[['티커','종목','테마','업종','마켓','종가','적정주가1','적정주가2','적정주가괴리율1','적정주가괴리율2']]

    st.dataframe(df)

    return


def 배당농부법종목1(날짜,시작일,종료일):
    col1,col2=st.columns([1,1])
    with col1:
        df=pd.read_excel('./Data/배당농부법종목.xlsx')
        df["티커"]=df["티커"].apply(lambda x: str(x).zfill(6))
        st.text('최근 20영업일 기관/외인 순매수 금액 상위 순')
        st.dataframe(df)
    with col2:
        st.write('[배당농부의 당신께 드리는 선물, 요즘 주식투자하는 방법](https://dividendfarmerdiary.tistory.com/m/364)')
        st.markdown('''
                    ###### :orange[1. 최근 20일동안 외국인과 기관이 가장 많이 매수한 종목 100개 선정]
                    ###### :orange[2. 100개 종목 중 20일선 위에서 주가가 형성된 것 선별]
                    ###### :orange[3. 선별된 종목 중 거래량이 전주 대비 3배이상 오른종목 선별]
                    ###### :orange[4. 15시에 주가가 어제보다 하락했는데, 거래량은 어제보다 적은 종목 매수]
                    ###### :orange[5. 음봉이 나올때까지 보유, 음봉이 나오고 외국인과 기관이 팔면 매도]
                    ''')
        
    티커s=df['티커'].unique().tolist()
    종목s=df['종목'].unique().tolist()
    _dict=dict(zip(종목s,티커s))

    col1,col2,col3=st.columns([1,1,2])
    with col1:
        종목=st.selectbox('선택',종목s)
        티커=_dict[종목]
    with col2:
        st.text('')
        st.text('')
        st.text(티커)
    with col3:
        st.text('')
        st.text('')
        자본총계,시가총액=GetData.종목별_현재_재무정보(_dict[종목])
        시총자본비율=format(시가총액/자본총계,'.2f')
        자본총계대비시총비율='자본총계대비 시총비율: '+시총자본비율
        st.write(자본총계대비시총비율)

    주가정보,내재가치=재무정보_보여주기(날짜, 시작일, 종료일, _dict[종목], 종목)

    return

def 매출증가_종목보기(날짜):
    st.text('최근3년 매출액 증가 및 영업이익 증가 종목 보기')
    # 시작일=str(get_date(날짜, 2000)).replace('-','')
    시작일=str(get_date(날짜, 260*2)).replace('-','')
    종료일=str(날짜).replace('-','')

    folder='./Data/'
    file='매출액변동상태.xlsx'
    df1=pd.read_excel(folder+file)
    df1["티커"]=df1["티커"].apply(lambda x: str(x).zfill(6))

    file='종목별테마.parquet'
    df2=pd.read_parquet(folder+file)[['티커','Theme','Sector']]
    df2["티커"]=df2["티커"].apply(lambda x: str(x).zfill(6))
    df2=df2.rename(columns={'Theme':'테마','Sector':'업종'})

    file='이동평균120기준 위치.xlsx'
    df3=pd.read_excel(folder+file)[['티커','위치']]
    df3["티커"]=df3["티커"].apply(lambda x: str(x).zfill(6))
    df3=df3.drop_duplicates(keep='first')

    df_merge=pd.merge(df1, df3, on='티커',how='left')
    df_merge=pd.merge(df_merge, df2, on='티커',how='left')

    col1,col2,col3,col4=st.columns([1,2,2,2])
    with col1:
        radio1=st.radio('선택',('테마별로 보기','위치별 보기'), key='r1')
        # radio1=st.radio('선택',('테마별로 보기','바닥기 보기','상승초기 보기','상승중기 보기','하락기 보기'), key='r1')
    if radio1=='테마별로 보기':
        with col2:
            radio2=st.radio('선택',('3년연속 매출상승 종목','전체'),key='r2')
        with col3:
            radio4=st.radio('선택',('전체','시총이 자본총계보다 작은것'),key='r4')
    else:
        with col2:
            radio3=st.radio('선택',('바닥기 보기','상승초기 보기','상승중기 보기','하락기 보기'), key='r3')
        with col3:
            radio2=st.radio('선택',('3년연속 매출상승 종목','전체'),key='r2')
        # with col4:
        #     radio4=st.radio('선택',('전체','시총이 자본총계보다 작은것'),key='r4')

    df_merge['테마'] = df_merge['테마'].fillna('테마없음')
    if radio2=='전체':
        pass
    else:
        df_merge=df_merge[df_merge['매출변동상태']==1] # 매출액 3년연속 증가
        df_merge=df_merge[df_merge['영업이익상태']<9] # 영업이익 최근3년중 2번이상 흑자

    if radio1=='테마별로 보기':
        # df_merge['테마'] = df_merge['테마'].fillna('테마없음')
        # df_merge=df_merge[df_merge['매출변동상태']==1] # 매출액 3년연속 증가
        # df_merge=df_merge[df_merge['영업이익상태']<9] # 영업이익 최근3년중 2번이상 흑자
        테마s=df_merge['테마'].unique().tolist()

        테마s=[ x for x in 테마s if "신규상장" not in x ]
        테마s=[ x for x in 테마s if "기업인수목적회사" not in x ]
        테마s=[ x for x in 테마s if "창투사" not in x ]
        테마s=[ x for x in 테마s if "지주사" not in x ]

        col1,col2=st.columns([1,3])
        with col1:
            테마=st.selectbox('테마선택',테마s)
            df_테마=df_merge[df_merge['테마']==테마]
            df_테마.sort_values(by='전년대비증감율',ascending=False,inplace=True)        
            티커s=df_테마['티커'].unique().tolist()
            종목s=df_테마['종목'].unique().tolist()
            # 종목=st.selectbox('선택',종목s)
            # _dict=dict(zip(종목s,티커s))
            # st.dataframe(df_merge[df_merge['종목']==종목][['테마','업종']])
            if radio4=='시총이 자본총계보다 작은것':
                티커1s=[]
                for 티커 in 티커s:
                    자본총계,시가총액=GetData.종목별_현재_재무정보(티커)
                    시총자본비율=시가총액/자본총계
                    if 시총자본비율<1.01: 
                        st.write(티커,자본총계,시가총액, 시가총액/자본총계)
                        티커1s.append(티커)
                종목1s=df_테마[df_테마['티커'].isin(티커1s)]['종목'].tolist()
                티커s=티커1s; 종목s=종목1s

            종목=st.selectbox('선택',종목s)
            _dict=dict(zip(종목s,티커s))
            st.dataframe(df_merge[df_merge['종목']==종목][['테마','업종']])

        with col2:
            st.write('테마종류:',len(테마s),'선택된 테마의 종목수:',len(티커s))
            st.dataframe(df_테마)

            자본총계,시가총액=GetData.종목별_현재_재무정보(_dict[종목])
            시총자본비율=format(시가총액/자본총계,'.2f')
            자본총계대비시총비율='자본총계대비 시총비율: '+시총자본비율
            st.write(자본총계대비시총비율)
            # container.text('** 1 이하가 좋은 것 **')


        # 재무정보 보여주기
        주가정보,내재가치=재무정보_보여주기(날짜, 시작일, 종료일, _dict[종목], 종목)

        st.write(len(df_merge['티커'].unique().tolist()))
        df_merge.sort_values(by='전년대비증감율',ascending=False, inplace=True)
        st.dataframe(df_merge)

        return
    
    if radio3=='바닥기 보기':
        바닥기=['겨울1','겨울2','겨울3']
        df_위치=df_merge[df_merge['위치'].isin(바닥기)].sort_values(by='전년대비증감율', ascending=False)
    if radio3=='상승초기 보기':
        상승초기=['봄1','봄2','봄3']
        df_위치=df_merge[df_merge['위치'].isin(상승초기)].sort_values(by='전년대비증감율', ascending=False)
    if radio3=='상승중기 보기':
        상승중기=['여름1','여름2','여름3']
        df_위치=df_merge[df_merge['위치'].isin(상승중기)].sort_values(by='전년대비증감율', ascending=False)
    if radio3=='하락기 보기':
        하락기=['가을1','가을2','가을3']
        df_위치=df_merge[df_merge['위치'].isin(하락기)].sort_values(by='전년대비증감율', ascending=False)

    if len(df_위치)>0:
        st.dataframe(df_위치)
        종목s=df_위치['종목'].unique().tolist()
        티커s=df_위치['티커'].unique().tolist()
        st.write('120이평 이격률 기준',len(종목s))
        col1,col2=st.columns([1,4])
        with col1:
            종목=st.selectbox('선택',종목s)
            container=st.container()
        with col2:
            st.dataframe(df_위치[df_위치['종목']==종목])
        _dict=dict(zip(종목s,티커s))

        자본총계,시가총액=GetData.종목별_현재_재무정보(_dict[종목])
        시총자본비율=format(시가총액/자본총계,'.2f')
        자본총계대비시총비율='자본총계대비 시총비율: '+시총자본비율
        container.write(자본총계대비시총비율)
        container.text('** 1 이하가 좋은 것 **')

        주가정보,내재가치=재무정보_보여주기(날짜, 시작일, 종료일, _dict[종목], 종목)

        # # 일자별 시가총액 조회
        # 시총=GetData.종목별_시가총액_기간(시작일,종료일,_dict[종목]).reset_index()
        # 시총['날짜']=시총['날짜'].dt.strftime('%Y-%m-%d')
        # 시총['시가총액(억)']=(시총['시가총액']/100000000).astype(int) # 억단위로 조정

        # Chart.차트_시가총액(시총,종목)

    return

def 차트영웅_저평가종목(조회일):

    df=pd.read_excel('./Data/관심주_차트영웅저평가.xlsx')
    df["티커"]=df["티커"].apply(lambda x: str(x).zfill(6))

    티커s=df['티커'].unique().tolist()
    종목s=df['종목명'].unique().tolist()
    _dict=dict(zip(종목s,티커s))

    col1, col2=st.columns([1,3])
    with col1:
        종목=st.selectbox('선택',종목s)
        티커=_dict[종목]
        st.text(종목+' : '+티커)
        자본총계,시가총액=GetData.종목별_현재_재무정보(티커)
        시총자본비율=format(시가총액/자본총계,'.2f')
        자본총계대비시총비율='자본총계대비 시총비율: '+시총자본비율
        st.text(자본총계대비시총비율)
    with col2:
        st.dataframe(df[['티커','종목명','Theme','Sector','Total_Rank']])

    # 재무정보 보여주기
    시작일=str(get_date(조회일, 2000)).replace('-','')
    종료일=str(조회일).replace('-','')
    주가정보,내재가치=재무정보_보여주기(조회일, 시작일, 종료일, 티커, 종목)

    시작일=str(get_date(조회일, 730)).replace('-','')  # 2년
    종료일=str(조회일).replace('-','')
    df_거래대금=GetData.종목별_거래대금(시작일,종료일,티커)

    df_w=df_거래대금.resample('W').agg({'기관합계':'sum','기타법인':'sum','개인':'sum','외국인합계':'sum'})
    df_m=df_거래대금.resample('M',closed='right',label='right').agg({'기관합계':'sum','기타법인':'sum','개인':'sum','외국인합계':'sum'})

    Chart.차트_거래대금(df_거래대금[100:],종목,'일')
    Chart.차트_거래대금(df_w,종목,'주')
    Chart.차트_거래대금(df_m,종목,'월')

    return

def 거래량폭증_종목보기(조회일):

    radio=st.radio('선택',('발굴된 종목 보기', '발굴하기'))
    if radio=='발굴된 종목 보기':
        folder='./Data/'
        작업파일='관심주_기타.xlsx'
        df1=pd.read_excel(folder+작업파일,sheet_name=0)
        df2=pd.read_excel(folder+작업파일,sheet_name=1)
        df3=pd.read_excel(folder+작업파일,sheet_name=2)
        df1["티커"]=df1["티커"].apply(lambda x: str(x).zfill(6))
        df2["티커"]=df2["티커"].apply(lambda x: str(x).zfill(6))
        df3["티커"]=df3["티커"].apply(lambda x: str(x).zfill(6))

        종목s=df3['종목'].tolist()
        col1, col2, col3=st.columns([3,2,10])
        with col1:
            종목선택=st.selectbox('종목선택',종목s)
            설명=df3[df3['종목']==종목선택]['설명'].tolist()
        with col2:
            구분=df3[df3['종목']==종목선택]['구분'].tolist()
            발굴일자=df3[df3['종목']==종목선택]['날짜'].tolist()
            st.text('')
            st.text('')
            칼럼2정보=구분[0]+'\n'+발굴일자[0]
            st.text(칼럼2정보)
        with col3:
            st.text(설명[0])

        df=pd.read_excel('./Data/거래량폭증종목.xlsx')
        df["티커"]=df["티커"].apply(int)
        df["티커"]=df["티커"].apply(lambda x: str(x).zfill(6))
        df['기간최고가일']=pd.to_datetime(df['기간최고가일']).dt.strftime('%Y-%m-%d')
        df['기간최저가일']=pd.to_datetime(df['기간최저가일']).dt.strftime('%Y-%m-%d')
        df_종목=df[df['종목']==종목선택]
        티커=df_종목['티커'].values[0]
        최고가=df_종목['기간최고가'].values[0]
        최저가=df_종목['기간최저가'].values[0]
        계산값1,계산값2,피보값=Strategy.피보나치_위치별가격(최고가,최저가)

        공용화면보기1(조회일,종목선택,티커,종목선택,df_종목,최고가,최저가,계산값1,계산값2,피보값)

        st.dataframe(df_종목)
    # 발굴하기
    else:
        st.caption('120일 상승종목은 2023년 3월 10일 부터 가능 / RSI30이하,RSI70이상은 2023년4월14일부터 가능')
        df=pd.read_excel('./Data/거래량폭증종목.xlsx')
        df["티커"]=df["티커"].astype(int)
        df["티커"]=df["티커"].apply(lambda x: str(x).zfill(6))

        날짜s=df['날짜'].unique().tolist()
        # 날짜s=reversed(날짜s)
        날짜=st.selectbox('날짜선택',날짜s)
        df=df[df['날짜']==날짜]
        col1,col2=st.columns([1,4])
        with col1:
            radio=st.radio('선택',('20일 평균거래량 10배이상','20일 평균거래량 5배이상','120이평 상승중 종목','240이평 상승중 종목','30주 골든크로스',
                                   '20/60 골든크로스','RSI30이하','RSI70이상','거래대금 1000억이상','거래대금 2000억이상'))
            if radio=='20일 평균거래량 5배이상': df=df[(df['거래량20대비']>4.99) & (df['거래량20대비']<10)]
            elif radio=='20일 평균거래량 10배이상': df=df[df['거래량20대비']>9.99]
            elif radio=='120이평 상승중 종목': df=df.query('상태120=="120이평 상승중"')
            elif radio=='30주 골든크로스': df=df.query('주30돌파==1')
            # elif radio=='RSI30이하': df=df.query('rsi14<30.001')
            # elif radio=='RSI70이상': df=df.query('rsi14>69.999')
            elif radio=='RSI30이하': df=df.query('rsi<30.001')
            elif radio=='RSI70이상': df=df.query('rsi>69.999')
            elif radio=='거래대금 1000억이상': df=df.query('거래대금>99999999999')
            elif radio=='거래대금 2000억이상': df=df.query('거래대금>199999999999')
            else: df=df[df['position2060']==1]

            바닥=['겨울3','겨울2','겨울1']
            상승초=['봄1','봄2','봄3']
            상승중=['여름1','여름2','여름3']
            하락=['가을1','가을2','가을3']
            선택=st.selectbox('선택',['바닥기','상승초기','상승중기','하락기','전체'])
           
            if 선택=='바닥기': 위치=st.radio('단계선택',바닥)
            elif 선택=='상승초기': 위치=st.radio('단계선택',상승초)
            elif 선택=='상승중기': 위치=st.radio('단계선택',상승중)
            elif 선택=='하락기': 위치=st.radio('단계선택',하락)
            else: pass
            
            if 선택=='전체': df.sort_values(by=['위치','종목'], ascending=[True,True], inplace=True)
            else: df=df[df['위치']==위치]; df.sort_values(by='거래대금20대비', ascending=False, inplace=True)

            종목s=df['종목'].unique().tolist()
            st.write(len(종목s),'건')
        with col2:
            if radio=='120일평 상승중 종목': st.caption('2023년 3월 10일 부터 가능..!!')
            if len(df)<1: st.markdown('''###### :orange[해당종목 없음..!!]'''); return
            st.dataframe(df)

        col1,col2=st.columns([1,5])
        with col1:
            종목선택=st.selectbox('종목선택',종목s)
            container=st.container()
        with col2:
            df_종목=df[df['종목']==종목선택]
            티커=df_종목['티커'].values[0]
            최고가=df_종목['기간최고가'].values[0]
            최저가=df_종목['기간최저가'].values[0]
            st.dataframe(df_종목)

            계산값1,계산값2,피보값=Strategy.피보나치_위치별가격(최고가,최저가)

        try:
            container.text(df_종목['단기상태'].values[0]+'\n'+df_종목['상태60'].values[0]+'\n'+df_종목['상태120'].values[0]+'\n'+df_종목['상태240'].values[0]+'\n' \
                        +'rsi: '+str(round(df_종목['rsi'].values[0],2))+'\n'+'RS: '+str(round(df_종목['RS'].values[0],2)))
        except:
            container.text('120/240 상승중 족목은 2023년3월10일 이후부터 가능..!!'+'\n'+'30주 골든 크로스는 2023년3월13일 부터 가능..!!')

        # 공용화면보기1
        공용화면보기1(조회일,종목선택,티커,종목선택,df_종목,최고가,최저가,계산값1,계산값2,피보값)

    return

def 골든크로스_2060(조회일):

    df=pd.read_excel('./Data/이동평균120기준 위치.xlsx')
    df["티커"]=df["티커"].apply(lambda x: str(x).zfill(6))
    col1,col2=st.columns([1,4])
    with col1:
        radio=st.radio('선택',['골든크로스(20/60)','데드크로스(20/60)'])
        container=st.container()
    with col2:
        if radio=='골든크로스(20/60)':
            df=df[df['position2060']==1]
        else:
            df=df[df['position2060']==-1]
        df.sort_values(by='위치',ascending=True,inplace=False)
        st.dataframe(df)
        
    바닥=['겨울3','겨울2','겨울1']
    상승초=['봄1','봄2','봄3']
    상승중=['여름1','여름2','여름3']
    하락=['가을1','가을2','가을3']
    선택=container.selectbox('선택',['바닥기','상승초기','상승중기','하락기'])

    if 선택=='바닥기': 위치=container.radio('단계선택',바닥)
    elif 선택=='상승초기': 위치=container.radio('단계선택',상승초)
    elif 선택=='상승중기': 위치=container.radio('단계선택',상승중)
    else: 위치=container.radio('단계선택',하락)
    df=df[df['위치']==위치]

    if len(df)<1: st.text('해당위치 종목 없음..!!'); return
    종목s=df['종목'].unique().tolist()
    container.write(len(종목s))
    종목선택=container.selectbox('선택',종목s)
    티커=df[df['종목']==종목선택]['티커'].values[0]
    container.caption(티커)
    
    # 재무정보 보여주기
    시작일=str(get_date(조회일, 2000)).replace('-','')
    종료일=str(조회일).replace('-','')
    주가정보,내재가치=재무정보_보여주기(조회일, 시작일, 종료일, 티커, 종목선택)
    
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
    df1['날짜']=pd.to_datetime(df1['날짜']).dt.strftime('%Y%m%d')
    df2['날짜']=pd.to_datetime(df2['날짜']).dt.strftime('%Y%m%d')
    df3['날짜']=pd.to_datetime(df3['날짜']).dt.strftime('%Y%m%d')
    df1['해당년월']=df1['해당년월'].astype(str)
    df2['해당년월']=df2['해당년월'].astype(str)
    df3['해당년월']=df3['해당년월'].astype(str)
    선정년월s=df1.해당년월.unique().tolist()
    선정년월s.reverse()

    col1, col2, col3, col4, col5=st.columns([1,1,2,1,2])
    with col1:
        # 선정년월=['202303','202302']
        년월=st.selectbox('선택',선정년월s)
        df1=df1[df1['해당년월']==년월]
        df2=df2[df2['해당년월']==년월]
        df3=df3[df3['해당년월']==년월]
        st.write(len(df1),len(df2),len(df3))
    with col2:
        radio1=st.radio('선택',('테마별 보기','전체보기'))
    with col3:
        if radio1=='테마별 보기':
            if len(df3)>0:
                테마s=df3['설명'].unique().tolist()
                테마선택=st.selectbox('선택',테마s)
                df3=df3[df3['설명']==테마선택]
                티커s=df3['티커'].tolist()
                df1=df1[df1["티커"].isin(티커s)]
                df2=df2[df2["티커"].isin(티커s)]
            else: st.text('해당년월 자료 없음..!!'); return
    with col4:
        선택위치=st.selectbox('위치',['전체','겨울3','겨울2','겨울1','봄1','봄2','봄3','여름1','여름2','여름3','가을1','가을2','가을3'])
        if 선택위치!='전체':
            df2=df2[df2['파동위치1']==선택위치]
            티커s=df2['티커'].tolist()
            if len(티커s)>0:
                df1=df1[df1["티커"].isin(티커s)]
                df3=df3[df3["티커"].isin(티커s)]
            else: st.text('해당위치 자료 없음..!!'); return            
    with col5:
        radio2=st.radio('선택',('120이평 작은순 보기', '120이평 큰순 보기'))
        if radio2=='120이평 작은순 보기':
            df2.sort_values(by='이평120이격률',ascending=True,inplace=True)
        else: df2.sort_values(by='이평120이격률',ascending=False,inplace=True)
  
        st.write('총', str(len(df2)),'건')

    st.dataframe(df2)

    ######
    종목s=df2['종목'].unique().tolist()
    종목=st.sidebar.selectbox('선택',종목s)
    티커=df2[df2['종목']==종목]['티커'].values[0]

    상승파동비율=df1[df1['티커']==티커].transpose()
    위치정보=df2[df2['티커']==티커].transpose()

    # 최근주가 가져오기
    시작일=str(get_date(조회일, 5)).replace('-','')  # 조회일로부터 5일전 부터 데이타 가져오기
    종료일=str(조회일).replace('-','')
    관심주_보기(티커, 종목, 상승파동비율, 위치정보, stock.get_market_ohlcv(시작일, 종료일, 티커),'관심주')

    # 재무정보 보여주기
    시작일=str(get_date(조회일, 2000)).replace('-','')
    종료일=str(조회일).replace('-','')
    주가정보,내재가치=재무정보_보여주기(조회일, 시작일, 종료일, 티커, 종목)

    # 일간 차트 그리기
    freq='d'
    df, df_w=Dart.Stock_OHLCV_조회(시작일, 종료일, 티커,freq)
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

    col1,col2=st.columns([2,5])
    with col1:
        radio=st.radio('선택',('상승/하락순 보기','최고가대비 하락/상승순 보기'))
        container=st.container()
        # radio=st.radio('선택',('코스피보다 더 상승한 종목보기', '상승/하락순 보기','최고가대비 하락/상승순 보기'))
    with col2:
        st.markdown('''
            ###### :violet[2023-04-05(수) 에스엘/명신산업(자동차부품)/한국항공우주/한화에어로스페이스/현대로템(방위산업.우주항공)]
            ###### :green[2023-04-04(화) 넷마블(게임)/케이카(렌트카)]
            ###### :orange[2023-04-03(월) GS건설/현대건설/한화에어로스페이스/HDC현대산업개발/대우건설/대우조선해양/풍산/GKL/GS리테일/롯데칠성/현대로템/LX인터네셔널/팬오션]
            ###### :blue[2023-03-09(목) 한미사이언스/HDC현대산업개발/한전기술/두산에너빌리티/SK바이오사이언스/에스엘]
        ''')

    if radio=='상승/하락순 보기':
        보기기준=container.selectbox('선택',['일자순','주간순','월간순'])
        col1,col2=st.columns([1,1])
        with col1:
            # st.text('-- 상승률순 --')
            # df.sort_values(by='등락률', ascending=False, inplace=True)


            if 보기기준=='일자순': st.text('-- 상승률순(일자순) --'); df.sort_values(by='등락률', ascending=False, inplace=True)
            elif 보기기준=='주간순': st.text('-- 상승률순(주간순) --'); df.sort_values(by='등락률(주)', ascending=False, inplace=True)
            else: st.text('-- 상승률순(월간순) --'); df.sort_values(by='등락률(주)', ascending=False, inplace=True)


            df.reset_index(inplace=True)
            df.drop('index', axis=1, inplace=True)
            st.dataframe(df)

            종목1s=df['종목'].tolist()
            종목1=st.selectbox('선택',종목1s,key='종목1')
            티커1=df[df['종목']==종목1]['티커'].values[0]
            위치=df[df['종목']==종목1]['위치'].values[0]

            결과단기=df[df['종목']==종목1]['단기상태'].values[0]
            결과60=df[df['종목']==종목1]['상태60'].values[0]
            결과120=df[df['종목']==종목1]['상태120'].values[0]
            결과240=df[df['종목']==종목1]['상태240'].values[0]
            RS일=df[df['종목']==종목1]['RS(일)'].values[0]
            RS주=df[df['종목']==종목1]['RS(주)'].values[0]
            RS월=df[df['종목']==종목1]['RS(월)'].values[0]

            st.text(티커1+'\n'+위치+'\n'+결과단기+'\n'+결과60+'\n'+결과120+'\n'+결과240)
            st.text('RS(일): '+str(round(RS일,2))+'\n'+'RS(주): '+str(round(RS주,2))+'\n'+'RS(월): '+str(round(RS월,2)))

        with col2:
            # st.text('-- 하락순 --')
            # df.sort_values(by='등락률', ascending=True, inplace=True)

            if 보기기준=='일자순': st.text('-- 하락률순(일자순) --'); df.sort_values(by='등락률', ascending=True, inplace=True)
            elif 보기기준=='주간순': st.text('-- 하락률순(주간순) --'); df.sort_values(by='등락률(주)', ascending=True, inplace=True)
            else: st.text('-- 하락률순(월간순) --'); df.sort_values(by='등락률(주)', ascending=True, inplace=True)


            df.reset_index(inplace=True)
            df.drop('index', axis=1, inplace=True)
            st.dataframe(df)

            종목2s=df['종목'].tolist()
            종목2=st.selectbox('선택',종목2s,key='종목2')
            티커2=df[df['종목']==종목2]['티커'].values[0]
            위치=df[df['종목']==종목2]['위치'].values[0]

            결과단기=df[df['종목']==종목2]['단기상태'].values[0]
            결과60=df[df['종목']==종목2]['상태60'].values[0]
            결과120=df[df['종목']==종목2]['상태120'].values[0]
            결과240=df[df['종목']==종목2]['상태240'].values[0]
            RS일=df[df['종목']==종목2]['RS(일)'].values[0]
            RS주=df[df['종목']==종목2]['RS(주)'].values[0]
            RS월=df[df['종목']==종목2]['RS(월)'].values[0]

            st.text(티커2+'\n'+위치+'\n'+결과단기+'\n'+결과60+'\n'+결과120+'\n'+결과240)
            st.text('RS(일): '+str(round(RS일,2))+'\n'+'RS(주): '+str(round(RS주,2))+'\n'+'RS(월): '+str(round(RS월,2)))

        # 재무정보 보여주기
        st.write('-----')
        조회일=datetime.datetime.today()
        종료일=datetime.datetime.today()
        시작일=get_date(종료일,1000).replace('-','')
        조회일=조회일.strftime('%Y-%m-%d').replace('-','')
        종료일=종료일.strftime('%Y-%m-%d').replace('-','')
        주가정보,내재가치=재무정보_보여주기(조회일, 시작일, 종료일, 티커1, 종목1)
        주가정보,내재가치=재무정보_보여주기(조회일, 시작일, 종료일, 티커2, 종목2)    

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

    col1, col2, col3, col4=st.columns([1,2,2,2])
    with col1:
        st.text('')
        # 개별종목 주가 가져오기
        주가정보,주봉정보=Dart.Stock_OHLCV_조회(시작일, 종료일, 티커, 'd')

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
        참조링크보기(티커,종목)

    with col2:
        # 재무정보,재무비율=Dart.get_CompanyGuide자료(티커).transpose()
        재무정보,재무비율=Dart.get_CompanyGuide자료(티커)
        col_names=재무정보.columns
        if len(재무정보)>0:
            st.text('재무정보(분기)')
            st.dataframe(재무정보.iloc[4:,:].T)
    with col3:
        if len(재무정보)>0:
            st.text('재무정보(년간)')
            st.dataframe(재무비율.T)
    with col4:
        try:
            시작일=str(get_date(pd.to_datetime(조회일), 2000)).replace('-','')
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

    # 일자별펀더멘털=GetData.종목별_펀더멘털_기간(시작일,종료일,티커)['PER'].reset_index()
    # 일자별펀더멘털['날짜']=일자별펀더멘털['날짜'].dt.strftime('%Y-%m-%d')
    # Chart.차트_PER(일자별펀더멘털,종목)


    # 일자별 펀더멘털 조회
    일자별펀더멘털=GetData.종목별_펀더멘털_기간(시작일,종료일,티커)

    # 일자별 DIV/DPS 조회
    일자별DIV=일자별펀더멘털[['DIV','DPS']].reset_index()
    일자별DIV['날짜']=일자별DIV['날짜'].dt.strftime('%Y-%m-%d')
    Chart.차트_배당정보(일자별DIV,종목)
    # Chart.차트_DIV(일자별DIV,종목)
    
    # 일자별 PER 조회
    일자별PER=일자별펀더멘털['PER'].reset_index()
    일자별PER['날짜']=일자별PER['날짜'].dt.strftime('%Y-%m-%d')
    Chart.차트_PER(일자별PER,종목)


    # 일자별 시가총액 조회
    시총=GetData.종목별_시가총액_기간(시작일,종료일,티커).reset_index()
    시총['날짜']=시총['날짜'].dt.strftime('%Y-%m-%d')
    시총['시가총액(억)']=(시총['시가총액']/100000000).astype(int) # 억단위로 조정
    Chart.차트_시가총액(시총,종목)

    return 주가정보.iloc[-1],내재가치

def 관심주_보기(티커, 종목, 상승파동비율, 위치정보, 최근주가,보기기준):
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

        # st.write('[경기상황정리](https://docs.google.com/spreadsheets/d/14OhuYvmkb3dZUIpxP9mu9uS1zNxUY3gFnafHOWOYs5o/edit#gid=719655173)')
        # st.write('[기법정리](https://docs.google.com/spreadsheets/d/1tJg4kfIIpt17LNKXoKwzzallnXPmyCzMF1DhIIw1Q-8/edit#gid=1186881965)')
        # st.write('[KT(030200) 보유주](https://docs.google.com/spreadsheets/d/1A_8rYBwU35sfWJezUcKGaFiofMc0cp39TZQCkdSA6Rw/edit#gid=0)')
        # st.write('[유라테크(048430) 관심주](https://docs.google.com/spreadsheets/d/1IwcqZpn8_yiw-ZwX8kJW3na9d5Xy_aLY9Bv4X1WruLY/edit#gid=743352833)')

    with col2:
        st.markdown(f'''###### :orange[{티커}]''')
        종가=상승파동비율.loc['종가'].values[0]

        if (보기기준=='전월 10이평 돌파 종목') or (보기기준=='수급주'):
            숙향가치=상승파동비율.loc['내재가치'].values[0]
        else: 숙향가치='n/a'
        가격='종가: '+str(종가)+'\n'
        내재가치='내재가치: '+str(숙향가치)+'\n'+'\n'

        이동평균120=위치정보.loc['이평120'].values[0]
        이격률120=위치정보.loc['이평120이격률'].values[0]
        if (보기기준=='전월 10이평 돌파 종목') or (보기기준=='수급주') or (보기기준=='관심주'):
            주봉60시가=위치정보.loc['주봉60시가'].values[0]
            주봉60종가=위치정보.loc['주봉60종가'].values[0]
            차이3년='n/a'
        else:
            이동평균3년=위치정보.loc['3년이평'].values[0]
            이격률3년=위치정보.loc['3년이평이격률'].values[0]
            차이3년=현재가-이동평균3년
        if 보기기준=='관심주':
            이동평균3년최근='n/a'
            이격률3년최근='n/a'
            차이3년최근='n/a'
        else:
            이동평균3년최근=위치정보.loc['3년이평최근'].values[0]
            이격률3년최근=위치정보.loc['3년이격률최근'].values[0]
            차이3년최근=현재가-이동평균3년최근

        차이120=현재가-이동평균120

        이동평균120값='120이동평균: '+str(이동평균120)+'('+str(이격률120)+')'+'\n'
        if (보기기준=='전월 10이평 돌파 종목') or (보기기준=='수급주') or (보기기준=='관심주'):
            주봉60시가종가값='주봉60시가/종가: '+str(주봉60시가)+'/'+str(주봉60종가)+'\n'
        else:
            이동평균3년값='3년이동평균: '+str(이동평균3년)+'('+str(이격률3년)+')'+'\n'
        이동평균3년최근값='3년이동평균(최근): '+str(이동평균3년최근)+'('+str(이격률3년최근)+')'+'\n'+'\n'
        차이120값='120이동평균과 현재가의 차이: '+str(차이120)+'\n'
        차이3년값='3년이동평균과 현재가의 차이: '+str(차이3년)+'\n'
        차이3년최근값='3년이동평균최근과 현재가의 차이: '+str(차이3년최근)

        if (보기기준=='전월 10이평 돌파 종목') or (보기기준=='수급주') or (보기기준=='관심주'):
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