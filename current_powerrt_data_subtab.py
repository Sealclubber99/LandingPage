import pandas as pd
import numpy as np
import datetime as dt
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt
from io import BytesIO
import zipfile, io, os, glob, pytz, pyodbc, time, requests
from pytz import timezone
from urllib.request import urlopen
from zipfile import ZipFile
from bs4 import BeautifulSoup
import json
import sqlalchemy, urllib
from sqlalchemy import create_engine
import plotly.express as px

# variables
#genscaper api key
key = '33549db6c25e47bf9ba1b95446e557f4'

# functions
#function to pull 7day data from PowerRT API
def RT_pull_historical(key: str, region: str='ERCOT'):

    ## emf only data for past 7 days
    sleep_time = 10

    #determine lookback period start of day in UTC
    x = dt.datetime.now().hour# + 6
    start_date = (datetime.utcnow()-timedelta(hours=x)).isoformat('T')[:-4]+'Z'
    end_date = (datetime.utcnow()).isoformat('T')[:-4]+'Z'

    url = 'https://api.genscape.com/power/na/v1/generation-transmission/7day'
    params = {
            'balancingAuthority':region,
            'startDate':start_date,
            'endDate':end_date
    }

    headers = {'Gen-Api-Key': key} #input API Key here

    limit = 5000
    offset = 0
    data = []

    while(1):

        params = { **params,
          'limit': limit,
          'offset': offset
         }

        r = requests.get(url,params=params,headers=headers)

        if r.status_code == 429:
            #print('429: Too many requests. Pausing for 10 seconds')
            time.sleep(sleep_time)

        elif r.status_code == 200:
            resp_data = r.json()['data']
            #print(f"API returned {len(resp_data)} rows")
            data.extend(resp_data)
            offset += limit

            if len(resp_data) < limit:
                #print('Finished getting data')
                gen_output = pd.DataFrame(data).set_index('entityId')
                break

        else:
            # API returned an error other than 429, raise exception.
            r.raise_for_status()

    #Pull generator data in order to map output to name by entity ID
    meta_url = 'https://api.genscape.com/power/na/v1/entities/generation'
    data = {
        'limit': '5000',
        'offset': '0',
        'balancingAuthority':region
        }
    headers = {
        'Gen-Api-Key': key,
        'Accept': 'application/json'
        }

    r = requests.get(meta_url,params=data,headers=headers)
    gen_map = pd.DataFrame(r.json()['data']).set_index('entityId')

    #Match up the generator names with megawatt values using EntityIDs
    merged = gen_output.merge(gen_map,left_index=True,right_index=True).reset_index()

    #adjust timestamp to match power RT
    merged['Timestamp'] = pd.to_datetime(merged['effectiveDate'], infer_datetime_format=True) - timedelta(hours=6)

    return merged

#function to pull from PowerRT API
def RT_pull_current(key: str, region: str='ERCOT'):

    ## emf only data for past 7 days
    sleep_time = 10

    #determine lookback period start of day in UTC
    x = dt.datetime.now().hour# + 6
    start_date = (datetime.utcnow()-timedelta(hours=x)).isoformat('T')[:-4]+'Z'
    end_date = (datetime.utcnow()).isoformat('T')[:-4]+'Z'

    url = 'https://api.genscape.com/power/na/v1/generation-transmission/current'
    params = {
            'balancingAuthority':region,
            'startDate':start_date,
            'endDate':end_date
    }

    headers = {'Gen-Api-Key': key} #input API Key here

    limit = 5000
    offset = 0
    data = []

    while(1):

        params = { **params,
          'limit': limit,
          'offset': offset
         }

        r = requests.get(url,params=params,headers=headers)

        if r.status_code == 429:
            #print('429: Too many requests. Pausing for 10 seconds')
            time.sleep(sleep_time)

        elif r.status_code == 200:
            resp_data = r.json()['data']
            #print(f"API returned {len(resp_data)} rows")
            data.extend(resp_data)
            offset += limit

            if len(resp_data) < limit:
                #print('Finished getting data')
                gen_output = pd.DataFrame(data).set_index('entityId')
                break

        else:
            # API returned an error other than 429, raise exception.
            r.raise_for_status()

    #Pull generator data in order to map output to name by entity ID
    meta_url = 'https://api.genscape.com/power/na/v1/entities/generation'
    data = {
        'limit': '5000',
        'offset': '0',
        'balancingAuthority':region
        }
    headers = {
        'Gen-Api-Key': key,
        'Accept': 'application/json'
        }

    r = requests.get(meta_url,params=data,headers=headers)
    gen_map = pd.DataFrame(r.json()['data']).set_index('entityId')

    #Match up the generator names with megawatt values using EntityIDs
    merged = gen_output.merge(gen_map,left_index=True,right_index=True).reset_index()

    #adjust timestamp to match power RT
    merged['Timestamp'] = pd.to_datetime(merged['effectiveDate'], infer_datetime_format=True) - timedelta(hours=6)

    return merged

#function to create plots
def power_rt_plots():
    #pull today's RT monitored gen data
    df = RT_pull_historical(key)

    #create emf coal, gas, wind, and ir dataframes
    emf_coal = df[(df.confidenceLevel == 4)&(df.generationType == 'Coal')]
    emf_coal = emf_coal[['Timestamp', 'name', 'value']].sort_values(['Timestamp', 'name'])

    emf_gas = df[(df.confidenceLevel == 4)&(df.generationType == 'Gas')]
    emf_gas = emf_gas[['Timestamp', 'name', 'value']].sort_values(['Timestamp', 'name'])

    emf_wind = df[(df.confidenceLevel == 4)&(df.generationType == 'Wind')]
    emf_wind = emf_wind[['Timestamp', 'name', 'value']].sort_values(['Timestamp', 'name'])

    ir = df[df.confidenceLevel != 4]
    ir = ir[['Timestamp', 'name', 'value']].sort_values(['Timestamp', 'name'])

    #create total gen by fuel type stacked are chart
    total = df.set_index('Timestamp')
    total = total.groupby(['name', 'generationType']).resample('30min').mean().round(2).reset_index()
    total = pd.DataFrame(total.groupby(['Timestamp', 'generationType'])['value'].sum()).reset_index()

    #current supply stack mix
    current_mix = RT_pull_current(key)
    current_mix = pd.DataFrame(current_mix.groupby('generationType')['value'].sum()).reset_index()
    current_mix_fig = px.bar(current_mix, x='generationType', y='value', color='generationType')

    #create plot objects
    emf_coal_fig = px.line(emf_coal, x='Timestamp', y='value', color='name').update_layout(title_text='EMF Monitored Coal', title_x=0.5)
    emf_gas_fig = px.line(emf_gas, x='Timestamp', y='value', color='name').update_layout(title_text='EMF Monitored Gas', title_x=0.5)
    emf_wind_fig = px.line(emf_wind, x='Timestamp', y='value', color='name').update_layout(title_text='EMF Monitored Wind', title_x=0.5)
    ir_fig = px.line(ir, x='Timestamp', y='value', color='name').update_layout(title_text='IR Monitored Gen', title_x=0.5)
    total_fig = px.area(total, x='Timestamp', y='value', color='generationType').update_layout(title_text='Total Gen by Fuel Type', title_x=0.5)

    return emf_coal_fig, emf_gas_fig, emf_wind_fig, ir_fig, total_fig, current_mix_fig


# callback
#just need a calback with an update button as the input
