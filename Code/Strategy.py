import streamlit as st

def 피보나치_위치별가격(최고가,최저가):

    계산값1=[];계산값2=[]
    차액=최고가-최저가
    피보값=[23.6, 38.2, 50, 61.8, 100, 138.2, 161.8,200]
    for 수치 in 피보값:
        계산값1.append(최저가*(1+수치/100))
        계산값2.append(최저가+차액*수치/100)
    return 계산값1,계산값2,피보값

def 강영현투자법():

    st.markdown('''
                ###### :orange[1. 1년에 3~4회 매매로 연봉보다 더 버는법.]
                ###### :blue[- 대한민국은 박스권 장이다.]
                ###### :blue[- 그러므로 박스권이 어디인가를 판단 하는것이 중요하다.]
                ###### :blue[- 박스권 저점은 신용잔고가 털리는 것을 확인한다. 신용이 털렸다는 뉴스가 나오면 KODEX200 ETF를 매수 한다.]
                ###### :blue[- 신용잔고 확인법 설명: https://economyplay.tistory.com/310]
                ###### :blue[- 네이버 고객예탹금 & 신용잔고: https://finance.naver.com/sise/sise_deposit.naver]
                ###### :blue[- 금융투자협회 신용공여 잔고 추이: http://freesis.kofia.or.kr/]
                ###### :blue[- 매수한 ETF의 수익이 15%~30%를 달성하면 매도 한다.]
                ###### :blue[- 1년 3,4회 이것을 반복한다.]
                ###### :blue[- 박스권의 고점은 per이 12배 이다.]
                ###### :orange[2. 시장의 바닥 확인법.]
                ###### :blue[- 실업률이 증가 되었다가 줄어 드는 싯점 => 9월 부동산 건설에서 착공이 줄어 들면서 실업률이 늘어나기 시작]
                ###### :blue[- 연방은행 이자율이 내리기 시작 => 불황의 시작을 의미 => 주식 시장은 더 내려가기 시작한다.]
    

                ###### :orange[3. 곱버스 개인 반대 전략(강환국)]
                ###### :red[*11월에서 다음해4월은 전통적으로 장이 강하나, 5월~10월은 장이 매우 약하다. 가끔 코스피는 4월이 5%이상 상승하면 코스피가 5월,10월도 상승하나 코스닥은 여전 약하다]
                ###### :blue[- 개인이 3/5/10/20/50일 동안 개인이 곱버를 순매수 하면 개인은 하락에 배팅을 한것이므로 우리는 KODEX200에 배팅을 한다.]
                ###### :blue[- 개인이 3/5/10/20/50일 동안 개인이 곱버를 순매도 하면 개인은 상승에 배팅을 한것이므로 우리는 KODEX인버스에 배팅을 한다.]
                ###### :red[* 특히 5월,10월은 코스닥이 매우 좋지 않으므로 코스닥150선물 인버스에 배팅을 한다]



                ''')


    return

def 현장세_보기():
    st.markdown('''
            ###### :red[약세장 초반이다]
            ###### :orange[주도 업종: 필수 소비재, 의료, 식품, 제약(기본 소비재를 포함한 방어주)]
            ###### :orange[최고 종목: 음료수, 화장품, 식품, 의료, 제약, 담배]
            ''')

    st.write('[기준금리 7연속 인상…“오랜 기간 ‘高금리’ 불가피할 듯”](https://www.segye.com/newsView/20230115503368?OutUrl=naver)')
    st.write('[2023-01-13_US annual CPI inflation drops to 6.5% in December as expected](https://www.fxstreet.com/news/breaking-us-annual-cpi-inflation-drops-to-65-in-december-as-expected-202301121330)')

    st.text('2023년 1월 3일 코스피 2218.68, RSI10이 23.42, 볼린저 하단선 2254를 하향 돌파 후 반등하여 단기 반등 중이다.'+'\n'
            '추세는 여전히 하락 중이나 2023년 1월, 2월은 단기 상승 후 3,4월 고점을 형성 후 다시 하락 할 것으로 예상 된다.')
    st.text('2023년 1분기 전략'+'\n'
            '1월, 2월 매수/보유(이번 반등장은 코스닥 중.소형주 위주로 매매)'+'\n'
            '3월, 4월 매도'+'\n')
    st.text('5월~10월은 폭락장이 나올 수 있다'+'\n'
            '대응은 곱버를 매수 하거나 매매를 쉰다(매우 조심해야 한다)')

    return

