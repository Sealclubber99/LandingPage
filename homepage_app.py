import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
import json, gzip
from bs4 import BeautifulSoup
from io import StringIO, BytesIO
import pandas as pd
import numpy as np
import datetime as dt
import time
from datetime import timedelta, datetime
import itertools
import pyodbc
import pickle
import getASForecast as gasf
import AssetDashboard as ass
import getHistoricals as ghis
import getAncillaryBid as ganc
import DoQueries as dq
import current_powerrt_data_subtab as curr
from yesapi.functions import *
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
import getNetLoad as gnet
import getNSA as gnsa
import getCIT as gcit
import getPointToPoint as ptp
from dash import dash_table as dsht
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import getActuals as actuals
import getSystem as gsys
import proxy_days_subtab as prox
import proxy_hr_tab as pheat
#import layouts
from layouts import rt_sys_data_layout, fundamentals_layout, as_layout, congestion_layout, assets_layout, power_bi_layout
import getRegulationDeploy as greg
# style sheets
external_stylesheets=[dbc.themes.LUMEN]

# create dash object
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# the style arguments for the sidebar. We use position:fixed and a fixed width
sidebar_style = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "border": "2px black solid",
    "background-color": "#f7f7f7",
}

# the style for 'BRP Trading'
brp_style = {
    "font-weight": "bold",
    "color": "black",
}

# the style for each nav link item
nav_link_style = {
    "font-size": "1.5rem",
    #"font-weight": "bold",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
content_style = {
    "margin-left": "16rem",
}

# html layout
sidebar = html.Div(
    [
        dcc.Interval(id='minute', interval=60000),
        # five minute update interval
        dcc.Interval(id='fiveMinutes', interval=300000),
        # hour long update interval
        dcc.Interval(id='hourDownload', interval=(300000 * 12)),
        # daily update interval (actually every 6 hours)
        dcc.Interval(id='dailyDownload', interval=(300000 * 72)),
        html.H2("BRP Trading", className="display-4", style=brp_style),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("RT Market & System Data", href="/", active="exact", style=nav_link_style),
                html.Hr(),
                dbc.NavLink("Fundamentals", href="/fundies", active="exact", style=nav_link_style),
                html.Hr(),
                dbc.NavLink("AS Alley", href="/as-alley", active="exact", style=nav_link_style),
                html.Hr(),
                dbc.NavLink("Congestion Corner", href="/congestion-corner", active="exact", style=nav_link_style),
                html.Hr(),
                dbc.NavLink("Asset Dashboard", href="/asset-dashboard", active="exact", style=nav_link_style),
                html.Hr(),
                dbc.NavLink("Power BI Links", href="/power-bi-links", active="exact", style=nav_link_style),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=sidebar_style,
)

content = html.Div(id="page-content", style=content_style)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

app.validation_layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return rt_sys_data_layout
    elif pathname == "/fundies":
        return fundamentals_layout
    elif pathname == "/as-alley":
        return as_layout
    elif pathname == "/congestion-corner":
        return congestion_layout
    elif pathname == "/asset-dashboard":
        return assets_layout
    elif pathname == "/power-bi-links":
        return power_bi_layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
#
# @app.callback(
#     Output('solarData', 'data'),
#     [Input('solarButton', 'n_clicks')],
#     prevent_initial_call=False
# )
# def updateSolar(minutes, clicks):
#     print("what is going on")
#     # solar = gnet.getSolarGraph()
#     # return solar
#     return ['test']
@app.callback(
    Output('solarData', 'data'),
    [Input('fiveMinutes', 'n_intervals'), Input('solarButton', 'n_clicks')],
    prevent_initial_call=False
)
def updateWind(minutes, clicks):
    print("finally working")
    solar = gnet.getSolarGraph()
    return solar

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='solar_graph'
    ),
    Output('solarForecast', 'figure'),
    Input('solarData', 'data'),
)

@app.callback(
    Output('windgraphData', 'data'),
    [Input('fiveMinutes', 'n_intervals'), Input('windButton', 'n_clicks')],
    prevent_initial_call=False
)
def updateWind(minutes, clicks):
    print()
    wind = gnet.getWindGraph()
    return wind

@app.callback(
    [Output('windrightData', 'data'), Output('windleftData', 'data')],
    [Input('region_right', 'value'), Input('region_left', 'value'), Input('windButton', 'n_clicks')],
    prevent_initial_call=False
)
def update_store_data(region_right, region_left, clicks):
    print('is in here')
    right, left = gnet.getWindRegion(region_right, region_left)
    return right, left


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='wind_graphs'
    ),
    Output('dynam_right', 'figure'),
    Input('windrightData', 'data'),
)
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='wind_graphs'
    ),
    Output('dynam_left', 'figure'),
    Input('windleftData', 'data'),
)

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='wind_graph'
    ),
    Output('windGraph', 'figure'),
    Input('windgraphData', 'data'),
)

