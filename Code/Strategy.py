import streamlit as st

def 주식시장순환원리_나바로():
    st.markdown('''
            ##### :red[1. 강세장 초반]
            ###### :red[- 주도업종: 운송]
            ###### :red[- 최고업종:  철동, 해운]
            ##### :green[2. 강세장 초반~중반]
            ###### :green[- 주도업종: 기술]
            ###### :green[- 최고업종: 컴퓨터, 전자, 반도체]
            ##### :orange[3. 강세장 중반~후반]
            ###### :orange[- 주도업종: 자본재(설비투자)]
            ###### :orange[- 최고업종: 전기설비, 중장비트럭, 기계와공구, 제조, 오염관리]
            ##### :blue[4. 강세장 후반]
            ###### :blue[- 주도업종: 기간산업, 화학, 원자재]
            ###### :blue[- 최고업종: 알루미늄, 화학, 컨테이너, 금속, 제지/임산품, 철강]
            ##### :red[5. 강세장 후반~정점]
            ###### :red[- 주도업종: 에너지]
            ###### :red[- 최고업종: 석유, 천연가스, 석탄]

            ''')

    return

def 연봉돌파_설명():

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

def Define_매매기술_설명():

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

    선택=st.selectbox('큰 흐름상 돌파매매 설명보기',['연봉돌파','월봉돌파','주봉돌파'])
    if 선택=='연봉돌파': 연봉돌파_설명()
    else: pass

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