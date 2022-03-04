# dictionaries
#asset dictionary - ADDED ASSETS
asset_dict = {
    'ALVIN_RN': 10016433362,
    'BRPANGLE_RN': 10016437282,
    'BATCAVE_RN': 10016670894,#
    'BRP_BRAZ_RN': 10016437281,
    'BRP_DIKN_RN': 10016437279,
    'BRHEIGHT_RN': 10016437277,#
    'BRP_LOOP_RN': 10016473683,
    'BRP_LOP1_RN': 10016761589,
    'BRPMAGNO_RN': 10016437280,#
    'NF_BRP_RN': 10016498292,
    'ODESW_RN': 10016433361,
    'BRP_PBL1_RN': 10016483004,#
    'BRP_PBL2_RN': 10016483001,
    'BRP_RN_UNIT1': 10016473685,
    'BRP_SWNY_RN': 10016473684,#
    'BRP_ZPT1_RN': 10016483003,
    'BRP_ZPT2_RN': 10016483009,
}

#hub dicitonary
hub_dict = {
    'HB_HUBAVG': 10000698382,
    'HB_HOUSTON': 10000697077,
    'HB_NORTH': 10000697078,
    'HB_SOUTH': 10000697079,
    'HB_PAN': 10015999590,
    'HB_WEST': 10000697080,
}

# functions
#master asset price plot
def plot_price_curves(price_data, date: str, market: str):
    prices = price_data
    #filter data by date, set HE to index, select asset specific RT and DA columns
    df = prices[prices['MARKETDAY'] == date].drop(['MARKETDAY', 'DATETIME'], axis=1).set_index('HOURENDING')
    #radio button dictionary to filter columns
    market_dict = {
        'DA': 'DALMP',
        'RT': 'RTLMP',
    }
    market_choice = market_dict.get(market)
    #filter columns (DA or RT)
    df = df.loc[:, df.columns.str.contains(market_choice)]
    #strip of excess (either 'DALMP or 'RTLMP')
    df = df.rename(columns = lambda x : str(x)[:-8])
    #plot
    fig = px.line(df, x=df.index, y=df.columns)

    return fig

#master hub price plot
def plot_hub_curves(price_data, date: str, market: str):
    prices = price_data
    #filter data by date, set HE to index, select asset specific RT and DA columns
    df = prices[prices['MARKETDAY'] == date].drop(['MARKETDAY', 'DATETIME'], axis=1).set_index('HOURENDING')
    #radio button dictionary to filter columns
    market_dict = {
        'DA': 'DALMP',
        'RT': 'RTLMP',
    }
    market_choice = market_dict.get(market)
    #filter columns (DA or RT)
    df = df.loc[:, df.columns.str.contains(market_choice)]
    #strip of excess (either 'DALMP or 'RTLMP')
    df = df.rename(columns = lambda x : str(x)[:-8])
    #line colors
    hub_colors = ['#F2F5FF', '#F25F5C', '#FFE066', '#247BA0', '#30F2F2', '#70C1B3']
    #plot
    fig = px.line(df, x=df.index, y=df.columns, color_discrete_sequence=hub_colors)

    return fig

