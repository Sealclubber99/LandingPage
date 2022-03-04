import pandas as pd
import dash
import plotly.express as px
from datetime import datetime, timedelta, date
import time
import requests
import time
from pandas import json_normalize
import DoQueries as dq
import arrow
import plotly.graph_objs as go

colors = {
    'background': '#F7F7F7',
    'text': '#000000',
}




def getRegDate(date):
    datereg = dq.getRegForecast(date)
    datereg.drop_duplicates(subset=['datetime'], keep='last', inplace=True)
    traces = [
        {
            'x': datereg['datetime'],
            'y': datereg['Exhaustion_RD'],
            'name': 'Reg Down',
            'type': 'line'

        },
        {
            'x': datereg['datetime'],
            'y': datereg['Exhaustion_RU'],
            'name': 'Reg Up',
            'type': 'line'

        },
    ]
    date_fig = {'data': traces,
                'layout': {'title': {'text': 'Reg by Date'}, 'paper_bgcolor': colors['background'],
                           'plot_bgcolor': colors['background'],
                           'font': {'color': colors['text']}}}
    return date_fig

def getReg():
    reg = dq.getregDeployment()

    regUp = reg[(reg['field_id'] == 30) | (reg['field_id'] == 32)]

    regDown = reg[(reg['field_id'] == 31) | (reg['field_id'] == 33)]

    regDown['value'] = regDown['value'].transform(lambda x: x * -1)



    traces = [
        {
            'x': regDown[regDown['field_id'] == 33]['dtm'],
            'y': regDown[regDown['field_id'] == 33]['value'],
            'name': 'Reg Down Procurement',
            'type': 'line'

        },
        {
            'x': regUp[regUp['field_id'] == 30]['dtm'],
            'y': regUp[regUp['field_id'] == 30]['value'],
            'name': 'Reg Up Deployment',
            'type': 'line'

        },
        {
            'x': regDown[regDown['field_id'] == 31]['dtm'],
            'y': regDown[regDown['field_id'] == 31]['value'],
            'name': 'Reg Down Deployment',
            'type': 'line'

        },


        {
            'x': regUp[regUp['field_id'] == 32]['dtm'],
            'y': regUp[regUp['field_id'] == 32]['value'],
            'name': 'Reg Up Procurement',
            'type': 'line'

        },

    ]
    #
    # trans_fig = {'data': traces,
    #             'layout': {'title': {'text': 'Reg'}, 'paper_bgcolor': colors['background'],
    #                        'plot_bgcolor': colors['background'],
    #                        'font': {'color': colors['text']}}}
    #

    # return downPlot,upPlot,trans_fig
    return [traces]
def dstCheck():
    utc = arrow.utcnow()
    local = utc.to('US/Central')
    local_string = str(local)
    if local_string[-4] == '5':
        print('It is DST')
        return ('DST')
    else:
        print('It is not DST')
        return ('notDST')

def getBox():

    DST = dstCheck()
    data = dq.AS_Status(date.today(), DST)
    data['HE'] = pd.to_datetime(data['hb']).dt.hour + 1

    up_mean = data.groupby(['HE'])[['Reg Up Exhaustion']].mean().reset_index()
    up_fig = go.Figure()
    up_fig.add_trace(go.Box(
        x=data['HE'],
        y=data['Reg Down Exhaustion'],
        marker_color='red'
        # color_discrete_sequence=['blue'],
    ))

    up_fig.add_trace(
        go.Scatter(
            x=up_mean['HE'],
            y=up_mean['Reg Up Exhaustion'],
            mode='lines+markers',
            opacity=0.7,
            marker={
                'size': 7,
                'line': {'width': 0.5}
            },
            line={
                'color': '#6b0052'
            },
            name='Mean RUE'
        ),
    )
    up_fig.update_layout(title='Reg Up',
                           xaxis_title='HE',
                           yaxis_title='Reg Up Exhaustion',
                           paper_bgcolor=colors['background'],
                           plot_bgcolor=colors['background'],
                           font_color=colors['text']

                           )


    down_mean = data.groupby(['HE'])[['Reg Down Exhaustion']].mean().reset_index()
    down_fig  = go.Figure()
    down_fig.add_trace(go.Box(
        x=data['HE'],
        y=data['Reg Down Exhaustion'],
        marker_color='#ADD8E6'
        # color_discrete_sequence=['blue'],
    ))

    down_fig.add_trace(
        go.Scatter(
            x=down_mean['HE'],
            y=down_mean['Reg Down Exhaustion'],
            mode='lines+markers',
            opacity=0.7,
            marker={
                'size': 7,
                'line': {'width': 0.5}
            },
            line={
                'color': '#0e6900'
                # 'color':'#ADD8E6'
            },
            name='Mean RDE'
        ),
    )
    down_fig.update_layout(title='Reg Down',
                      xaxis_title='HE',
                      yaxis_title='Reg Down Exhaustion',
                      paper_bgcolor=colors['background'],
                      plot_bgcolor=colors['background'],
                      font_color=colors['text']

                      )
    # testFrame = data.groupby(['HE'])['Reg Down Exhaustion'].mean()
    # print(testFrame)
    return up_fig, down_fig