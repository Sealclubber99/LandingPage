import pandas as pd
import time
from datetime import datetime, date, timedelta
import requests
from pandas import json_normalize
import numpy as np
import plotly.express as px
# from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import arrow
import itertools
import plotly.graph_objs as go
import DoQueries as dq

# colors dictionary
# colors = {
#     'background': '#1b2444',
#     'text': '#CAD2C5',
# }
direct_path = r'C:\Users\sealc\PycharmProjects\LandingPage\Data\NetData'
# style for table headings
colors = {
    'background': '#F7F7F7',
    'text': '#000000',
}
#style for table headings
style_header = {'backgroundColor': ' #c2ebff'}
#style for tables cells
style_cell = {
    'backgroundColor': '#F7F7F7',
    'color': '#000000',
    'textAlign': 'center',
    'font-size': '.7vw',
}
#table styles
style_table = {
    'width': '100%',
    # 'maxWidth':'95%',
    'backgroundColor': '#1b2444',
    'display':'flex',
    'justify-content':'center',
    'margin':'0',
    'table-layout':'fixed'
}
# colorscale for tabel colors
colorscale = [
    '#ff2100',
    '#ff6800',
    '#ffb300',
    '#ffdd00',
    '#aebb4e',
    '#81db29',
    '#4eff00'
]


# converts date for HB column
def convertdate_1(df):
    df['HB'] = df['HourEnding'].str.split(':').str[0]
    df['HB'] = pd.to_numeric(df['HB']) - 1
    df['datetime'] = df['DeliveryDate'].astype(str) + ' ' + df['HB'].astype(str) + ':00'
    df['datetime'] = pd.to_datetime(df['datetime'])
    return (df)


# converts dates for HB column
def convertdate_2(df):
    df['HB'] = df['HOUR_ENDING'] - 1
    df['datetime'] = df['DELIVERY_DATE'].astype(str) + ' ' + df['HB'].astype(str) + ':00'
    df['datetime'] = pd.to_datetime(df['datetime'])
    return (df)


# fills the background for the table with color scales
def fillBackground(df, n_bins=7, columns='all'):
    # creates an array of bins for the bounds of colors ie min max
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    #
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    legend = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        # backgroundColor = colorlover.scales[str(n_bins+4)]['div']['RdGy'][2:-2][i - 1]
        backgroundColor = colorscale[i - 1]
        color = 'black'

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


# gets recent data for netload change
def RecentData(Report_ID, call_number):
    # renames variable to report id - idk why this is here casey lmao
    reportID = Report_ID
    # pulls the data from ercot site
    ercotQuery = pd.read_json("https://sa.ercot.com/misapp/servlets/IceDocListJsonWS?reportTypeId=" + str(reportID))
    # normalize queried json file
    ercotQuery = pd.json_normalize(ercotQuery['ListDocsByRptTypeRes'][0])
    ercotQuery['type'] = ercotQuery['Document.FriendlyName'].str.slice(-3)
    ercotQuery['PublishDate'] = pd.to_datetime(ercotQuery['Document.PublishDate'], format='%Y-%m-%dT%H:%M:%S')
    csvList = ercotQuery[ercotQuery['type'] == 'csv']
    csvList = csvList[['Document.DocID', 'Document.ConstructedName', 'PublishDate']]
    csvList['zipFile'] = "https://sa.ercot.com/misdownload/servlets/mirDownload?doclookupId=" + csvList[
        'Document.DocID']
    zipFiles = csvList['zipFile'].tolist()
    file = zipFiles[call_number]
    df = pd.read_csv(file, compression='zip')
    df['report_time'] = 'Hours Ago: ' + str(call_number)
    return (df)


