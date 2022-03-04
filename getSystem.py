import pandas as pd
import plotly.express as px
import DoQueries as dq

colors = {
    'background': '#1b2444',
    'text': '#CAD2C5',

}


def getFrequency():
    freq = dq.getFrequency()
    data = [
        {
            'x': freq['dtm'],
            'y': freq['value'],
            'name': 'value'
        }
    ]

    return data

def getInertia():
    inertia = dq.getInertia()
    data = [
        {
            'x':inertia['dtm'],
            'y':inertia['value'],
            'name': 'value'
        }
    ]

    return  data