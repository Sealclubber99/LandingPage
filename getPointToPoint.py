import pandas as pd
import time
from datetime import datetime, date, timedelta

import numpy as np
import plotly.express as px
# from dash import html, dcc, dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import arrow
import requests
import itertools
import json
from io import StringIO, BytesIO

auth = ('dl_trading@broadreachpower.com', 'joshallen')
style_header = {'backgroundColor': ' #161d33'}
style_cell = {
    'backgroundColor': '#1b2444',
    'color': 'white',
    'textAlign': 'center'
}
# style_table = {
#     'width': '100%',
#     'backgroundColor': '#1b2444',
# }
# style_table_as = {
#     'width': '1000px',
#     'backgroundColor': '#1b2444',
# }

node_dict = {
    'ALVIN_RN': 10016433362,
    'BRPANGLE_RN': 10016437282,
    'BRPMAGNO_RN': 10016437280,
    'BRP_BRAZ_RN': 10016437281,
    'BRP_DIKN_RN': 10016437279,
    'BRP_LOOP_RN': 10016473683,
    'BRP_SWNY_RN': 10016473684,
    'BRHEIGHT_RN': 10016437277,
    'ODESW_RN': 10016433361,
    'HB_HUBAVG': 10000698382,
    'HB_HOUSTON': 10000697077,
    'HB_NORTH': 10000697078,
    'HB_SOUTH': 10000697079,
    'HB_PAN': 10015999590,
    'HB_WEST': 10000697080,
}


wind_dict = {
    'COASTAL': 10004189446,
    'NORTH': 10004189449,
    'PANHANDLE': 10004189445,
    'SOUTH': 10004189447,
    'WEST': 10004189450,
    }
#solar zone dicitonary
solar_dict = {
    'SOLAR': 10000712973,
}
#load zone dictionary
load_dict = {
    'HOUSTON': 10000712972,
    'NORTH': 10000712969,
    'SOUTH': 10000712970,
    'WEST': 10000712971,
}
neg_backgroundColor = list(reversed(px.colors.sequential.Reds))
pos_backgroundColor = px.colors.sequential.Greens
colorscale = neg_backgroundColor + pos_backgroundColor

def fill_background(df, n_bins=9):

    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]

    df_numeric_columns = df.iloc[:,1:25] #change back to 1:8 if reverting back to long form table
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()

    neg_ranges = [
        -((df_min * i) - df_min)
        for i in bounds
    ]
    pos_ranges = [
        (df_max * i)
        for i in bounds
    ]
    ranges = neg_ranges + pos_ranges
    ranges.remove(-0.0)

    styles = []
    legend = []

    #style for date column
    styles.append({
        'if': {'column_id': 'Date'},
        'color': 'black',
        'fontWeight': 'bold',
        'fontSize': 18,
        'textAlign': 'center'
    })

    for i in range(1, 19):
        #regular value scale
        min_bound = ranges[i - 1]
        max_bound = ranges[i]

        backgroundColor = colorscale[i-1]

        if i > 5 and i < 13:
            color = 'black'
        else:
            color = 'white'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                            '{{{column}}} >= {min_bound}' +
                            (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': str(column)
                },
                'backgroundColor': backgroundColor,
                'color': color
            })
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
            ])
        )

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))



def getPaths(paths):
    return [{'label': i, 'value': i} for i in paths.columns]
def onpk(df):
    hours = list(range(8,24))
    df = df[df.index.hour.isin(hours)]
    return df

#off-peak
def offpk(df):
    hours = list(range(0,8))
    df = df[df.index.hour.isin(hours)]
    return df

#evening peak
def pk(df):
    hours = list(range(14,19))
    df = df[df.index.hour.isin(hours)]
    return df

def price_data(asset_dictionary):
    #create string to fulfill items parameter
    start_date = (date.today() + timedelta(days=-7)).strftime('%Y-%m-%d')
    end_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    items_list = []
    for value in asset_dictionary.values():
        item = 'DALMP:' + str(value) + ',RTLMP:' + str(value)
        items_list.append(item)

    items = ','.join(items_list)

    #DST flag
    if time.localtime().tm_isdst == 1:
        tz = 'CPT'
    else:
        tz = 'CST'

    #define parameters
    parameters = {

        'agglevel': 'hour',
        'startdate': start_date,
        'enddate': end_date,
        'timezone': tz,
        'items': items,

    }
    #define query
    query = requests.get('https://services.yesenergy.com/PS/rest/timeseries/multiple.csv?',params = parameters, auth = auth)
    #pull and manipulate raw data
    raw = pd.read_csv(StringIO(query.text)).round(2)
    #delete unnecesary columns
    df = raw.iloc[:,:-3]

    return df