def getwind():
    reportID = 14787
    ercotQuery = pd.read_json("https://sa.ercot.com/misapp/servlets/IceDocListJsonWS?reportTypeId=" + str(reportID))
    ercotQuery = pd.json_normalize(ercotQuery['ListDocsByRptTypeRes'][0])
    ercotQuery['type'] = ercotQuery['Document.FriendlyName'].str.slice(-3)
    ercotQuery['PublishDate'] = pd.to_datetime(ercotQuery['Document.PublishDate'], format='%Y-%m-%dT%H:%M:%S')
    csvList = ercotQuery[ercotQuery['type'] == 'csv']
    csvList = csvList[['Document.DocID', 'Document.ConstructedName', 'PublishDate']]
    csvList['zipFile'] = "https://sa.ercot.com/misdownload/servlets/mirDownload?doclookupId=" + csvList[
        'Document.DocID']

    # dest = 'C:\\Users\\CaseyKopp\\Documents\\Python_Scripts\\ERCOT Downloads'
    file = csvList['zipFile'][0]

    df = pd.read_csv(file, compression='zip')
    df['HB'] = df['HOUR_ENDING'] - 1
    df['datetime'] = df['DELIVERY_DATE'].astype(str) + ' ' + df['HB'].astype(str) + ':00'
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = pd.melt(df, id_vars=['datetime', 'DELIVERY_DATE'],
                 value_vars=['ACTUAL_SYSTEM_WIDE', 'COP_HSL_SYSTEM_WIDE', 'STWPF_SYSTEM_WIDE', 'WGRPP_SYSTEM_WIDE',
                             'ACTUAL_PANHANDLE', 'COP_HSL_PANHANDLE', 'STWPF_PANHANDLE', 'WGRPP_PANHANDLE',
                             'ACTUAL_COASTAL', 'COP_HSL_COASTAL', 'STWPF_COASTAL', 'WGRPP_COASTAL', 'ACTUAL_SOUTH',
                             'COP_HSL_SOUTH', 'STWPF_SOUTH', 'WGRPP_SOUTH', 'ACTUAL_WEST', 'COP_HSL_WEST', 'STWPF_WEST',
                             'WGRPP_WEST', 'ACTUAL_NORTH', 'COP_HSL_NORTH', 'STWPF_NORTH', 'WGRPP_NORTH'],
                 value_name='value', var_name='type')
    df['region'] = np.where(df['type'].str.slice(-4) == "WIDE", "ISO", "")
    df['region'] = np.where(df['type'].str.slice(-4) == "NDLE", "PANHANDLE", df['region'])
    df['region'] = np.where(df['type'].str.slice(-4) == "STAL", "COASTAL", df['region'])
    df['region'] = np.where(df['type'].str.slice(-4) == "OUTH", "SOUTH", df['region'])
    df['region'] = np.where(df['type'].str.slice(-4) == "WEST", "WEST", df['region'])
    df['region'] = np.where(df['type'].str.slice(-4) == "ORTH", "NORTH", df['region'])
    # directory = r'C:\Users\sealc\OneDrive\Desktop\NewTimings\venv\Scripts\test_wind'
    # df.to_csv(directory + '\\' + 'test_wind.csv')
    return df


def getLoadGraph():
    load = getload()
    demandPlot = px.line(
        data_frame=load,
        x='datetime',
        y='value',
        color='type',
        title='Load Total Forecast',
        color_discrete_sequence=px.colors.qualitative.G10
    )
    demandPlot.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return demandPlot


def getSolarGraph():
    solar = pd.read_csv(direct_path +  '\\' + 'solar.csv')
    types = solar['type'].unique()
    data = [{'name': i, 'x': solar[solar['type'] == i]['datetime'],
             'y': solar[solar['type'] == i]['value']} for i in types]
    return data


def getWindGraph():
    wind = pd.read_csv(direct_path +  '\\' + 'wind.csv')

    types = wind['type'].unique()
    data = [{'name': i, 'x': wind[wind['type'] == i]['datetime'],
             'y': wind[wind['type'] == i]['value']} for i in types]

    return data


def getWindRegion(region_right, region_left):
    wind = pd.read_csv(direct_path +  '\\' + 'wind.csv')

    wind_right = wind[(wind['region'] == region_right)]
    types = wind_right['type'].unique()
    data_right = [{'name': i, 'x': wind_right[wind_right['type'] == i]['datetime'],
                   'y': wind_right[wind_right['type'] == i]['value']} for i in types]

    wind_left = wind[(wind['region'] == region_left)]
    types = wind_left['type'].unique()
    data_left = [{'name': i, 'x': wind_left[wind_left['type'] == i]['datetime'],
                  'y': wind_left[wind_left['type'] == i]['value']} for i in types]

    return data_right, data_left
    # return dynam_right, dynam_left


