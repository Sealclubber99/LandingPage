import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime, timedelta
from yesapi.functions import *
import plotly.express as px
import pyodbc
import DoQueries as dq
# functions
#SQL Query Function


#pull proxy data
def plot_proxy_hr(day):

    if day == 'ND':
        table = 'nd_proxy_prices'
    else:
        table = 'nd1_proxy_prices'

    #sql string
    sql = 'select * from {}'.format(table)

    #query data
    df = dq.proxy_hours(sql)

    #pop off gas, he, and date
    df_back = pd.concat([df.pop(x) for x in df.iloc[:,-3:]], axis=1)
    df_front = df.loc[:, df.columns.str.contains('HB_HUBAVG')]

    #concatenate
    df = pd.concat([df_front, df_back], axis=1)
    df.columns = ['DA', 'RT', 'HH', 'HE', 'Date']

    #calculate heat rates
    df['DA'] = (df['DA']/df['HH']).round(2)
    df['RT'] = (df['RT']/df['HH']).round(2)

    #create boxplot df to plot later
    boxplot_df = df[['DA', 'RT', 'HE']]
    boxplot_df = pd.melt(boxplot_df, id_vars='HE', value_vars=['DA', 'RT'], var_name='Market', value_name='Heat Rate')

    #create a plotly box plot
    fig = px.box(boxplot_df, x="HE", y="Heat Rate", color="Market").update_traces(boxmean=True)

    return fig