def 급등예상주발굴매매법():

    st.write('[주식투자 최적의 타이밍을 잡는 범/스탠 와인스타인/부자회사원](https://myrichlife.tistory.com/474)')
    st.write('[주식매매 관련 기법 총정리](https://m.blog.naver.com/hankng/221560696297)')
    st.write('[급등 예상주 발굴 매매 기법(전체)](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=tujadr&logNo=80135979205)')

    st.markdown('''
            ##### :orange[-- 주도주 찾는 법 --]
            ###### :blue[1. 숲을보고 나무를 찾아 시나리오를 짠다.]
            ###### :green[-- 외국인, 투신 매매동향, 수급분석, 금리.환율.선물.뉴스등을 통해 시장 변화를 파악한다.]
            ###### :green[-- 업종별, 대형/중형/소형에서 가장 빠르고 크게 움직이는 종복 검색(동종비교, 상대 우위성)]
            ###### :blue[2. 매수 시그널 파악]
            ###### :green[-- 월,주,일,분,30분봉을 차례로 확인하여 5개월(일) 이평선 돌파 종목]
            ###### :green[3. 유동성 장세인 경우(큰 시세가 나는 장)]
            ###### :green[-- 피날레는 결국 대형주가 한다.]
            ###### :green[4. 조정장세인 경우]
            ###### :green[-- 테마주, 중소형주, 스몰캡, 저가중등 특히 순환매 주의]
            ''')

    st.markdown('''
            ##### :orange[-- 급등 예상주 발굴 매매법 --]
            ###### :green[1. 이평선 정배열하의 점프 종목]
            ###### :green[2. 신고가를 가볍게 돌파(대기 매물대를 가볍계 돌파하는 종목) => 강력한 매수 세력 존재 의미]
            ###### :green[3. 2중,3중의 바닥을 다진 종목 중 이평선 정배열 전환 종목(저향선을 모두 뚫었다는 의미)]
            ###### :orange[4. 주가가 60일, 120일선을 돌파 후 2달이상 빠지지 않는 종목]
            ###### :green[5. 역배열하의 이격큰 종목, 즉 장기하락 중 단기급락주(골이 깊으면 산이 높다)]
            ###### :green[6. V자 바닥형(급락후 매도세력 전멸로 일시적인 매물 공백상태)-되돌림/목눌림 구분 필요]
            ###### :green[7. 거래량 연중 최저에서 방향을 바꾸거나 주가가 하락할수록 거래량이 늘어나는 종목]
            ###### :green[8. 장기간 횡보하고 최근 6개월 거래량 최저점 기록한 종목]
            ###### :green[9. 매물 부담이 적고 전고점 거래가격대와 괴리도가 큰 종목이 거래량이 늘어 나면서 상승]
            ###### :green[** 편승: 거래량 급증하며 상승시 매물 저항이 크지 않은 경우]
            ###### :green[** 하차: 거래량 급증하며 사승 하였지만 상승폭이 작거나 빠지면서 3일연속 거래량 지속(세력실패)]
            ''')
    
    return

def 주식시장순환원리_나바로():

    현장세_보기()

    chk1=st.checkbox('전체내용 보기',value=False)
    if chk1:
        col1,col2,col3=st.columns(3)
        with col1:
            st.markdown('''
                    ##### :orange[--강세장에 대한 정리--]
                    ###### :red[1. 강세장 초반]
                    ###### :red[- 주도업종: 운송]
                    ###### :red[- 최고업종: 철동, 해운]
                    ###### :green[2. 강세장 초반~중반]
                    ###### :green[- 주도업종: 기술]
                    ###### :green[- 최고업종: 컴퓨터, 전자, 반도체]
                    ###### :orange[3. 강세장 중반~후반]
                    ###### :orange[- 주도업종: 자본재(설비투자)]
                    ###### :orange[- 최고업종: 전기설비, 중장비트럭, 기계와공구, 제조, 오염관리]
                    ###### :blue[4. 강세장 후반]
                    ###### :blue[- 주도업종: 기간산업, 화학, 원자재]
                    ###### :blue[- 최고업종: 알루미늄, 화학, 컨테이너, 금속, 제지/임산품, 철강]
                    ###### :red[5. 강세장 후반~정점]
                    ###### :red[- 주도업종: 에너지]
                    ###### :red[- 최고업종: 석유, 천연가스, 석탄]
                ''')
        with col2:
            st.markdown('''
                    ##### :orange[--약세장에 대한 정리--]
                    ###### :red[1. 약세장 초반]
                    ###### :red[- 주도업종: 필수소비재, 의료, 식품, 제약(기본 소비재를 포함한 방어주)]
                    ###### :red[- 최고업종: 음료수, 화장품, 식품, 의료, 제약, 담배]
                    ###### :green[2. 약세장 중반]
                    ###### :green[- 주도업종: 공익사업(전기, 가스, 통신)]
                    ###### :green[- 최고업종: 전기, 가스, 통신]
                    ###### :orange[3. 약세장 후반]
                    ###### :orange[- 주도업종: 금융, 소비, 순환재(자동차등)]
                    ###### :orange[- 최고업종: 자동차, 은행, 주택, 부동산, 소매]
                ''')
        with col3:
            st.markdown('''
                    ##### :orange[--경재 사이클--]
                    ###### :red[금리인상 => 사업비용 증가 => 물가상승 => 수요감소(소비감소) =>]
                    ###### :red[재고증가 => 노동시간단축 => 소득감소 => 매출하락 => 재고증가 =>]
                    ###### :red[직원해고 시작 => 더 큰 실업률 => 소득감소 => 소비감소]
                    ##### :blue[기본적 분석으로 종목 선택하고 기술적 분석으로 매매 타이밍을 잡는다]
                    ###### :blue[매크로 투자의 2가지 중요한 2가지 규칙]
                    ###### :blue[1.상승세에는 강한 업종의 강한 주식을 사라]
                    ###### :blue[2.하락세에는 약한 업종의 약한 주식을 공매도 하라]
                    ###### :green[매크로 투자자가 알아 둬야할 것]
                    ###### :green[1.경제가 불경기 일때는 재정 정책을]
                    ###### :green[2.경제가 완전고용 상태에 있을때는 통화정책 해법을 예상하라]
                ''')

    return