#darts
def plot_dart_curves(price_data, asset: str, date: str):
    prices = price_data
    #filter data by date, set HE to index, select asset specific RT and DA columns
    df = prices[prices['MARKETDAY'] == date].drop('MARKETDAY', axis=1).set_index('HOURENDING')
    df = df.loc[:, df.columns.str.contains(asset)]

    #rename columns
    df.columns = ['da', 'rt']
    #create da, rt, and da/rt series
    da = df.da.reset_index(drop=True)
    rt = df.rt.reset_index(drop=True)
    dart = da - rt


    da_rt_color = []
    da_rt_line = []
    for i in range(0,len(dart)):
        if dart[i]>0 :
            da_rt_color.append('rgb(57, 194, 8)')
            da_rt_line.append('rgb(57, 194, 8)')
        else:
            da_rt_color.append('rgb(207, 13, 6)')
            da_rt_line.append('rgb(161, 6, 0)')
    fig={
        'data': [
            go.Scatter(
                x = df.index,
                y = rt,
                mode = 'lines+markers',
                opacity=0.7,
                marker={
                    'size': 7,
                    'line': {'width':0.5}
                },
                line={
                    'color': '#0074D9'
                },
                name = 'RT'
            ),
          go.Scatter(
                x= df.index,
                y= da,
                mode = 'lines+markers',
                opacity=0.7,
                marker={
                    'size': 7,
                    'line': {'width':0.5}
                },
                line={
                    'color': 'rgb(215, 219, 215)'
                },
                name = 'DA'
            ),
          go.Bar(
                x = df.index,
                y = dart,
                opacity=0.7,
                marker=dict(color=da_rt_color),

                name = 'DA/RT'
            ),
            ],
            'layout': go.Layout(
                title=dict(text='{}'.format(asset),
                    font=dict(
                        size=12
                    )),
                xaxis=dict(title='HE',
                    range=[1, 24],
                    nticks=20,
                    titlefont=dict(
                        size=12
                    ),
                    tickfont=dict(
                        size=10,
                    )),
                yaxis=dict(title='$/MWHr',
                    titlefont=dict(
                        size=12
                    ),
                    tickfont=dict(
                        size=10,
                    )),
                legend=dict(orientation='h',
                    yanchor="bottom",
                    y=1.02,
                    xanchor='center',
                    x=0.5,
                    font=dict(
                        size=7
                    )),
                )
    }

    return fig

# html layout - actually use this
dcc.Tab(label = 'Asset Dashboard', children = [
    html.Div(
        dcc.RadioItems(
            id='market-choice',
            options=list(map(lambda x:dict({'label':x,'value':x}),['DA', 'RT'])),
            value='DA',
            labelStyle={'fontSize': 16, 'padding': '1vh', 'marginBottom': '0'},
            inputStyle={'margin-right': '5px'}
        ),
    style=dict(textAlign='center')),
    dbc.Row(
        [
        dbc.Col(
            html.Div([
                dcc.Graph(
                    id='master-price',
                ),
            ]), width=12),
        ],
    justify='center'),
    dbc.Row(
        [
        dbc.Col(
            html.Div([
                dcc.Graph(
                    id='hub-price',
                ),
            ]), width=12),
        ],
    ),
    dbc.Container(fluid=True, children=[
        dbc.Row(
            [
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='alvin',
                    ),
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='angleton',
                    ),
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='batcave',
                    ),
                ]), width=4),
            ],
        ),
        dbc.Row(
            [
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='brazoria',
                    ),
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='dickinson',
                    ),
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='heights',
                    ),
                ]), width=4),
            ],
        ),
        dbc.Row(
            [
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='loop',
                    ),
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='lopeno',
                    ),
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='magnolia',
                    ),
                ]), width=4),
            ],
        ),
        dbc.Row(
            [
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='northfork',
                    ),
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='odessa',
                    ),
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='pueblo1',
                    ),
                ]), width=4),
            ],
        ),
        dbc.Row(
            [
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='pueblo2',
                    ),
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='ranchtown',
                    ),
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='sweeny',
                    ),
                ]), width=4),
            ],
        ),
        dbc.Row(
            [
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='zapata1',
                    ),
                ]), width=4),
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='zapata2',
                    ),
                ]), width=4),
            ],
        ),
    ], style={'width': '95%', 'height': '100%'}),
]),

# callbacks
#master asset and hub graphs
@app.callback(
    Output('master-price', 'figure'),
    Output('hub-price', 'figure'),
    [Input('date-choice', 'value'),
    Input('market-choice', 'value'),
    Input('btn', 'n_clicks')])
