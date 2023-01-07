import streamlit as st
import plotly.express as px

# Load data
# df = px.data.gapminder()

def Chart_001(df):
    # Create the Plotly figure
    fig = px.bar(x=df["날짜"],
                 y=df["PBR"],
                 title="최근 20일 PBR",
                #  color="continent",
                #  template="plotly_dark"
                 )

    fig.update_layout(showlegend=False)
    fig.update_layout(barmode='group')
    
    # Render the figure in the Streamlit app
    st.plotly_chart(fig)

    return