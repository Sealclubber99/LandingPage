import pandas as pd
import time
from datetime import datetime, date, timedelta
from datetime import datetime, timedelta, date
import numpy as np
import plotly.express as px
import requests
import dash_table
from io import StringIO, BytesIO
import DoQueries as dq
# from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html

colors = {
    'background': '#1b2444',
    'text': '#CAD2C5',

}

auth = ('dl_trading@broadreachpower.com', 'joshallen')

wind_dict = {
    'COASTAL': 10004189446,
    'NORTH': 10004189449,
    'PANHANDLE': 10004189445,
    'SOUTH': 10004189447,
    'WEST': 10004189450,
}
# solar zone dicitonary
solar_dict = {
    'SOLAR': 10000712973,
}
# load zone dictionary
load_dict = {
    'HOUSTON': 10000712972,
    'NORTH': 10000712969,
    'SOUTH': 10000712970,
    'WEST': 10000712971,
}
rows = ['Capacity available to increase Generation Resource Base Points in the next 5 minutes in SCED (HDL)',
        'ERCOT-wide Physical Responsive Capability (PRC)',
        'Real-Time On-Line reserve capacity',
        'Real-Time On-Line and Off-Line reserve capacity',
        'Reg-Up',
        'Deployed Reg-Up',
        'Reg-Down',
        'Deployed Reg-Down',
        ]

style_cell = {
    'backgroundColor': '#1b2444',
    'color': 'white',
    'textAlign': 'center',
    'font_size': '10px'
}
# table styles
style_table = {
    'margin': '10px',
    # 'height': '40vh',
    'backgroundColor': '#1b2444',
    # 'maxWidth':'100%',
    'maxWidth': '50%',
    'maxHeight': '40%'
}
style_header = {'backgroundColor': ' #161d33'}


def getASreport():
    # pulls the data
    df = pd.read_html('http://www.ercot.com/content/cdr/html/as_capacity_monitor.html', header=0)
    df = df[0]
    df.columns = ['Name', 'Value']
    df = df[(df['Name'].isin(rows))]
    return df


def getRTreport():
    # pulls the data
    df = pd.read_html('http://www.ercot.com/content/cdr/html/real_time_system_conditions.html', header=0)
    df = df[0]
    df.columns = ['Name', 'Value']
    return df


def createboxes(data):
    # children div for AS report
    # filled with cards
    children = []
    # dictionary for the cards that are used in the different tabs
    cardsDict = {}
    # for each row in the data
    for i in data:
        # if the row is not null
        if not pd.isnull(i['Name']):
            # make sure that the column names/values are the same
            if i['Name'] != i['Value']:
                # creates the card for the div
                temp = html.Div(
                    className='Card',
                    children=[
                        html.Div(
                            className='TitleDiv',
                            children=[html.P(className='CardTitle', children=[i['Name']])]
                        ),
                        html.Div(
                            className='ValueDiv',
                            children=[html.P(className='CardTitle', children=[i['Value']])]
                        ),

                    ])
                # adds the card to the list == card div
                children.append(temp)
                # adds the solar, load, and system demabds card to teh dicitonary
                # they are used in diffferent tabs, not just the main asreport tab
                if i['Name'] in ['Total Wind Output', 'Total PVGR Output', 'Actual System Demand']:
                    cardsDict[i['Name']] = temp
    # returns the card div as well as the dictionary for the other tabs
    return children, cardsDict


def testASData():
    asReport = getASreport()
    # get RT report data
    rtReport = getRTreport()
    # transforms both dataframes into dictionaries

    result = pd.concat([rtReport, asReport])
    result['Value'].replace('DC Tie Flows', np.nan, inplace=True)
    result['Value'].replace('Real-Time Data', np.nan, inplace=True)
    result['Name'].replace(
        'Capacity available to increase Generation Resource Base Points in the next 5 minutes in SCED (HDL)', 'HDL',
        inplace=True)
    result['Name'].replace('Total System Capacity (not including Ancillary Services)', 'Total System Capacity',
                           inplace=True)
    result['Name'].replace('Consecutive BAAL Clock-Minute Exceedances (min)', 'Consecutive BAAL Minute Exceedances',
                           inplace=True)
    result['Name'].replace('ERCOT-wide Physical Responsive Capability (PRC)', 'PRC', inplace=True)
    result['Name'].replace('Real-Time On-Line and Off-Line reserve capacity', 'RT on and off line reserve cap',
                           inplace=True)
    result['Value'].replace('', np.nan, inplace=True)
    result.dropna(subset=['Value'], inplace=True)
    print(result.shape)
    new_frame = result.iloc[:7, :]
    new_frame2 = result.iloc[7:14, :]
    new_frame3 = result.iloc[14:, :]
    print(new_frame)
    columns_1 = [{'name': str(i), "id": str(i)} for i in new_frame.columns]
    data_1 = new_frame.to_dict('records')

    columns_2 = [{'name': str(i), "id": str(i)} for i in new_frame2.columns]
    data_2 = new_frame2.to_dict('records')

    columns_3 = [{'name': str(i), "id": str(i)} for i in new_frame3.columns]
    data_3 = new_frame3.to_dict('records')

    asTable_1 = dash_table.DataTable(
        columns=columns_1,
        id='asTable_1',
        data=data_1,
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell
    )
    asTable_2 = dash_table.DataTable(
        columns=columns_2,
        id='asTable_2',
        data=data_2,
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell
    )
    asTable_3 = dash_table.DataTable(
        columns=columns_3,
        id='asTable_3',
        data=data_3,
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell
    )
    return [asTable_1, asTable_2, asTable_3]

    # asR = asReport.to_dict('records')
    # rtR = rtReport.to_dict('records')
    # # combines the dictionaries
    # test = asR + rtR