def wind_data(dictionary, start_date, end_date):
    #create string to fulfill items parameter
    items_list = []
    for value in dictionary.values():
        item = 'WIND_RTI:' + str(value)
        items_list.append(item)

    items = ','.join(items_list)

    #DST flag
    if time.localtime().tm_isdst == 1:
        tz = 'CPT'
    else:
        tz = 'CST'

    #define parameters
    parameters = {

        'agglevel': 'hour',
        'startdate': start_date,
        'enddate': end_date,
        'timezone': tz,
        'items': items,

    }

    #define query
    query = requests.get('https://services.yesenergy.com/PS/rest/timeseries/multiple.csv?',params = parameters, auth = auth)
    #pull and manipulate raw data
    raw = pd.read_csv(StringIO(query.text)).round(2)
    #delete unnecesary columns
    df = raw.iloc[:,:-5]
    #strip '(WIND_RTI)' from column names
    df = df.rename(columns = lambda x : str(x).replace('GR_','').replace(' (WIND_RTI)',''))
    #set index ot datetime
    df = df.set_index('DATETIME')
    #change to datetime format
    df.index = pd.to_datetime(df.index)

    return df

#pull solar actuals from yes api
def solar_data(dictionary, start_date, end_date):
    #create string to fulfill items parameter
    items_list = []
    for value in dictionary.values():
        item = 'GENERATION_SOLAR_RT:' + str(value)
        items_list.append(item)

    items = ','.join(items_list)

    #DST flag
    if time.localtime().tm_isdst == 1:
        tz = 'CPT'
    else:
        tz = 'CST'

    #define parameters
    parameters = {

        'agglevel': 'hour',
        'startdate': start_date,
        'enddate': end_date,
        'timezone': tz,
        'items': items,

    }

    #define query
    query = requests.get('https://services.yesenergy.com/PS/rest/timeseries/multiple.csv?',params = parameters, auth = auth)
    #pull and manipulate raw data
    raw = pd.read_csv(StringIO(query.text)).round(2)
    #delete unnecesary columns
    df = raw.iloc[:,:-5]
    #strip '(GENERATION_SOLAR_RT)' from column names
    df = df.rename(columns = lambda x : str(x).replace(' (GENERATION_SOLAR_RT)',''))
    #set index ot datetime
    df = df.set_index('DATETIME')
    #change to datetime format
    df.index = pd.to_datetime(df.index)

    return df
def load_data(dictionary, start_date, end_date):
    #create string to fulfill items parameter
    items_list = []
    for value in dictionary.values():
        item = 'RTLOAD:' + str(value)
        items_list.append(item)

    items = ','.join(items_list)

    #DST flag
    if time.localtime().tm_isdst == 1:
        tz = 'CPT'
    else:
        tz = 'CST'

    #define parameters
    parameters = {

        'agglevel': 'hour',
        'startdate': start_date,
        'enddate': end_date,
        'timezone': tz,
        'items': items,

    }

    #define query
    query = requests.get('https://services.yesenergy.com/PS/rest/timeseries/multiple.csv?',params = parameters, auth = auth)
    #pull and manipulate raw data
    raw = pd.read_csv(StringIO(query.text)).round(2)
    #delete unnecesary columns
    df = raw.iloc[:,:-5]
    #strip '(GENERATION_SOLAR_RT)' from column names
    df = df.rename(columns = lambda x : str(x).replace(' (RTLOAD)','').replace(' (ERCOT)',''))
    #set index ot datetime
    df = df.set_index('DATETIME')
    #change to datetime format
    df.index = pd.to_datetime(df.index)

    return df