@app.callback(
    [Output('netloadData', 'data'),
     Output('netloadtable', 'children'),
     Output('netchangetable', 'children'),
     Output('legend', 'children'),],
    [Input('hourDownload', 'n_intervals'), Input('netloadButton', 'n_clicks')],
    prevent_initial_call=False
)
def update_store_data(intervals, clicks):
    print("is calling netchange methods")
    netgraph, nettable, netchangetable, legend = gnet.runNetload()
    legend_div = html.Div(className="rounded border border-primary bg-light col-5 d-flex justify-content-center m-2", children=[legend])
    return netgraph, [nettable], [netchangetable], legend_div


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='netload_graph'
    ),
    Output('netloadForecast', 'figure'),
    Input('netloadData', 'data'),
)


@app.callback(
    Output('netchangeData', 'data'),
    [Input('hourDownload', 'n_intervals'), Input('netloadButton', 'n_clicks')],
    prevent_initial_call=False
)
def update_store_data(intervals, clicks):
    netchangegraph = gnet.getNetLoadChange()
    return netchangegraph


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='netchange_graph'
    ),
    Output('netchangegraph', 'figure'),
    Input('netchangeData', 'data'),
)
@app.callback(
    Output('sevenData', 'data'),
    [Input('hourDownload', 'n_intervals'), Input('netloadButton', 'n_clicks')],
    prevent_initial_call=False
)
def updateSeven(hours, clicks):
    data = gnet.getLoad7DayGraph()
    return data


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='seven_graph'
    ),
    Output('day7loadForecast', 'figure'),
    Input('sevenData', 'data'),
)

@app.callback(
    Output('outageData', 'data'),
    [Input('hourDownload', 'n_intervals'), Input('netloadButton', 'n_clicks')],
    prevent_initial_call=False
)
def update_outage(hours, clicks):
    outage = gnet.getOutageGraph()
    return outage


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='outage_graph'
    ),
    Output('outageForecast', 'figure'),
    Input('outageData', 'data'),
)

@app.callback(
    [Output('actData', 'data'),
     Output('rampData', 'data')
     ],
    [Input('hourDownload', 'n_intervals'), Input('netloadButton', 'n_clicks')],
    prevent_initial_call=False
)
def update_store_data(clicks, intervals):
    act, ramp = gnet.getActNet()
    return act, ramp


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='ramp_graph'
    ),
    Output('rampForecast', 'figure'),
    Input('rampData', 'data'),
)
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='actnet_graph'
    ),
    Output('actNetload', 'figure'),
    Input('actData', 'data'),
)

@app.callback(
    Output('HDLData', 'data'),
    [Input('hdlButton', 'n_clicks'),
     Input('fiveMinutes', 'n_intervals')],
    prevent_initial_call=False
)
def update_store_data(clicks, intervals):
    hdl = actuals.getHDL()
    return hdl

@app.callback(
    Output('PRCData', 'data'),
    [Input('hdlButton', 'n_clicks'),
     Input('fiveMinutes', 'n_intervals')],
    prevent_initial_call=False
)
def update_store_data(clicks, intervals):
    prc = actuals.getPRC()
    print("is in prc")
    return prc

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='HDL_graph'
    ),
    Output('HDLGraph', 'figure'),
    Input('HDLData', 'data'),
)
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='PRC_graph'
    ),
    Output('PRC', 'figure'),
    Input('PRCData', 'data'),
)

@app.callback(
    [Output('frequencyData', 'data'), Output('inertiaData', 'data')],
    [Input('fiveMinutes', 'n_intervals'), Input('freqbutton', 'n_clicks')],
    prevent_initial_call=False
)
def update_store_data(intervals, clicks):
    frequency = gsys.getFrequency()
    inertia = gsys.getInertia()
    return frequency, inertia


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='frequency_graph'
    ),
    Output('frequency', 'figure'),
    Input('frequencyData', 'data'),
)
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='inertia_graph'
    ),
    Output('inertia', 'figure'),
    Input('inertiaData', 'data'),
)

@app.callback(
    [
        Output('masterData', 'data'),
        Output('hubData', 'data'),

    ],
    [Input('market-choice', 'value'), Input('assetDate', 'value'), Input('AssetsButton', 'n_clicks')], prevent_initial_call=True
)
def updateAssets(market, date, clicks):
    asset, hub = ass.getAssets(date, market)
    return asset, hub

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='asset_graph'
    ),
    Output('master-price', 'figure'),
    Input('masterData', 'data'),
)
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='hub_graph'
    ),
    Output('hub-price', 'figure'),
    Input('hubData', 'data'),
)


