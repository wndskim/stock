import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def Chart_002(data):
    
    # data_hi = data[data['등락률']>=0]
    # data_lo = data[data['등락률']<0]

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

    # # set up trace with extreme highs
    # fig.add_traces(go.Candlestick(x=data['년도'],
    #             open=data_hi['시가'], high=data_hi['고가'],
    #             low=data_hi['저가'], close=data_hi['종가']))


    # color_hi_fill = 'red'
    # color_hi_line = 'red'

    # color_lo_fill = 'blue'
    # color_lo_line = 'blue'

    # fig.data[1].increasing.fillcolor = color_hi_fill
    # fig.data[1].increasing.line.color = color_hi_line
    # fig.data[1].decreasing.fillcolor = 'rgba(0,0,0,0)'
    # fig.data[1].decreasing.line.color = 'rgba(0,0,0,0)'

    # fig.data[2].increasing.fillcolor = 'rgba(0,0,0,0)'
    # fig.data[2].increasing.line.color = 'rgba(0,0,0,0)'
    # fig.data[2].decreasing.fillcolor = color_lo_fill
    # fig.data[2].decreasing.line.color = color_lo_line

    fig.update_layout(title='년간 주가', xaxis_rangeslider_visible = False)

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