def getload():
    reportID = 13499
    ercotQuery = pd.read_json("https://sa.ercot.com/misapp/servlets/IceDocListJsonWS?reportTypeId=" + str(reportID))
    ercotQuery = pd.json_normalize(ercotQuery['ListDocsByRptTypeRes'][0])
    ercotQuery['type'] = ercotQuery['Document.FriendlyName'].str.slice(-3)
    ercotQuery['PublishDate'] = pd.to_datetime(ercotQuery['Document.PublishDate'], format='%Y-%m-%dT%H:%M:%S')
    csvList = ercotQuery[ercotQuery['type'] == 'csv']
    csvList = csvList[['Document.DocID', 'Document.ConstructedName', 'PublishDate']]
    csvList['zipFile'] = "https://sa.ercot.com/misdownload/servlets/mirDownload?doclookupId=" + csvList[
        'Document.DocID']
    # dest = 'C:\\Users\\CaseyKopp\\Documents\\Python_Scripts\\ERCOT Downloads'
    file = csvList['zipFile'][0]
    df = pd.read_csv(file, compression='zip')

    df['HB'] = df['HourEnding'] - 1
    df['datetime'] = df['DeliveryDate'].astype(str) + ' ' + df['HB'].astype(str) + ':00'
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = pd.melt(df, id_vars=['datetime', 'DeliveryDate'],
                 value_vars=['CurrentDayForecast', 'DayAheadForecast', 'ActualLoad', 'DayAheadHSL', 'CurrentDayHSL'],
                 value_name='value', var_name='type')

    return df


def getsolar():
    reportID = 13483
    ercotQuery = pd.read_json("https://sa.ercot.com/misapp/servlets/IceDocListJsonWS?reportTypeId=" + str(reportID))
    ercotQuery = pd.json_normalize(ercotQuery['ListDocsByRptTypeRes'][0])
    ercotQuery['type'] = ercotQuery['Document.FriendlyName'].str.slice(-3)
    ercotQuery['PublishDate'] = pd.to_datetime(ercotQuery['Document.PublishDate'], format='%Y-%m-%dT%H:%M:%S')
    csvList = ercotQuery[ercotQuery['type'] == 'csv']
    csvList = csvList[['Document.DocID', 'Document.ConstructedName', 'PublishDate']]
    csvList['zipFile'] = "https://sa.ercot.com/misdownload/servlets/mirDownload?doclookupId=" + csvList[
        'Document.DocID']
    # dest = 'C:\\Users\\CaseyKopp\\Documents\\Python_Scripts\\ERCOT Downloads'
    file = csvList['zipFile'][0]
    df = pd.read_csv(file, compression='zip')
    df['HB'] = df['HOUR_ENDING'] - 1
    df['datetime'] = df['DELIVERY_DATE'].astype(str) + ' ' + df['HB'].astype(str) + ':00'
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = pd.melt(df, id_vars=['datetime', 'DELIVERY_DATE'],
                 value_vars=['ACTUAL_SYSTEM_WIDE', 'COP_HSL_SYSTEM_WIDE', 'STPPF_SYSTEM_WIDE', 'PVGRPP_SYSTEM_WIDE'],
                 value_name='value', var_name='type')
    return df


def getoutage():
    reportID = 13103

    ercotQuery = pd.read_json(r'https://sa.ercot.com/misapp/servlets/IceDocListJsonWS?reportTypeId=' + str(reportID))

    ercotQuery = pd.json_normalize(ercotQuery['ListDocsByRptTypeRes'][0])

    ercotQuery['type'] = ercotQuery['Document.FriendlyName'].str.slice(-3)

    ercotQuery['PublishDate'] = pd.to_datetime(ercotQuery['Document.PublishDate'], format='%Y-%m-%dT%H:%M:%S')

    csvList = ercotQuery[ercotQuery['type'] == 'csv']

    csvList = csvList[['Document.DocID', 'Document.ConstructedName', 'PublishDate']]

    csvList['zipFile'] = 'https://sa.ercot.com/misdownload/servlets/mirDownload?doclookupId=' + csvList[
        'Document.DocID']

    # dest = 'C:\\Users\\CaseyKopp\\Documents\\Python_Scripts\\ERCOT Downloads'

    file = csvList['zipFile'][0]

    df = pd.read_csv(file, compression='zip')

    df['HB'] = df['HourEnding'] - 1

    df['datetime'] = df['Date'].astype(str) + ' ' + df['HB'].astype(str) + ':00'

    df['datetime'] = pd.to_datetime(df['datetime'])

    df['TotalResourceMW'] = df['TotalResourceMWZoneSouth'] + df['TotalResourceMWZoneNorth'] + df[
        'TotalResourceMWZoneWest'] + df['TotalResourceMWZoneHouston']

    # do not need to melt the data frame since there is only really one column to be concerned about

    # df = pd.melt(df, id_vars = ['datetime','DELIVERY_DATE'], value_vars = ['ACTUAL_SYSTEM_WIDE','COP_HSL_SYSTEM_WIDE','STPPF_SYSTEM_WIDE','PVGRPP_SYSTEM_WIDE'], value_name = 'value', var_name='type')

    # df = df[['datetime','TotalResourceMW']]
    print('outage:')
    print(df)

    return df