def update_graph(date, market, n_clicks):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'btn' in changed_id:
        #asset price data
        updated_asset_prices = price_data(asset_dict)
        asset_fig = plot_price_curves(updated_asset_prices, date, market)
        asset_fig.update_layout(asset_layout)
        #hub price data
        updated_hub_prices = price_data(hub_dict)
        hub_fig = plot_hub_curves(updated_hub_prices, date, market)
        hub_fig.update_layout(hub_layout)
        return asset_fig, hub_fig

    elif date == datelist[1] and market == 'RT':
        #asset price data
        updated_asset_prices = price_data(asset_dict)
        asset_fig = plot_price_curves(updated_asset_prices, date, market)
        asset_fig.update_layout(asset_layout)
        #hub price data
        updated_hub_prices = price_data(hub_dict)
        hub_fig = plot_hub_curves(updated_hub_prices, date, market)
        hub_fig.update_layout(hub_layout)
        return asset_fig, hub_fig

    else:
        #asset price data
        asset_fig = plot_price_curves(asset_prices, date, market)
        asset_fig.update_layout(asset_layout)
        #hub price data
        hub_fig = plot_hub_curves(hub_prices, date, market)
        hub_fig.update_layout(hub_layout)
        return asset_fig, hub_fig

#asset dart plots
@app.callback(
    Output('alvin', 'figure'),
    Output('angleton', 'figure'),
    Output('batcave', 'figure'),
    Output('brazoria', 'figure'),
    Output('dickinson', 'figure'),
    Output('heights', 'figure'),
    Output('loop', 'figure'),
    Output('lopeno', 'figure'),
    Output('magnolia', 'figure'),
    Output('northfork', 'figure'),
    Output('odessa', 'figure'),
    Output('pueblo1', 'figure'),
    Output('pueblo2', 'figure'),
    Output('ranchtown', 'figure'),
    Output('sweeny', 'figure'),
    Output('zapata1', 'figure'),
    Output('zapata2', 'figure'),
    [Input('date-choice', 'value'),
    Input('market-choice', 'value'),
    Input('btn', 'n_clicks')])
