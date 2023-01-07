import streamlit as st

def Strategy_2023_01():

    st.markdown('**2023년 1월 현재 시장은 하향추세로 다음 사항을 매일 한번 점검한다.**')
    st.markdown('**:blue[1. 코스피의 현재 PBR이 0.90이하인가?]** \n \
                 **:red[2. 코스피 지수가 볼린저밴드(40,2)의 하한선을 하향 돌파 하였는가?]** \n \
                 **:violet[3. 코스피 지수의 RSI(10)이 30 이하인가?]** \n \
                ')


    st.markdown("Text can be :blue[azul], but also :orange[laranja]. And of course it can be \
    :red[red]. And :green[verde]. And look at this :violet[violeta]!")

    st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")

    st.markdown(
        'This will print <span style="color:blue;"> blue text </span>',
        unsafe_allow_html=True
        )    

    return