def get7daydemand():
    reportID = 12311
    ercotQuery = pd.read_json("https://sa.ercot.com/misapp/servlets/IceDocListJsonWS?reportTypeId=" + str(reportID))
    ercotQuery = pd.json_normalize(ercotQuery['ListDocsByRptTypeRes'][0])
    ercotQuery['type'] = ercotQuery['Document.FriendlyName'].str.slice(-3)
    ercotQuery['PublishDate'] = pd.to_datetime(ercotQuery['Document.PublishDate'], format='%Y-%m-%dT%H:%M:%S')
    csvList = ercotQuery[ercotQuery['type'] == 'csv']
    csvList = csvList[['Document.DocID', 'Document.ConstructedName', 'PublishDate']]
    csvList['zipFile'] = "https://sa.ercot.com/misdownload/servlets/mirDownload?doclookupId=" + csvList[
        'Document.DocID']
    # dest = 'C:\\Users\\CaseyKopp\\Documents\\Python_Scripts\\ERCOT Downloads'
    file = csvList['zipFile'][0]
    df = pd.read_csv(file, compression='zip')

    df['HB'] = df['HourEnding'].str.split(':').str[0]
    df['HB'] = pd.to_numeric(df['HB']) - 1

    df['datetime'] = df['DeliveryDate'].astype(str) + ' ' + df['HB'].astype(str) + ':00'
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = pd.melt(df, id_vars=['datetime', 'DeliveryDate'],
                 value_vars=['North', 'South', 'West', 'Houston', 'SystemTotal'], value_name='value', var_name='type')
    return df


def getLoad7DayGraph():
    seven = pd.read_csv(direct_path + '\\'+ 'sevenDay.csv')

    types = seven['type'].unique()
    data = [{'name': i, 'x': seven[seven['type'] == i]['datetime'],
             'y': seven[seven['type'] == i]['value']} for i in types]

    return data


def CIQ_Generation(start, end):
    key = 'OMAJksxQNp6FEMt3CQxb41YLyIe5Mwoq9DRgdWvz'

    params = {
        'start_date': start,
        'end_date': end
    }

    headers = {'x-api-key': key}

    url = 'https://congestioniq-api.genscape.com/v1/ercot/generation/power-iq/async?'

    resp = requests.get(url, headers=headers, params=params)
    resp_url = resp.json()['url']

    time.sleep(4)

    r = requests.get(resp_url)
    json_data = r.json()['generation']

    df_raw = pd.DataFrame.from_dict(json_normalize(json_data), orient='columns')

    df_raw['dispatch_date'] = pd.to_datetime(df_raw.dispatch_date, format='%Y-%m-%d')

    df = df_raw.drop(['settlement_point_rdfid'], axis=1)

    columns = df.columns[5:30]

    df = df.melt(id_vars=['settlement_point', 'fuel_type', 'lsl', 'hsl', 'dispatch_date'], value_vars=columns,
                 value_name='value', var_name='HE')

    df['HE'] = df['HE'].str.extract('(\d+)')
    df['HB'] = df['HE'].astype(int) - 1
    df['datetime'] = df['dispatch_date'].astype(str) + ' ' + df['HB'].astype(str) + ':00'
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M')
    df['fuel_type'] = df['fuel_type'].apply(', '.join)

    # df.to_csv(download_path + '\\' + 'ciq_generation.csv')
    aggregatedStack = df.groupby(['fuel_type', 'datetime'], as_index=False).value.agg('sum')
    return aggregatedStack


def getActNet():
    act = dq.getactnetload()

    traces_act = [
        {
            'x': act['datetime'],
            'y': act['netload'],
            'name': 'netload',
            'type': 'line'

        },
        {
            'x': act['datetime'],
            'y': act['actnetload'],
            'name': 'actual',
            'type': 'line'

        }
    ]
    actFig = {'data': traces_act, 'layout': {'title': {'text': 'Actuals'}, 'paper_bgcolor': colors['background'],
                                             'plot_bgcolor': colors['background'],
                                             'font': {'color': colors['text']}}}

    traces_ramp = [

        {
            'x': act['datetime'],
            'y': act['ramprate'],
            'name': 'ramp rate',
            'type': 'line'

        },
        {
            'x': act['datetime'],
            'y': act['actramprate'],
            'name': 'actual ramp rate',
            'type': 'line'

        }

    ]

    rampPlot = {'data': traces_ramp, 'layout': {'title': {'text': 'Ramp Rates'}, 'paper_bgcolor': colors['background'],
                                                'plot_bgcolor': colors['background'],
                                                'font': {'color': colors['text']}}}

    return traces_act, traces_ramp