def 연봉돌파():

    st.markdown('''
            ###### :red[1. 매년 1월 첫째주에 선별 작업을 수행한다.]
            ###### :blue[2. 3년 이동평균값을 첫번째 중요 라인으로 결정한다.]
            ###### :green[3. 전 고점을 두번째 중요 라인으로 결정한다.]
            ###### :violet[4. 업종을 확인 한다.]
            ###### :orange[5. 테마를 확인 한다.]
            ###### :red[6. 지난 3년 이상의 재무상태를 확인한다.]
            ###### :blue[7. 최근 부터 과거의 뉴스를 확인 한다.]
            ###### :green[8. 차트의 위치와 테마의 순환성을 조사한다.]
            ###### :violet[9. 위의 내용을 엑셀파일에 저장한다.]
        ''')
    return

def 월봉돌파():

    radio=st.radio('선택',('월봉 10이평 돌파','월봉 20/60돌파 및 기준선 돌파'))
    if radio=='월봉 10이평 돌파':
        st.markdown('''
                ###### :red[1. 매월 1월 첫째주에 선별 작업을 수행한다.]
                ###### :blue[2. 10이평 돌파가 2차인것 선별.]
                ###### :green[3. 주봉에서 60이평 돌파 인것 선별.]
                ###### :orange[4. 업종을 확인 한다.]
                ###### :orange[5. 테마를 확인 한다.]
                ###### :red[6. 지난 3년 이상의 재무상태를 확인한다.]
                ###### :blue[7. 최근 부터 과거의 뉴스를 확인 한다.]
                ###### :green[8. 차트의 위치와 테마의 순환성을 조사한다.]
                ###### :violet[9. 위의 내용을 엑셀파일에 저장한다.]
                ###### :violet[10. 타점은 주봉의 몸통이다.]
            ''')
    return

def 거래량폭증():

    st.text('거래량 폭증 매매법')
    st.markdown('''
        ###### :green[1단계 - 온라인에서 거래량 폭증종목 보기에서 위치가 겨울1, 봄1, 봄2, 봄3에 있는 종목]
        ###### :green[1.1 과거 꼬리달린 매집봉이 얼마나 있는지 확인(많이 있을수록 신뢰도가 높다)]
        ###### :green[1.2 구름대 근방에 있는지 확인]
        ###### :green[1.3 외국인/기관 매집 확인]
        ###### :blue[2단계 - 재무정보 확인(온라인 화면 사용)]
        ###### :blue[2.1 매출성장여부(지난 3년간)]
        ###### :blue[2.2 매출이익/당기순이익(지난 3년간)]
        ###### :blue[2.3 유동비율/당좌비율/부채비율(지난 3년간)]
        ###### :blue[2.4 EPS/PER/PGR/ROE확인]
        ###### :green[3단계 - 상대강도(선도주인지 여부)]
        ###### :green[3.1 코스피 지수와 비교한 주가 상승률(업종, 전체)]
        ###### :green[3.2 네이버금융 사용]
        ###### :blue[4단계 - 발행주식수 확인(수요공급법칙)]
        ###### :blue[4.1 fnguide에서 확인]
        ###### :blue[4.2 3000만주 이하]
        ###### :blue[4.2 6000만주 이하(남석관)]
        ###### :green[5단계 - 새로운 변화 여부]
        ###### :green[5.1 새로운 제품]
        ###### :green[5.2 새로운 서비스]
        ###### :green[5.3 업계에서 일어난 변화]
        ###### :green[5.4 새로운 경영진]
        ###### :green[5.5 신고가 등..]
        ###### :blue[6단계 - 기관수급]
        ###### :blue[6.1 기관보유 20% 이하(네이버 금융)]
        ###### :blue[7단계 - 전체시장(하락장/상승장 여부)]
        ###### :blue[7.1 선도주 움직임 확인]
        ###### :blue[7.2 삼성전자/주가상승률 상위 종목(HTS)]
        ''')



    return