@app.callback([
    Output('nsaData', 'data'),
    Output('NSATable', 'children')
],
    [
        Input('NSAButton', 'n_clicks')

    ],
    prevent_initial_call=True)
def update_store_info(clicks):
    graph, table = gnsa.getNSAConstraints()
    return graph, table


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='asset_graph'
    ),
    Output('nsaGraph', 'figure'),
    Input('nsaData', 'data'),
)

# @app.callback([Output('date', 'options')], Input('ancbidButton', 'n_clicks'))
# def updatedates(clicks):
#     dates = ass.getDates()
#     print(type(dates))
#     return [dates]

@app.callback(
    [
        Output('supplyData', 'data'),
        Output('totalOfferData', 'data')
    ],
    [Input('asType', 'value'), Input('date', 'value'),
     Input('ancbidButton', 'n_clicks')],
    prevent_initial_call=True
)
def update_store_data(type, date, clicks):
    print('in here')
    total, supply = ganc.getAncillary(date, type)
    # temp = fd.getTempLoad(date
    return supply, total


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='Bid_graph'
    ),
    Output('supplyChart', 'figure'),
    Input('supplyData', 'data'),
)
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='total_graph'
    ),
    Output('totalOffer', 'figure'),
    Input('totalOfferData', 'data'),
)
@app.callback(
    [Output('rug', 'figure'), Output('rdg', 'figure')],
    [Input('fiveMinutes', 'n_intervals'), Input('deployButton', 'n_clicks')],
    prevent_initial_call=True
)
def update_store_data(clicks, intervals):
    ru, rd = greg.getBox()
    return ru, rd

@app.callback(
    [Output('regTransData', 'data')],
    [Input('fiveMinutes', 'n_intervals'), Input('deployButton', 'n_clicks')],
    prevent_initial_call=False
)
def update_store_data(clicks, intervals):
    trans = greg.getReg()
    return trans


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='regtrans_graph'
    ),
    Output('regTransform', 'figure'),
    Input('regTransData', 'data'),
)


@app.callback(
    Output('asset_graphs_div', 'children'),
    [
        Input('AssetsButton', 'n_clicks'),
        Input('fiveMinutes', 'n_intervals'),
        Input('market-choice', 'value'),
        Input('assetDate', 'value')
    ]
)
def getAssetDiv(clicks, intervals, market, date):

    assets = ass.getAssetGraphs(market, date)
    return assets

@app.callback(
    [Output('TexasMap', 'src'), Output('LegendKey', 'src')],
    [Input('fiveMinutes', 'n_intervals'), Input('mapBtn', 'n_clicks')],
    prevent_initial_call=False
)
def updateMap(n_intervals, n_clicks):
    ERCOTmap = "http://www.ercot.com/content/cdr/contours/rtmLmpHg.png"
    ERCOTLegend = 'http://www.ercot.com/content/cdr/contours/rtmLmpLegendHg.png'

    return ERCOTmap, ERCOTLegend

@app.callback(
    [Output('dartData', 'data'), Output('nodeDiv', 'children')],
    [Input('historicalButton', 'n_clicks')],
    prevent_initial_call=True
)
def update_store_data(intervals):
    data, nodes = ghis.getDart()
    return data, nodes


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='dart_graph'
    ),
    Output('Dart', 'figure'),
    Input('dartData', 'data'),
)


@app.callback(
    [
        Output('fxData', 'data'),
        Output('asTable', 'children'),
        Output('uplanTable', 'children'),
        Output('uplanData', 'data')
    ],

    [
        Input('asForButton', 'n_clicks'),

    ], [State('dateRange', 'start_date'),
        State('dateRange', 'end_date')],
    prevent_initial_call=False
)
def update_store_data(n_clicks, start_date, end_date):
    if end_date >= start_date:
        dash.exceptions.PreventUpdate
    fx, asTable = gasf.getFX(end_date, start_date)
    uplan, data = gasf.getUplan()
    return fx, asTable, uplan, data

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='asGraph'
    ),
    Output('uplanGraph', 'figure'),
    Input('uplanData', 'data'),
)

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='fxGraph'
    ),
    Output('fxGraph', 'figure'),
    Input('fxData', 'data'),
)

@app.callback(
    [Output('contingency-dropdown', 'options')],
    [Input('constraint-dropdown', 'value')], prevent_initial_call=True)
def set_contingency_options(constraint):

    return dq.getContingencies(constraint)


@app.callback(
    [Output('CIT_asset', 'children'), Output('CIT_hub', 'children'), Output('shift_div', 'children')],
    [Input('contingency-dropdown', 'value'), Input('direction-dropdown', 'value')],
    State('constraint-dropdown', 'value'), prevent_initial_call=True)