def plot_actuals():
    start_date = (date.today() + timedelta(days=-7)).strftime('%Y-%m-%d')
    end_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    wind = wind_data(wind_dict, start_date, end_date)
    # line colors
    line_colors = ['#F81007', '#150CE9', '#FF6B42', '#FFBA38', '#028D05']
    # plot
    fig_wind = px.line(wind, x=wind.index, y=wind.columns, title='Wind Actuals',
                  color_discrete_sequence=line_colors)

    fig_wind.update_layout(
        xaxis=dict(nticks=10)  # , tickformat='%m/%d')
    )

    solar = solar_data(solar_dict, start_date, end_date)
    #line colors
    line_colors = ['#F81007', '#150CE9', '#FF6B42', '#FFBA38', '#028D05']
    #plot
    solar_fig = px.line(solar, x=solar.index, y=solar.columns, title='Solar Actuals',
                    color_discrete_sequence=line_colors)

    solar_fig.update_layout(
        xaxis=dict(nticks=10)#, tickformat='%m/%d')
    )


    load = load_data(load_dict, start_date, end_date)
    #line colors
    line_colors = px.colors.qualitative.G10
    #plot
    fig_load = px.line(load, x=load.index, y=load.columns, title='Load Actuals',
                    color_discrete_sequence=line_colors)

    fig_load.update_layout(
        xaxis=dict(nticks=10)#, tickformat='%m/%d')
    )
    return fig_wind, solar_fig, fig_load

def getTables():
    print()
    data = price_data(node_dict).set_index('DATETIME')
    data.index.names = ['datetime']
    data.index = pd.to_datetime(data.index)
    data = data[data.index.date < date.today()]

    # da dataframe
    da_prices = data.loc[:, data.columns.str.contains('DALMP')]
    # strip of excess (either 'DALMP or 'RTLMP')
    da_prices = da_prices.rename(columns=lambda x: str(x)[:-8])
    # rt dataframe
    rt_prices = data.loc[:, data.columns.str.contains('RTLMP')]
    # strip of excess (either 'DALMP or 'RTLMP')
    rt_prices = rt_prices.rename(columns=lambda x: str(x)[:-8])

    # find all possible combinations
    nodes = list(node_dict.keys())
    combos = []
    for i in itertools.combinations(nodes, 2):
        combos.append(i)

    ## calculate spreads for cost of path table
    # create empty dataframe to merge onto
    path_price = pd.DataFrame(columns=['datetime'])
    # for loop through list of paths (tuples) and calculate profitability
    for path in combos:
        da_spread = da_prices.loc[:, da_prices.columns.isin(list(path))]
        da_spread['price'] = da_spread.iloc[:, 1] - da_spread.iloc[:, 0]
        da_spread = da_spread[['price']]
        da_spread.columns = [path]

        path_price = path_price.merge(da_spread, on='datetime', how='outer').round(2)

    path_price = path_price.set_index('datetime')
    # new columns w/o ''
    new_columns = []
    for i in path_price.columns:
        header = str(i).replace("'", "").replace("(", "").replace(")", "")
        new_columns.append(header)

    path_price.columns = new_columns

    ## calculate spreads and profitability
    # create empty dataframe to merge onto
    path_profitability = pd.DataFrame(columns=['datetime'])
    # for loop through list of paths (tuples) and calculate profitability
    for path in combos:
        da = da_prices.loc[:, da_prices.columns.isin(list(path))]
        da['da_spread'] = da.iloc[:, 1] - da.iloc[:, 0]

        rt = rt_prices.loc[:, rt_prices.columns.isin(list(path))]
        rt['rt_spread'] = rt.iloc[:, 1] - rt.iloc[:, 0]

        dart = (rt.iloc[:, 2] - da.iloc[:, 2]).reset_index().set_index('datetime')
        dart.columns = [path]

        path_profitability = path_profitability.merge(dart, on='datetime', how='outer').round(2)
        # path_profitability = pd.concat([path_profitability, dart], join='outer', axis=1).round(2)

    path_profitability = path_profitability.set_index('datetime')
    # new columns w/o ''
    new_columns = []
    for i in path_profitability.columns:
        header = str(i).replace("'", "").replace("(", "").replace(")", "")
        new_columns.append(header)

    path_profitability.columns = new_columns

    # filter by time period
    on_peak = onpk(path_profitability)
    on_peak = on_peak.groupby(on_peak.index.date).sum()
    on_peak = on_peak.rename(index=lambda x: str(x)[5:])

    off_peak = offpk(path_profitability)
    off_peak = off_peak.groupby(off_peak.index.date).sum()
    off_peak = off_peak.rename(index=lambda x: str(x)[5:])

    atc = path_profitability.groupby(path_profitability.index.date).sum()
    atc = atc.rename(index=lambda x: str(x)[5:])

    # top 10 paths over past 7 days averaged by period
    # on-peak
    top_on = on_peak.sum().reset_index()
    top_on.columns = ['Path', 'PnL']
    top_on = top_on.reindex(top_on.PnL.abs().sort_values(ascending=False).index)[:10].round(2)
    top_on.Path = top_on.Path.astype(str).str.replace("'", "")

    # off-peak
    top_off = off_peak.sum().reset_index()
    top_off.columns = ['Path', 'PnL']
    top_off = top_off.reindex(top_off.PnL.abs().sort_values(ascending=False).index)[:10].round(2)
    top_off.Path = top_off.Path.astype(str).str.replace("'", "")

    # atc
    top_atc = atc.sum().reset_index()
    top_atc.columns = ['Path', 'PnL']
    top_atc = top_atc.reindex(top_atc.PnL.abs().sort_values(ascending=False).index)[:10].round(2)
    top_atc.Path = top_atc.Path.astype(str).str.replace("'", "")
    return top_on, top_off, top_atc, getPaths(path_profitability), path_profitability, path_price

