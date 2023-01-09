import streamlit as st

def Define_매매기술():

    # 차트영웅 22가지 기술에 대한 원리
    # 1. 큰 흐름(년봉/월봉/주봉)에서 추가 상승이 나올 수 있는 패턴 발견 후
    # 2. 월봉/주봉에서 기준에 맞아야 하고
    # 3. 그다음 일봉에서 매매 타이밍(눌림목)이 나올 때까지 기다린다.
    #   - 기다리는 동안 해당 종목이 올라갈 수 있는 이유(기업, 재료, 차트)에 대한 분석을 진행 한다.
    # 4. 그 이후에 분봉상에서 매매 타점을 잡아 매수 진행 한다.

    st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")
    st.markdown('**:blue[전고점 돌파매매]**')
    st.markdown('''
            ####**:blue[전고점 돌파매매]**
            ''')




    pass

    return



def Strategy_2023_01(pbr):

    st.markdown(f'최근 코스피 PBR은 :blue[{pbr}]로 매우 저평가 되어있다. :orange[이번 사이클의 상승 여력이 있는 종목이나] \
        :violet[지금 바닥에 있는 종목중 다음 사이클에 상승 예상 종목을 발굴하여 진입할 준비가 필요하다].')

    st.text('')
    st.markdown('**2023년 1월 현재 시장은 하향추세로 다음 사항을 매일 한번 점검한다.**')
    st.text('')

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