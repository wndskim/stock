import streamlit as st
import plotly.express as px

# Load data
# df = px.data.gapminder()

def Chart_001(df):
    # Create the Plotly figure
    fig = px.bar(x=df["날짜"], y=df["PBR"], color="continent",
                title="최근 20일 PBR",
                template="plotly_dark")

    # Render the figure in the Streamlit app
    st.plotly_chart(fig)

    return