# associated functions
import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime, date, timedelta
import dash
import pyodbc
from dash.dependencies import Input, Output
import AssetDashboard as ass
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash import dash_table as dsht
from dash.dependencies import Input, Output, State
import dash_table
import plotly.express as px
#background for everything should be #282c34
start_date = date.today() + timedelta(days=0)
end_date = start_date + timedelta(days=2)
import DoQueries as dq



#plot proxy day ptp graphs (distribution of return by da spread and HE)
def ptp_plots(source, sink, he, day):
    if day == 'ND':
        table = 'nd_proxy_prices'
    else:
        table = 'nd1_proxy_prices'

    #df = pull_proxy_prices([source, sink], 'dart').set_index('DATETIME')
    sql = ("""

        select {0}, {1}, {2}, {3}, HOURENDING, MARKETDAY
        from {4}

    """)
    print(type(source))
    print(type(day))
    print(type(sink))
    print(type(he))
    df = dq.proxy_days(sql.format(source+'_da', source+'_rt', sink+'_da', sink+'_rt', table))

    da_spread = df.iloc[:,2] - df.iloc[:,0]
    rt_spread = df.iloc[:,3] - df.iloc[:,1]

    path_return = (rt_spread - da_spread).round(2)

    spread_profile = pd.concat([da_spread, path_return, df['HOURENDING'], df['MARKETDAY']], axis=1)
    spread_profile.columns = ['DA Spread $', 'Return $', 'HE', 'Date']
    spread_profile['Timestamp'] = spread_profile['Date'] + ' ' + spread_profile['HE'].astype(str)

    if he == 0:
        fig_spread = px.scatter(spread_profile, x='DA Spread $', y='Return $', hover_name='Timestamp')
    else:
        fig_spread = px.scatter(spread_profile[spread_profile['HE']==he], x='DA Spread $', y='Return $', hover_name='Timestamp')

    fig_hour = px.scatter(spread_profile, x='HE', y='Return $', hover_name='Timestamp').update_traces(marker=dict(color='red'))

    return fig_spread, fig_hour



# callback
# @app.callback(
#     Output('daspread-return', 'figure'),
#     Output('hour-return', 'figure'),
#     [Input('source-choice', 'value'),
#      Input('sink-choice', 'value'),
#      Input('he-slider', 'value'),
#      Input('day-choice', 'value')])
# def plot_proxy_ptp_graphs(source, sink, he, day):
#     daspread_plot, hour_plot = ptp_plots(source, sink, he, day)
#     return daspread_plot, hour_plot
