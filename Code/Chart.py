import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def Chart_002(data,종목):

    # Create the chart
    fig = go.Figure(data=[go.Candlestick(x=data['년도'],
                        open=data["시가"],
                        high=data["고가"],
                        low=data["저가"],
                        close=data["종가"],
                        increasing_line_color='blue',
                        increasing_fillcolor='blue',
                        decreasing_line_color='red',
                        decreasing_fillcolor='red'
                    )])

    fig.update_layout(title=종목+' 년간 차트', xaxis_rangeslider_visible = False)

    # Add the chart to the app
    st.plotly_chart(fig)

    return


def Chart_001(df):
    # Create the Plotly figure
    fig = px.bar(x=df["날짜"],
                 y=df["PBR"],
                 title="최근 20일 PBR",
                #  color="continent",
                #  template="plotly_dark"
                 )
    fig.update_layout(
        xaxis_title="<b>날짜<b>",
        yaxis_title="<b>PBR<b>",
        width=1000,
        height=300,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=4
            ),
        # plot_bgcolor='rgba(0,0,0,0)',
        # yaxis=(dict(showgrid=False)),
        # paper_bgcolor='cornsilk'
    )
    # Render the figure in the Streamlit app
    st.plotly_chart(fig)

    return