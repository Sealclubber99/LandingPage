import pandas as pd
import DoQueries as dq
import plotly.express as px
# from dash import dash_table
import numpy as np
from datetime import datetime, date, timedelta
import requests
import time
from pandas import json_normalize
# from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html
import dash_table
#colors dictionary
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
    'textAlign': 'center'
}
#table styles
style_table = {
    # 'width': '100%',
    'backgroundColor': '#1b2444',
}

def getFX(end_date, start_date):


    forecast = dq.fx(startDate=start_date, endDate=end_date)
    table = forecast.pivot_table(index='OperatingDate', columns='forecast', values='value', aggfunc='sum').reset_index()

    data = table.to_dict('records')
    columns = [{'name': str(i), "id": str(i)} for i in table.columns]

    as_table = dash_table.DataTable(
        columns=columns,
        id='asForecast',
        data=data,
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell
    )

    data_store = [{'name': i, 'x': table['OperatingDate'], 'y': table[i]} for i in table.columns[1:]]
    return data_store, as_table

def getUplan():
    try:
        df = dq.uplan_dbConnect(True)
    except:
        df = dq.uplan_dbConnect(False)
    data = df.to_dict('records')
    columns = [{'name': str(i), "id": str(i)} for i in df.columns]

    as_table = dash_table.DataTable(
        columns=columns,
        id='uplanForecast',
        data=data,
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell
    )
    data_store = [{'name': i, 'x': df['timestamp'], 'y': df[i]} for i in df.columns[1:]]

    return as_table, data_store