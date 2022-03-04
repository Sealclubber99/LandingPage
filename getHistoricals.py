

import DoQueries as dq
import pandas as pd
import dash
import plotly.express as px
# from dash import dcc, html

import dash_core_components as dcc
import dash_html_components as html
colors = {
    'background': '#F7F7F7',
    'text': '#000000',
}

layout = {
    # 'margin': '100px',
    'backgroundColor': '#1b2444',

}
def getDart():
    his = dq.getHistorical()
    his.sort_values(by=['datetime'], inplace=True)
    fig = px.line(
        data_frame=his,
        x='datetime',
        y='dart',
        color='node',
        title='Historicals',
        color_discrete_sequence=px.colors.qualitative.G10
    )

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    nodes_his = his['node'].unique()
    data =[{'name': i, 'x': his[his['node'] == i]['datetime'],
             'y': his[his['node'] == i]['dart'] }for i in nodes_his]
    print(fig)
    nodes = []

    for name in his['node'].unique():
        temp = his[his['node'] == name]
        traces = [
            {
                'x': temp['datetime'],
                'y': temp['daprice'],
                'name': 'day ahead',
                'type': 'line'

            },
            {
                'x': temp['datetime'],
                'y': temp['rtprice'],

                'name': 'realtime',
                'type': 'line'

            }
        ]
        temp_fig = {'data': traces,
                    'layout': {'title': {'text': name}, 'paper_bgcolor': colors['background'],
                               'plot_bgcolor': colors['background'],
                               'font': {'color': colors['text']}}}
        temp = html.Div(className="col-6 d-flex justify-content-center", children=[dcc.Graph(figure=temp_fig, style={'width': '95%', 'height':'35vh'})])
        nodes.append(temp)
    container = []
    for i, k in zip(nodes[0::2], nodes[1::2]):
        temp = html.Div(className="row d-flex justify-content-around mb-2", children=[i, k])
        container.append(temp)
    last = html.Div(className="row d-flex justify-content-center", children=[nodes[-1]])
    container.append(last)
    return data, container