def update_graph(date, market, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'btn' in changed_id:
        updated_prices = price_data(asset_dict)
        #create each graph
        alvin = plot_dart_curves(updated_prices, asset='ALVIN_RN', date=date)
        angleton = plot_dart_curves(updated_prices, asset='BRPANGLE_RN', date=date)
        batcave = plot_dart_curves(updated_prices, asset='BATCAVE_RN', date=date)
        brazoria = plot_dart_curves(updated_prices, asset='BRP_BRAZ_RN', date=date)
        dickinson = plot_dart_curves(updated_prices, asset='BRP_DIKN_RN', date=date)
        heights = plot_dart_curves(updated_prices, asset='BRHEIGHT_RN', date=date)
        loop = plot_dart_curves(updated_prices, asset='BRP_LOOP_RN', date=date)
        lopeno = plot_dart_curves(updated_prices, asset='BRP_LOP1_RN', date=date)
        magnolia = plot_dart_curves(updated_prices, asset='BRPMAGNO_RN', date=date)
        northfork = plot_dart_curves(updated_prices, asset='NF_BRP_RN', date=date)
        odessa = plot_dart_curves(updated_prices, asset='ODESW_RN', date=date)
        pueblo1 = plot_dart_curves(updated_prices, asset='BRP_PBL1_RN', date=date)
        pueblo2 = plot_dart_curves(updated_prices, asset='BRP_PBL2_RN', date=date)
        ranchtown = plot_dart_curves(updated_prices, asset='BRP_RN_UNIT1', date=date)
        sweeny = plot_dart_curves(updated_prices, asset='BRP_SWNY_RN', date=date)
        zapata1 = plot_dart_curves(updated_prices, asset='BRP_ZPT1_RN', date=date)
        zapata2 = plot_dart_curves(updated_prices, asset='BRP_ZPT2_RN', date=date)

        return  alvin, angleton, batcave, brazoria, dickinson, heights, loop, lopeno, magnolia, northfork, odessa, pueblo1, pueblo2, ranchtown, sweeny, zapata1, zapata2

    elif date == datelist[1] and market == 'RT':
        updated_prices = price_data(asset_dict)
        #create each graph
        alvin = plot_dart_curves(updated_prices, asset='ALVIN_RN', date=date)
        angleton = plot_dart_curves(updated_prices, asset='BRPANGLE_RN', date=date)
        batcave = plot_dart_curves(updated_prices, asset='BATCAVE_RN', date=date)
        brazoria = plot_dart_curves(updated_prices, asset='BRP_BRAZ_RN', date=date)
        dickinson = plot_dart_curves(updated_prices, asset='BRP_DIKN_RN', date=date)
        heights = plot_dart_curves(updated_prices, asset='BRHEIGHT_RN', date=date)
        loop = plot_dart_curves(updated_prices, asset='BRP_LOOP_RN', date=date)
        lopeno = plot_dart_curves(updated_prices, asset='BRP_LOP1_RN', date=date)
        magnolia = plot_dart_curves(updated_prices, asset='BRPMAGNO_RN', date=date)
        northfork = plot_dart_curves(updated_prices, asset='NF_BRP_RN', date=date)
        odessa = plot_dart_curves(updated_prices, asset='ODESW_RN', date=date)
        pueblo1 = plot_dart_curves(updated_prices, asset='BRP_PBL1_RN', date=date)
        pueblo2 = plot_dart_curves(updated_prices, asset='BRP_PBL2_RN', date=date)
        ranchtown = plot_dart_curves(updated_prices, asset='BRP_RN_UNIT1', date=date)
        sweeny = plot_dart_curves(updated_prices, asset='BRP_SWNY_RN', date=date)
        zapata1 = plot_dart_curves(updated_prices, asset='BRP_ZPT1_RN', date=date)
        zapata2 = plot_dart_curves(updated_prices, asset='BRP_ZPT2_RN', date=date)

        return  alvin, angleton, batcave, brazoria, dickinson, heights, loop, lopeno, magnolia, northfork, odessa, pueblo1, pueblo2, ranchtown, sweeny, zapata1, zapata2

    else:
        #create each graph
        alvin = plot_dart_curves(asset_prices, asset='ALVIN_RN', date=date)
        angleton = plot_dart_curves(asset_prices, asset='BRPANGLE_RN', date=date)
        batcave = plot_dart_curves(asset_prices, asset='BATCAVE_RN', date=date)
        brazoria = plot_dart_curves(asset_prices, asset='BRP_BRAZ_RN', date=date)
        dickinson = plot_dart_curves(asset_prices, asset='BRP_DIKN_RN', date=date)
        heights = plot_dart_curves(asset_prices, asset='BRHEIGHT_RN', date=date)
        loop = plot_dart_curves(asset_prices, asset='BRP_LOOP_RN', date=date)
        lopeno = plot_dart_curves(asset_prices, asset='BRP_LOP1_RN', date=date)
        magnolia = plot_dart_curves(asset_prices, asset='BRPMAGNO_RN', date=date)
        northfork = plot_dart_curves(asset_prices, asset='NF_BRP_RN', date=date)
        odessa = plot_dart_curves(asset_prices, asset='ODESW_RN', date=date)
        pueblo1 = plot_dart_curves(asset_prices, asset='BRP_PBL1_RN', date=date)
        pueblo2 = plot_dart_curves(asset_prices, asset='BRP_PBL2_RN', date=date)
        ranchtown = plot_dart_curves(asset_prices, asset='BRP_RN_UNIT1', date=date)
        sweeny = plot_dart_curves(asset_prices, asset='BRP_SWNY_RN', date=date)
        zapata1 = plot_dart_curves(asset_prices, asset='BRP_ZPT1_RN', date=date)
        zapata2 = plot_dart_curves(asset_prices, asset='BRP_ZPT2_RN', date=date)

        return  alvin, angleton, batcave, brazoria, dickinson, heights, loop, lopeno, magnolia, northfork, odessa, pueblo1, pueblo2, ranchtown, sweeny, zapata1, zapata2