def hourly_cost(path, path_price):
    print('path price')
    print(path_price)

    df = path_price[path]
    df = pd.DataFrame(df)

    df.reset_index(inplace=True)

    df['datetime'] = pd.to_datetime(df['datetime'], infer_datetime_format=True)
    df['HE'] = df['datetime'].dt.hour + 1
    df['date'] = df['datetime'].dt.date


    hourly = pd.pivot_table(df, values=path, index='date', columns='HE', aggfunc=np.mean)
    hourly.reset_index(inplace=True)
    hourly.rename_axis(None, inplace=True, axis=1)
    return hourly


def hourly_ptp(path, path_profitability):
    print('path profitability')
    print(path_profitability)
    df = path_profitability[path]

    # print(df.columns)
    df=pd.DataFrame(df)
    df.reset_index(inplace=True)

    df['datetime'] = pd.to_datetime(df['datetime'], infer_datetime_format=True)
    df['HE'] = df['datetime'].dt.hour + 1
    df['date'] = df['datetime'].dt.date
    df.reset_index(inplace=True)


    hourly = pd.pivot_table(df, values=path, index='date', columns='HE', aggfunc=np.mean)
    hourly.reset_index(inplace=True)
    hourly.rename_axis(None, inplace=True, axis=1)

    return hourly

def update_ptp_table(path):
    if path is None:
        return dash.no_update

    df = hourly_ptp(path).round(2).reset_index()
    df.columns = df.columns.astype('str')

    # (styles, legend) = fill_background(df)

    return html.Div([
                html.P(
                    "Daily Path Profitability by Hour", className="control_label2",
                    style={'fontSize': 20, 'fontWeight': 'bold'}
                ),
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    style_header={
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textAlign': 'center'
                    },
                    style_cell={
                        'height': '3vh',
                        'textAlign': 'center'
                    },
                    # style_data_conditional=styles,
                ),
            ])


def ptp_table_daily(path, path_profitability):
    print('ptp_table_daily')
    df = hourly_ptp(path, path_profitability)
    (styles, legend) = fill_background(df)
    df.columns = df.columns.astype('str')

    # temptable = dash_table.DataTable(
    #     data=df.to_dict('records'),
    #     id='ptp_table',
    #     columns=[{'name': i, 'id': i} for i in df.columns],
    #     style_table=style_table,
    #     style_header=style_header,
    #     style_cell=style_cell
    # )
    columns_df = [{'name': str(i), "id": str(i)} for i in df.columns]
    data_df = df.to_dict('records')

    return html.Div([
        html.P(
            "Daily Path Profitability by Hour", className="control_label2",
            style={'fontSize': 20, 'fontWeight': 'bold'}
        ),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_cell={
                'height': '3vh',
                'textAlign': 'center'
            },
            style_data_conditional=styles,
        ),
    ])
def ptp_table_price(path, path_profitability):
    df = hourly_cost(path, path_profitability)
    df.columns = df.columns.astype('str')

    (styles, legend) = fill_background(df)

    return html.Div([
        html.P(
            "Daily Path Price by Hour", className="control_label2",
            style={'fontSize': 20, 'fontWeight': 'bold'}
        ),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_cell={
                'height': '3vh',
                'textAlign': 'center'
            },
            style_data_conditional=styles,
        ),
    ])
    return 'etst'
def getTablesUpdates(path):
    top_on, top_off, atc, paths, path_profitability, path_price = getTables()
    ptp_d = ptp_table_daily(path, path_profitability)
    ptp_p = ptp_table_price(path, path_price)

    return ptp_d, ptp_p