def getOutageGraph():
    outage = pd.read_csv(direct_path +'\\'+ 'outage.csv')
    data = [
        {
            'x': outage['datetime'],
            'y': outage['TotalResourceMW']
        }
    ]

    return data


def getDayChange(df):
    for col in df.columns[1:-1]:
        df[col] = df[col].shift(1) - df[col]

    df.drop(df.head(1).index, inplace=True)

    return df.round(2)


def getnetChangeTable(netload_table):
    changeFrame = getDayChange(netload_table)
    columns_change = [{'name': str(i), "id": str(i)} for i in changeFrame.columns]
    data_change = changeFrame.to_dict('records')

    changetable = dash_table.DataTable(
        columns=columns_change,
        id='netload_change',
        data=data_change,
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell
    )

    return changetable


def getNetloadTable(netload_table):
    columns_net = [{'name': str(i), "id": str(i)} for i in netload_table.columns]
    data_net = netload_table.to_dict('records')
    table_style, legend = fillBackground(netload_table, columns=[i for i in range(1, 25)])

    temptable = dash_table.DataTable(
        columns=columns_net,
        data=data_net,
        id='netload_table',
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell,
        style_data_conditional=table_style
    )
    return temptable, legend


def getNetLoadFM(wind, solar, outage, load7day):
    sysLoadForecast = load7day[load7day['type'] == 'SystemTotal']
    sysLoadForecast = pd.pivot_table(sysLoadForecast, values='value', index='datetime', columns='type', aggfunc=np.mean)

    sysWindForecast = wind[wind['type'] == 'STWPF_SYSTEM_WIDE']
    sysWindForecast = pd.pivot_table(sysWindForecast, values='value', index='datetime', columns='type', aggfunc=np.mean)

    sysSolarForecast = solar[solar['type'] == 'STPPF_SYSTEM_WIDE']
    sysSolarForecast = pd.pivot_table(sysSolarForecast, values='value', index='datetime', columns='type',
                                      aggfunc=np.mean)

    netload = pd.merge(sysLoadForecast, sysSolarForecast, how='inner', on='datetime')
    netload = pd.merge(netload, sysWindForecast, how='inner', on='datetime')
    netload['netload_forecast'] = round(
        netload['SystemTotal'] - netload['STPPF_SYSTEM_WIDE'] - netload['STWPF_SYSTEM_WIDE'], 1)
    netload.reset_index(inplace=True)
    netload['datetime'] = pd.to_datetime(netload['datetime'])
    netload['HE'] = netload['datetime'].dt.hour + 1
    netload['date'] = netload['datetime'].dt.date

    # this is for the data table display
    netload_table = pd.pivot_table(netload, values='netload_forecast', index='date', columns='HE', aggfunc=np.mean)
    netload_table.reset_index(inplace=True)

    # add the outages into the table
    outage['datetime'] = pd.to_datetime(outage['datetime'])
    netload = pd.merge(netload, outage, how='inner', on='datetime')
    # SARA Capacity comes from the ERCOT SARA report
    netload['SARA Capacity'] = 70821
    netload['Generation Shortage Level'] = 5000
    netload['Available Capacity'] = netload['SARA Capacity'] - netload['TotalResourceMW'] - netload['netload_forecast']
    netload['Outages + Net Load'] = netload['netload_forecast'] + netload['TotalResourceMW']

    netload.rename(columns={'SystemTotal': 'Total Load Forecast', 'netload_forecast': 'Net Load Forecast',
                            'SARA Capacity': 'SARA Capacity', 'TotalResourceMW': 'Total Generation Outages',
                            'Available Capacity': 'Available Capacity'}, inplace=True)

    netload = pd.melt(netload, id_vars=['datetime'],
                      value_vars=['Total Load Forecast', 'Net Load Forecast', 'SARA Capacity',
                                  'Total Generation Outages',
                                  'Available Capacity', 'Outages + Net Load'], value_name='value', var_name='type')
    return netload_table, netload


