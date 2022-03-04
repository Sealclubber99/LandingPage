import pandas as pd
import time
from datetime import datetime, date, timedelta
import plotly.graph_objs as go
import numpy as np
import plotly.express as px
# from dash import dcc, html
# from dash import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import arrow
import requests
import itertools
import json
from io import StringIO, BytesIO

colors = {
    'background': '#F7F7F7',
    'text': '#000000',
}

# layout = {
#     # 'margin': '100px',
#     'margin':'25px',
#     'maxWidth':'40%',
#     'backgroundColor': '#1b2444',
#
# }
asset_dict = {
    'ALVIN_RN': 10016433362,
    'BRPANGLE_RN': 10016437282,
    'BATCAVE_RN': 10016670894,#
    'BRP_BRAZ_RN': 10016437281,
    'BRP_DIKN_RN': 10016437279,
    'BRHEIGHT_RN': 10016437277,#
    'BRP_LOOP_RN': 10016473683,
    'BRP_LOP1_RN': 10016761589,
    'BRPMAGNO_RN': 10016437280,#
    'NF_BRP_RN': 10016498292,
    'ODESW_RN': 10016433361,
    'BRP_PBL1_RN': 10016483004,#
    'BRP_PBL2_RN': 10016483001,
    'BRP_RN_UNIT1': 10016473685,
    'BRP_SWNY_RN': 10016473684,#
    'BRP_ZPT1_RN': 10016483003,
    'BRP_ZPT2_RN': 10016483009,
}



hub_dict = {
    'HB_HUBAVG': 10000698382,
    'HB_HOUSTON': 10000697077,
    'HB_NORTH': 10000697078,
    'HB_SOUTH': 10000697079,
    'HB_PAN': 10015999590,
    'HB_WEST': 10000697080,
}
auth = ('dl_trading@broadreachpower.com', 'joshallen')


def price_data(asset_dictionary):
    # create string to fulfill items parameter
    start_date = (date.today() + timedelta(days=-7)).strftime('%Y-%m-%d')
    end_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    items_list = []
    for value in asset_dictionary.values():
        item = 'DALMP:' + str(value) + ',RTLMP:' + str(value)
        items_list.append(item)

    items = ','.join(items_list)

    # DST flag
    if time.localtime().tm_isdst == 1:
        tz = 'CPT'
    else:
        tz = 'CST'

    # define parameters
    parameters = {

        'agglevel': 'hour',
        'startdate': start_date,
        'enddate': end_date,
        'timezone': tz,
        'items': items,

    }
    # define query
    query = requests.get('https://services.yesenergy.com/PS/rest/timeseries/multiple.csv?', params=parameters,
                         auth=auth)
    # pull and manipulate raw data
    raw = pd.read_csv(StringIO(query.text)).round(2)
    # delete unnecesary columns
    df = raw.iloc[:, :-3]

    return df


def getDates():
    today = date.today() - timedelta(days=1)
    test = pd.date_range(start='03/30/2021', end=today)
    dates = []
    for d in test:
        temp = {'label': d.strftime("%m/%d/%Y"), 'value': d.strftime("%m/%d/%Y")}
        dates.append(temp)
    return dates


def plot_hub_curves(price_data, date, market):
    prices = price_data
    # filter data by date, set HE to index, select asset specific RT and DA columns
    df = prices[prices['MARKETDAY'] == date].drop(['MARKETDAY', 'DATETIME'], axis=1).set_index('HOURENDING')
    # radio button dictionary to filter columns
    market_dict = {
        'DA': 'DALMP',
        'RT': 'RTLMP',
    }
    market_choice = market_dict.get(market)
    # filter columns (DA or RT)
    df = df.loc[:, df.columns.str.contains(market_choice)]
    # strip of excess (either 'DALMP or 'RTLMP')
    df = df.rename(columns=lambda x: str(x)[:-8])
    # line colors
    # hub_colors = ['#F2F5FF', '#F25F5C', '#FFE066', '#247BA0', '#30F2F2', '#70C1B3']
    # plot
    # fig = px.line(df, x=df.index, y=df.columns, color_discrete_sequence=hub_colors)
    # fig.update_layout(
    #     plot_bgcolor=colors['background'],
    #     paper_bgcolor=colors['background'],
    #     font_color=colors['text']
    # )
    data = [{'name': i, 'x': df.index, 'y': df[i]} for i in df.columns]
    return data


