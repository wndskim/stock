import streamlit as st

def 종목명_티커_선택(종목명s, df):
    col1, col2, col3=st.columns([1,2,1])
    with col1:
        종목=st.selectbox('종목선택',종목명s)
        티커=df[df['종목']==종목]['티커'].values[0]
    with col2:
        st.markdown('''
            ###### :orange[꼭 확인해야 할 사항 4가지]
            ###### :orange[1:부채비율, 2:유보율, 3:유통주식수, 4:적자흑자유무]
            ''')
    return 티커, 종목