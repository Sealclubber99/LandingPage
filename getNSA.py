import DoQueries as dq
import pandas as pd
import dash
import plotly.express as px
# from dash import html, dcc, dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_table

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
# colorscale for the NSA constaint table
colorscale = [
    '#ffe2e2',
    '#ffbebe',
    '#ff8787',
    '#ff5858',
    '#ff3f3f',
    '#ff1a1a',
    '#e00000'
]


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


def getNSAConstraints():
    NSA = dq.NSA_Constraints()
    over_90 = NSA[NSA['RTCAPercentViolation'] > 100]
    data = over_90.to_dict('records')
    columns = [{'name': str(i), "id": str(i)} for i in over_90.columns]

    types = NSA['MonitoredElementId'].unique()
    data_graph = [{'name': i, 'x': NSA[NSA['MonitoredElementId'] == i]['RTCAExecutionTime'],
                   'y': NSA[NSA['MonitoredElementId'] == i]['MWViolation'], 'type': 'scatter',
                   'marker': {'symbol': 'circle'}, 'mode': 'markers', } for i in types]
    table_style, legend = fillBackground(over_90, columns=['RTCAPercentViolation'])
    table = dash_table.DataTable(
        columns=columns,
        id='nsaTable',
        data=data,
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell,
        style_data_conditional=table_style
    )

    return data_graph, table