def getASData():
    # get AS report data
    asReport = getASreport()
    # get RT report data
    rtReport = getRTreport()
    # transforms both dataframes into dictionaries
    asR = asReport.to_dict('records')
    rtR = rtReport.to_dict('records')
    # combines the dictionaries
    test = asR + rtR

    children, cardsDict = createboxes(test)

    return children, cardsDict['Total Wind Output'], cardsDict['Total PVGR Output'], cardsDict[
        'Actual System Demand']


def wind_data(start_date, end_date):
    items_list = []
    for value in wind_dict.values():
        item = 'WIND_RTI:' + str(value)
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
    df = raw.iloc[:, :-5]
    # strip '(WIND_RTI)' from column names
    df = df.rename(columns=lambda x: str(x).replace('GR_', '').replace(' (WIND_RTI)', ''))
    # set index ot datetime
    df = df.set_index('DATETIME')
    # change to datetime format
    df.index = pd.to_datetime(df.index)
    return df


def solar_data(start_date, end_date):
    # create string to fulfill items parameter
    items_list = []
    for value in solar_dict.values():
        item = 'GENERATION_SOLAR_RT:' + str(value)
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
    df = raw.iloc[:, :-5]
    # strip '(GENERATION_SOLAR_RT)' from column names
    df = df.rename(columns=lambda x: str(x).replace(' (GENERATION_SOLAR_RT)', ''))
    # set index ot datetime
    df = df.set_index('DATETIME')
    # change to datetime format
    df.index = pd.to_datetime(df.index)

    return df


def load_data(start_date, end_date):
    # create string to fulfill items parameter
    items_list = []
    for value in load_dict.values():
        item = 'RTLOAD:' + str(value)
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
    df = raw.iloc[:, :-5]
    # strip '(GENERATION_SOLAR_RT)' from column names
    df = df.rename(columns=lambda x: str(x).replace(' (RTLOAD)', '').replace(' (ERCOT)', ''))
    # set index ot datetime
    df = df.set_index('DATETIME')
    # change to datetime format
    df.index = pd.to_datetime(df.index)

    return df


def getPRC():
    # get PRC data from databse
    prc = dq.getPRC()
    data = [{
        'x': prc['dtm'],
        'y': prc['value'],
        'line': {'color': '#3366CC', 'dash': 'solid'},
    }

    ]
    return data


def getHDL():
    # queires the HDL database
    hdl = dq.getHDL()
    # creates the HDL plot
    data = [{
        'x': hdl['dtm'],
        'y': hdl['value'],
        'line': {'color': '#3366CC', 'dash': 'solid'},
    }

    ]
    return data


def plot_actuals():
    # start and end dtaets
    start_date = (date.today() + timedelta(days=-7)).strftime('%Y-%m-%d')
    end_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    # get the wind data from wind_data method
    wind = wind_data(start_date, end_date)
    # line colors
    line_colors = ['#F81007', '#150CE9', '#FF6B42', '#FFBA38', '#028D05']
    # plot
    fig_wind = px.line(wind, x=wind.index, y=wind.columns, title='Wind Actuals',
                       color_discrete_sequence=line_colors)
    wind_data_array = [{'name': i, 'x': wind.index, 'y': wind[i]} for i in wind.columns]

    # get the solar data from solar_data method
    solar = solar_data(start_date, end_date)
    solar_data_array = [{'name': i, 'x': solar.index, 'y': solar[i]} for i in solar.columns]
    # solar_data_array = solar_data_array + ['line': {'color': '#F81007', 'dash': 'solid'}]
    solar_data_array[0]['line'] = {'color': '#F81007', 'dash': 'solid'}
    # create the solar figure

    # line colors
    line_colors = ['#F81007', '#150CE9', '#FF6B42', '#FFBA38', '#028D05']
    # plot

    # create the solar figure

    # get load data from load_data method
    load = load_data(start_date, end_date)
    load_data_array = [{'name': i, 'x': load.index, 'y': load[i]} for i in load.columns]
    # line colors

    return wind_data_array, solar_data_array, load_data_array

# def hdl_callback():
#