def create_tables(contingency, direction, constraint):
    if constraint == None or contingency == None:
        dash.no_update
    shift_div = []
    if direction == None:
        asset_table, hub_table = gcit.getCIT(constraint, contingency)
    else:
        asset_table, hub_table = gcit.getCITDirection(constraint, contingency, direction)
        shift_div = gcit.update_shift_table(constraint, contingency, direction)
    return asset_table, hub_table, shift_div


@app.callback(
    Output('direction-dropdown', 'options'),
    Input('contingency-dropdown', 'value'),
    State('constraint-dropdown', 'value'),
    prevent_initial_call=True)
def set_direction_options(contingency, constraint):
    choices = dq.getDirections(contingency, constraint)
    if type(choices) == bool:
        return dash.no_update
    return choices

@app.callback(
    [

        Output('top_on', 'data'),
        Output('top_off', 'data'),
        Output('atc', 'data'),
        Output('path-choice', 'options')

    ],
    Input('ptpButton', 'n_clicks'),
    prevent_initial_call=False
)
def getptpTables(clicks):
    top_on, top_off, atc, paths, path_profitability, path_price = ptp.getTables()
    on_data = top_on.to_dict('records')
    off_data = top_off.to_dict('records')
    atc_data = atc.to_dict('records')
    print(path_profitability)
    return on_data, off_data, atc_data, paths

@app.callback(
    [Output('path_profitability', 'children')],
    [Input('path-choice', 'value'),
     ],
    prevent_initial_call=True
)
def getptpTable(path):
    print("getting in here")
    if path is None:
        return dash.no_update
    ptp_d, ptp_p = ptp.getTablesUpdates(path)
    tables_array = [[ptp_p, ptp_d]]
    return tables_array



@app.callback(
    [
        Output('wind_act_data', 'data'),
        Output('solar_act_data', 'data'),
        Output('load_act_data', 'data'),
    ],
    [
        Input('netloadButton', 'n_clicks'),
        Input('solarButton', 'n_clicks'),
        Input('windButton', 'n_clicks')
     ],

    prevent_initial_call=True
)
def getActuals(n_load, n_solar, n_wind):
    wind_act, solar_act, load_act = actuals.plot_actuals()
    return wind_act, solar_act, load_act


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='actuals_solar'
    ),
    Output('solar_act', 'figure'),
    Input('solar_act_data', 'data'),
)

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='actuals_wind'
    ),
    Output('wind_act', 'figure'),
    Input('wind_act_data', 'data'),
)

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='actuals_load'
    ),
    Output('load_act', 'figure'),
    Input('load_act_data', 'data'),
)

@app.callback(
    Output('daspread-return', 'figure'),
    Output('hour-return', 'figure'),
    [Input('source-choice', 'value'),
     Input('he-slider', 'value'),
     Input('day-choice', 'value')], State('sink-choice', 'value'), prevent_initial_call=True)
def plot_proxy_ptp_graphs(source, he, day,sink):
    daspread_plot, hour_plot = prox.ptp_plots(source, sink, he, day)
    return daspread_plot, hour_plot


@app.callback(
    [
        Output('emf-coal-fig', 'figure'),
        Output('emf-gas-fig', 'figure'),
        Output('emf-wind-fig', 'figure'),
        Output('ir-fig', 'figure'),
        Output('total-fig', 'figure'),
        Output('current-mix-fig', 'figure')

     ],
    [
        Input('powerButton','n_clicks'),
        Input('fiveMinutes', 'n_intervals')
    ]
)
def currentGen(clicks, intervals):

    emf_coal_fig, emf_gas_fig, emf_wind_fig, ir_fig, total_fig, current_mix_fig = curr.power_rt_plots()
    return emf_coal_fig, emf_gas_fig, emf_wind_fig, ir_fig, total_fig, current_mix_fig

@app.callback(Output('proxy-hr', 'figure'), Input('day-choice', 'value'))
def proxy_head(choice):
    return pheat.plot_proxy_hr(choice)

@app.callback(
    Output('loadTest', 'data'),
    [Input('netloadButton', 'n_clicks'),
     Input('hourDownload', 'n_intervals')],

)
def TestLoad(clicks, intervals):
    df = gnet.getload()
    types = df['type'].unique()
    data = [{'name': i, 'x': df[df['type'] == i]['datetime'], 'y': df[df['type'] == i]['value']} for i in types]
    return data


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='load_graph'
    ),
    Output('loadForecast', 'figure'),
    Input('loadTest', 'data'),
)

if __name__ == "__main__":
    app.run_server(port=8888, debug=True,)
