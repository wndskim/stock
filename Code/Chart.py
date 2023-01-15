import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def Chart_002(data,종목,freq):

    # if freq=='d': title=' 일봉 차트 / 20일 이격률: '; 이격률3=data['sam20'].iloc[-1].round(2)
    if freq=='d': title=' 일봉 차트'
    elif freq=='y': title=' 연봉 차트 / 3년 이격률: '; 이격률3=data['이격률3'].iloc[-1].round(2)
    else: title=' 월봉 차트 / 20개월 이격률: '; 이격률20=data['이격률20'].iloc[-1].round(2)

    # Create the chart
    if freq=='d':
        # Create the chart
        fig = go.Figure(data=[go.Candlestick(x=data['날짜'],
                            open=data["시가"],
                            high=data["고가"],
                            low=data["저가"],
                            close=data["종가"],
                            name='일봉',
                            increasing_line_color='red',
                            increasing_fillcolor='red',
                            decreasing_line_color='blue',
                            decreasing_fillcolor='blue'
                        ),
                            go.Scatter(
                            x=data['날짜'],
                            y=data['sma20'],
                            name='20일평균',
                            line_color="yellow"
                        )
                ])

        fig.update_layout(title=종목+title+str(이격률20),
                        xaxis_title='날짜',
                        yaxis_title='가격',
                        width=1000,
                        height=400,
                        xaxis_rangeslider_visible = False)

    elif freq=='y':
        fig = go.Figure(data=[go.Candlestick(x=data['년도'],
                            open=data["시가"],
                            high=data["고가"],
                            low=data["저가"],
                            close=data["종가"],
                            name='연봉',
                            increasing_line_color='red',
                            increasing_fillcolor='red',
                            decreasing_line_color='blue',
                            decreasing_fillcolor='blue'
                        ),
                            go.Scatter(
                            x=data['년도'],
                            y=data['sma3'],
                            name='3년평균',
                            line_color="yellow"
                        )
                ])

        fig.update_layout(title=종목+title+str(이격률3),
                        xaxis_title='년도',
                        yaxis_title='가격',
                        xaxis_rangeslider_visible = False)

    else:
        # Create the chart
        fig = go.Figure(data=[go.Candlestick(x=data['년월'],
                            open=data["시가"],
                            high=data["고가"],
                            low=data["저가"],
                            close=data["종가"],
                            name='월봉',
                            increasing_line_color='red',
                            increasing_fillcolor='red',
                            decreasing_line_color='blue',
                            decreasing_fillcolor='blue'
                        ),
                            go.Scatter(
                            x=data['년월'],
                            y=data['sma20'],
                            name='20개월평균',
                            line_color="yellow"
                        )
                ])

        fig.update_layout(title=종목+title+str(이격률20),
                        xaxis_title='년월',
                        yaxis_title='가격',
                        width=1000,
                        height=400,
                        xaxis_rangeslider_visible = False)




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