def runNetload():
    wind = pd.read_csv(direct_path +'\\'+ 'wind.csv')
    solar = pd.read_csv(direct_path + '\\'+'solar.csv')
    outage = pd.read_csv(direct_path + '\\'+'outage.csv')
    load7day = pd.read_csv(direct_path + '\\'+ 'sevenDay.csv')

    start_date = date.today() + timedelta(days=0)
    end_date = start_date + timedelta(days=2)

    netload_table, netload = getNetLoadFM(wind, solar, outage, load7day)
    # netloadPlot = px.line(
    #     data_frame=netload,
    #     x='datetime',
    #     y='value',
    #     color='type',
    #     title='Net Load Forecast',
    #     color_discrete_sequence=px.colors.qualitative.G10
    # )
    # netloadPlot.update_layout(
    #     plot_bgcolor=colors['background'],
    #     paper_bgcolor=colors['background'],
    #     font_color=colors['text']
    # )
    types = netload['type'].unique()
    data = [{'name': i, 'x': netload[netload['type'] == i]['datetime'], 'y': netload[netload['type'] == i]['value']} for
            i in types]
    table, legend = getNetloadTable(netload_table)
    changetable = getnetChangeTable(netload_table)
    # test_dict = {
    #     'netData': netloadPlot,
    #     'tableData': table,
    #     'changeData': changetable,
    #     'legend': legend
    # }

    return data, table, changetable, legend


def getNetLoad():
    wind = getwind()
    windGraph = getWindGraph(wind)

    solar = getsolar()
    solarGraph = getSolarGraph(solar)

    outage = getoutage()
    outageGraph = getOutageGraph(outage)

    load7day = get7daydemand()
    Load7DayGraph = getLoad7DayGraph(load7day)

    start_date = date.today() + timedelta(days=0)
    end_date = start_date + timedelta(days=2)
    # aggregatedStack = CIQ_Generation(start_date, end_date)

    netload_table, netload = getNetLoadFM(wind, solar, outage, load7day)
    netloadPlot = px.line(
        data_frame=netload,
        x='datetime',
        y='value',
        color='type',
        title='Net Load Forecast',
        color_discrete_sequence=px.colors.qualitative.G10
    )
    netloadPlot.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    table, legend = getNetloadTable(netload_table)
    changetable = getnetChangeTable(netload_table)
    test_dict = {
        'netData': netloadPlot,
        'tableData': table,
        'changeData': changetable,
        'legend': legend
    }

    return windGraph, solarGraph, outageGraph, Load7DayGraph, netloadPlot, table, changetable, legend


def getNetLoadChangeFM(previous_hours):
    #### ERCOT Load Forecast ####
    load = RecentData(12311, previous_hours)
    load = convertdate_1(load)
    load = load[['datetime', 'SystemTotal', 'report_time']]
    load = load.rename(columns={
        'SystemTotal': 'load'
    })
    #### ERCOT Wind Forecast ####

    wind = RecentData(14787, previous_hours)
    wind = convertdate_2(wind)
    wind = wind[['datetime', 'STWPF_SYSTEM_WIDE', 'report_time']]
    wind = wind.rename(columns={
        'STWPF_SYSTEM_WIDE': 'wind',
    })

    #### ERCOT Solar Forecast ####

    solar = RecentData(13483, previous_hours)
    solar = convertdate_2(solar)
    solar = solar[['datetime', 'STPPF_SYSTEM_WIDE', 'report_time']]
    solar = solar.rename(columns={'STPPF_SYSTEM_WIDE': 'solar'})
    df = pd.merge(load, wind, how='inner', on=['datetime', 'report_time'])
    df = pd.merge(df, solar, how='inner', on=['datetime', 'report_time'])
    df['net_load'] = df['load'] - df['wind'] - df['solar']
    return (df)


def getNetLoadChange():
    netload = pd.concat(getNetLoadChangeFM(x) for x in [0, 6, 24])

    # graph = px.line(
    #     data_frame=netload,
    #     x='datetime',
    #     y='net_load',
    #     color='report_time',
    #     color_discrete_sequence=px.colors.qualitative.G10
    # )
    # graph.update_layout(
    #     plot_bgcolor=colors['background'],
    #     paper_bgcolor=colors['background'],
    #     font_color=colors['text']
    # )
    times = netload['report_time'].unique()
    data = [{'name': i, 'x': netload[netload['report_time'] == i]['datetime'],
             'y': netload[netload['report_time'] == i]['net_load']} for
            i in times]

    return data