def plot_price_curves(price_data, date, market):
    prices = price_data
    # filter data by date, set HE to index, select asset specific RT and DA columns
    df = prices[prices['MARKETDAY'] == date].drop(['MARKETDAY', 'DATETIME'], axis=1).set_index('HOURENDING')
    # radio button dictionary to filter columns
    market_dict = {
        'DA': 'DALMP',
        'RT': 'RTLMP',
    }
    market_choice = market_dict.get(market)
    # filter columns (DA or RT)
    df = df.loc[:, df.columns.str.contains(market_choice)]
    # strip of excess (either 'DALMP or 'RTLMP')
    df = df.rename(columns=lambda x: str(x)[:-8])

    data = [{'name': i, 'x': df.index, 'y': df[i]} for i in df.columns]
    return data


def getDatesAssets():
    tomorrow = date.today() + timedelta(days=1)
    datelist = pd.date_range(tomorrow + timedelta(days=-8), periods=9).tolist()
    # datelist = [x.strftime('%m/%d/%Y') for x in reversed(datelist)]
    dates = []
    for d in datelist:
        temp = {'label': d.strftime("%m/%d/%Y"), 'value': d.strftime("%m/%d/%Y")}
        dates.append(temp)
    return dates


def getAssets(date, market):
    asset_prices = price_data(asset_dict)
    hub_prices = price_data(hub_dict)
    asset_fig = plot_price_curves(asset_prices, date, market)
    hub_fig = plot_hub_curves(hub_prices, date, market)

    return asset_fig, hub_fig


def getAssetGraphs(market, date):
    prices = price_data(asset_dict)
    df = prices[prices['MARKETDAY'] == date].drop('MARKETDAY', axis=1).set_index('HOURENDING')
    graphs = []
    for name in asset_dict:
        temp = df.loc[:, df.columns.str.contains(name)]

        # rename columns
        temp.columns = ['da', 'rt']
        # create da, rt, and da/rt series
        da = temp.da.reset_index(drop=True)
        rt = temp.rt.reset_index(drop=True)
        dart = da - rt

        da_rt_color = []
        da_rt_line = []
        for i in range(0, len(dart)):
            if dart[i] > 0:
                da_rt_color.append('rgb(57, 194, 8)')
                da_rt_line.append('rgb(57, 194, 8)')
            else:
                da_rt_color.append('rgb(207, 13, 6)')
                da_rt_line.append('rgb(161, 6, 0)')

        fig = go.Figure()
        fig.layout.xaxis.color = '#000000'
        fig.add_trace(
            go.Scatter(
                x=temp.index,
                y=rt,
                mode='lines+markers',
                opacity=0.7,
                marker={
                    'size': 7,
                    'line': {'width': 0.5}
                },
                line={
                    'color': '#0074D9'
                },
                name='RT'
            ),
        )
        fig.add_trace(
            go.Scatter(
                x=temp.index,
                y=da,
                mode='lines+markers',
                opacity=0.7,
                marker={
                    'size': 7,
                    'line': {'width': 0.5}
                },
                line={
                    'color': '#FFA500'
                },
                name='DA'
            ),
        )
        fig.add_trace(
            go.Bar(
                x=temp.index,
                y=dart,
                opacity=0.7,
                marker=dict(color=da_rt_color),

                name='DA/RT'
            ),
        )

        fig.update_layout(title=name,
                          xaxis_title='HE',
                          yaxis_title='$/MWHr',
                          paper_bgcolor=colors['background'],
                          plot_bgcolor=colors['background'],
                          font_color=colors['text'],

                          )

        temp_fig = dcc.Graph(figure=fig,  className='Asset_graph', style={'width': '95%', 'height':'35vh'})
        fig_div = html.Div(className="col-6 d-flex justify-content-center", children=[temp_fig])
        graphs.append(fig_div)
    container =[]
    for i, k in zip(graphs[0::2], graphs[1::2]):
        temp = html.Div(className="row d-flex justify-content-around mb-2", children=[i,k])
        container.append(temp)
    last = html.Div(className="row d-flex justify-content-center ", children=[graphs[-1]])
    container.append(last)
    return container
    # return graphs