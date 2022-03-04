import DoQueries as dq
import pandas as pd
import dash
import plotly.express as px
# from dash import dcc, html
from datetime import datetime, timedelta, date
import dash_core_components as dcc
import dash_html_components as html
colors = {
    'background': '#1b2444',
    'text': '#CAD2C5',
}

def getAncillary(chosen_date, ancillary_type):

    if chosen_date == 0:
        chosen_date= (date.today()-timedelta(days=1)).strftime("%m/%d/%Y")
        ancillary_type = 'OFFNS'

    asCurve = dq.AggASSupply(ancillary_type, chosen_date)

    graph = px.scatter(
        data_frame=asCurve,
        x='Quantity',
        y='Price',
        color='HourEnding',
        title='Bid Prices for Selected Hours',
        color_discrete_sequence=px.colors.qualitative.G10
    )
    graph.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    hours = asCurve['HourEnding'].unique()
    data = [{'name': i, 'x': asCurve[asCurve['HourEnding'] == i]['Quantity'],
             'y': asCurve[asCurve['HourEnding'] == i]['Price'], 'type': 'scatter', 'marker': {'symbol': 'circle'},
             'mode': 'markers' } for i in hours]

    # 74F531
    total = asCurve.groupby(['DeliveryDate', 'HourEnding', "AncillaryType"], as_index=False)[['Quantity']].max()
    total_plot = total[(total['AncillaryType'] == str(ancillary_type)) & (total['DeliveryDate'] == str(chosen_date))]
    aggOffer = px.scatter(
        data_frame=total,
        x='HourEnding',
        y='Quantity',
        title='Total Offer Through the Day',
        color_discrete_sequence = ['#FAED27'],

    )

    aggOffer.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        xaxis={'showgrid':False}

    )
    total_data = [{
        'x':total_plot['HourEnding'],
        'y':total_plot['Quantity'],
        'type': 'scatter', 'marker': {'color': '#FF0000','symbol': 'circle'},
        'mode': 'markers'
    }
    ]
    print(aggOffer)
    # total_data[0]['line'] = {'color': '#FAED27'}
    # aggOffer['data'][0]['marker']['color'] = '#F4FF00'
    return total_data, data