def 매매기술_설명():

    # 차트영웅 22가지 기술에 대한 원리
    # 1. 큰 흐름(년봉/월봉/주봉)에서 추가 상승이 나올 수 있는 패턴 발견 후
    # 2. 월봉/주봉에서 기준에 맞아야 하고
    # 3. 그다음 일봉에서 매매 타이밍(눌림목)이 나올 때까지 기다린다.
    #   - 기다리는 동안 해당 종목이 올라갈 수 있는 이유(기업, 재료, 차트)에 대한 분석을 진행 한다.
    # 4. 그 이후에 분봉상에서 매매 타점을 잡아 매수 진행 한다.

    # st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")
    # st.markdown('**:blue[전고점 돌파매매]**')
    # st.markdown('''
    #         ##### **:red[전고점 돌파매매 설명 보기]**
    #         ''')

    col1, col2=st.columns([1,3])
    with col1:
        선택=st.selectbox('큰 흐름상 돌파매매 설명보기',['거래량폭증','연봉돌파','월봉돌파','주봉돌파'])
    with col2:
        if 선택=='거래량폭증': 거래량폭증(); return
        if 선택=='연봉돌파': 연봉돌파(); return
        if 선택=='월봉돌파': 월봉돌파(); return

    return

def Strategy_2023():

    st.write('[2023년2월 매매전락](https://docs.google.com/spreadsheets/d/1sHyoHX7zW9kaMTFzEptQqRDP00MVAEN_mthdvljF1oM/edit#gid=)')
    st.text('3월 준비중')
    st.text('4월 준비중')
    st.text('5월 준비중')
    st.text('6월 준비중')
    st.text('7월 준비중')

    return

def Strategy_2023_01(pbr):

    col1, col2=st.columns(2)
    with col1:
        st.markdown('''
                ##### :orange[시장평가 기준]
                ###### :red[1. 코스피의 PBR이 1.2 이상이면 미친 고평가]
                ###### :blue[2. 코스피의 PBR이 1 이하이면 저평가]
                ###### :green[3. 코스피의 PBR이 0.9 이하이면 폭락장/하락장]
            ''')
    with col2:
        st.markdown('''
                ##### :orange[2023년 1월9일 현재 바닥을 확인후 반등중임]
                ###### :orange[기술적 지표(rsi(10): 침체구간(30이하), 볼린저밴드(40,2): 하단선 하향 돌파)]
                ###### :orange[주식시장의 저평가: 0.9이하 + 기술적 저점일때 적극적으로 매매]
                ###### :orange[위의 3가지 요건이 만족되면 몰빵한다.]
                ##### :violet[일반적 통계를 활용한 매매 방법]
                ###### :green[1월 진입 3,4월 매도(코스닥이 코스피보다 좋다, 개별주(중소형주)위주로 매매)]
                ###### :green[1월~3월 매수, 4월에 매도]
                ###### :green[장단기 금리차 역전이 해소 된 후 3~7개월내에 폭락장 나올 수 있음]
                ###### :green[5월~10월은 폭락장이 나올 수 있으므로 콥버스 매수하거나, 조심해야 된다]
                ###### :green[폭락장 나오면 매수 후 12월까지 보유하면 큰 수익이 가능할 것으로 생각된다]
            ''')

    st.markdown(f'최근 코스피 PBR은 :blue[{pbr}]로 매우 저평가 되어있다. :orange[이번 사이클의 상승 여력이 있는 종목이나] \
        :violet[지금 바닥에 있는 종목중 다음 사이클에 상승 예상 종목을 발굴하여 진입할 준비가 필요하다].')

    st.text('')
    st.markdown('**2023년 1월 현재 시장은 하향추세로 다음 사항을 매일 한번 점검한다.**')
    st.markdown('**:blue[1. 코스피의 현재 PBR이 0.90이하인가?]**')
    st.markdown('**:red[2. 코스피 지수가 볼린저밴드(40,2)의 하한선을 하향 돌파 하였는가?]**')
    st.markdown('**:violet[3. 코스피 지수의 RSI(10)이 30 이하인가?]**')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown("Text can be :blue[azul], but also :orange[laranja]. And of course it can be \
    :red[red]. And :green[verde]. And look at this :violet[violeta]!")

    st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")

    st.markdown(
        'This will print <span style="color:blue;"> blue text </span>',
        unsafe_allow_html=True
        )    

    return