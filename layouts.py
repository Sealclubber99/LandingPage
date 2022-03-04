import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime, date, timedelta
import dash
from dash.dependencies import Input, Output
import AssetDashboard as ass
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash import dash_table as dsht
from dash.dependencies import Input, Output, State
import dash_table
#background for everything should be #f0f0f0
start_date = date.today() + timedelta(days=0)
end_date = start_date + timedelta(days=2)
import DoQueries as dq
#columns for PTP 7Day tables
columns_all = [{'name': 'Path', 'id': 'Path'}, {'name': 'PnL', 'id': 'PnL'}]
# style for tabs
tab_style = {
    'fontSize': '1rem',
    'color': 'black',
    'fontWeight': 'bold',
}
#styles for selected tabs
selected_tab_style = {
    'color': 'white',
    'fontSize': '1rem',
    'fontWeight': 'bold',
    'background': '#158cba'#'#444445'
}
#wind region dropdown options
wind_regions = ['ISO', 'PANHANDLE', 'COASTAL', 'SOUTH', 'WEST', 'NORTH']
#node dict for node options Proxy
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
#### Page Layouts ####
# RT Market & System Data
rt_sys_data_layout = html.Div(children=[
    dcc.Tabs([
        #as report
        dcc.Tab(label='AS Report', children=[
            html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid", children=[
                html.Div(className="row d-flex justify-content-between", children=[
                    html.Div(className="col-6", children=[
                        html.H3(className="display-3 text-primary", children=["HDL"])
                    ]),
                    #update button for HDL/PRC
                    html.Div(className="col-6 d-flex justify-content-end align-items-center", children=[
                        html.Button(id='hdlButton', children=['Update'], className='btn btn-lg btn-primary')
                    ]),


                ]),
            html.Div(className="row d-flex justify-content-center", children=[
                #HDL store component, updates graph using javascript clientside callback
                dcc.Store(id='HDLData'),
                # HDL Graph
                dcc.Graph(
                    style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'},
                    id='HDLGraph',
                ),
            ]),
            html.Div(className="row", children=[
                html.H3(className="display-3 text-primary", children=["PRC"])
            ]),
            html.Div(className="row d-flex justify-content-center", children=[
                # PRC store component, updates using clientside
                dcc.Store(id='PRCData'),
                # PRC graph
                dcc.Graph(
                    style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'},
                    id='PRC'
                ),

            ])
        ])], style=tab_style, selected_style=selected_tab_style),
        # System Data Tab
        dcc.Tab(label='System Data', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'),className="container-fluid", children=[
            html.Div(className="row d-flex justify-content-between", children=[
                html.Div(className="col-6", children=[
                    html.H3(className="display-3 text-primary", children=["Frequency"])
                ]),
                # update button
                html.Div(className="col-6 d-flex justify-content-end align-items-center ", children=[
                    html.Button(id='freqbutton', children=['Update'], className='btn btn-lg btn-primary')
                ]),

            ]),
            html.Div(className="row d-flex justify-content-center", children=[
                # frequency store component, updates using clientside callback
                dcc.Store(id='frequencyData'),
                # frequency graph
                dcc.Graph(id='frequency', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'},),
            ]),

            html.Div(className="row ", children=[
                html.H3(className="display-3 text-primary", children=["Inertia"])
            ]),
            html.Div(className="row d-flex justify-content-center", children=[
                # inertia store component, updates using clientside callback
                dcc.Store(id='inertiaData'),
                # inertia graph
                dcc.Graph(id='inertia', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'},)

            ])
        ])], style=tab_style, selected_style=selected_tab_style),
        # regulation deployments tab
        dcc.Tab(label='Regulation Deployments', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid", children=[
            # reg deploy update button
            html.Div(className="row d-flex justify-content-between", children=[
                html.Div(className="col-6", children=[
                    html.H3(className="display-3 text-primary", children=["Reg Transform"])
                ]),
                # update button
                html.Div(className="col-6 d-flex justify-content-end align-items-center ", children=[
                    html.Button(id='deployButton', children=['Update'], className='btn btn-lg btn-primary')
                ]),

            ]),
            html.Div(className="row d-flex justify-content-center", children=[
                # reg trans graph store component, updates using clientside callback
                dcc.Store(id='regTransData'),
                # reg trans graph
                dcc.Graph(id='regTransform', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
            ]),
            html.Div(className="row ", children=[
                html.H3(className="display-3 text-primary", children=["Reg Up"])
            ]),
            html.Div(className="row d-flex justify-content-center", children=[
                # Reg up graph (box)
                dcc.Graph(id='rug', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
            ]),
            html.Div(className="row ", children=[
                html.H3(className="display-3 text-primary", children=["Reg Down"])
            ]),
            html.Div(className="row d-flex justify-content-center", children=[
                # reg down graph (box)
                dcc.Graph(id='rdg', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
            ]),
        ])], style=tab_style, selected_style=selected_tab_style),
        # ERCOT dashboard tab
        dcc.Tab(label='ERCOT Dashboard', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid", children=[
            html.Div(className="row justify-content-md-center", children=[
                html.Button(id='mapBtn', children=['Update'], className='btn btn-lg btn-primary')
            ]),
            html.Div(className="row ", children=[
                html.H3(className="display-3 text-primary", children=["Texas Heat Map"])
            ]),
            # # div containing links for BRP power bi
            # html.Div(className="row justify-content-md-center", children=[
            #     html.A('ICE Forwards',
            #            href='https://app.powerbi.com/groups/eac87a79-730b-4de6-8622-4dfc066d1f5d/reports/6d252bd5-fce8-4cb3-ab54-c41ff2a37796/ReportSection299d06f0942674dce843',
            #            className='BILinks', target='_blank'),
            #     html.A('PnL',
            #            href='https://app.powerbi.com/groups/eac87a79-730b-4de6-8622-4dfc066d1f5d/reports/101c705e-3ad1-491a-b6d8-4a8f65d2128b/ReportSectionabc701467783e3700255',
            #            className='BILinks', target='_blank'),
            #     html.A('Optimizer Results',
            #            href='https://app.powerbi.com/groups/eac87a79-730b-4de6-8622-4dfc066d1f5d/reports/5ce74f1f-e702-4b0a-8b10-225f8b329138/ReportSection',
            #            className='BILinks', target='_blank')
            # ]),
            # texas map
            html.Div(className="row d-flex justify-content-around", children=[
                # map
                html.Div([
                    # image updated using source link
                    html.Img(id='TexasMap', style={'width':'80%', 'height':'auto'})
                ], className='col-6 d-flex justify-content-center'),
                # map legend
                html.Div([
                    # legend key, udpated along with map suing source link
                    html.Img(id='LegendKey')
                ], className='col-6 d-flex justify-content-center')
            ])
        ])], style=tab_style, selected_style=selected_tab_style),
    ]),
])

# Fundamentals
fundamentals_layout = html.Div(children=[
    dcc.Tabs([
        # net load tab
        dcc.Tab(label='Net Load Forecast', children=[
            html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid", children=[
                html.Div(className="row d-flex justify-content-between", children=[
                    html.Div(className="col-6", children=[
                        html.H3(className="display-3 text-primary", children=["Netload Forecast"])
                    ]),
                    html.Div(className="col-6 d-flex justify-content-end align-items-center ", children=[
                        # netload update button
                        html.Button(id='netloadButton', children=['Update'], className='btn btn-lg btn-primary')
                    ]),


                ]),
                html.Div(className="row d-flex justify-content-center mb-2", children=[
                    dcc.Store(id='netloadData'),
                    dcc.Graph(id='netloadForecast',style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
                ]),

                html.Div(className="row d-flex justify-content-center", children=[
                    html.Div(className="", id="netloadtable")
                ]),
                html.Div(className="row d-flex justify-content-md-center", id='legend'),
                html.Div(className="row", children=[
                    html.H3(className="display-3 text-primary", children=["Netload Change"])
                ]),
                html.Div(className="row d-flex justify-content-center mb-2", children=[
                    dcc.Store(id='netchangeData'),
                    dcc.Graph(id='netchangegraph', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
                ]),
                html.Div(className="row m-2 d-flex justify-content-md-center", id='netchangetable'),
                html.Div(className="row", children=[
                    html.H3(className="display-3 text-primary", children=["Seven Day Forecast"])
                ]),
                html.Div(className="row d-flex justify-content-center", children=[
                    dcc.Store(id='sevenData'),
                    dcc.Graph(id='day7loadForecast', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
                ]),
                html.Div(className="row", children=[
                    html.H3(className="display-3 text-primary", children=["Outage Forecast"])
                ]),
                html.Div(className="row d-flex justify-content-center", children=[
                    dcc.Store(id='outageData'),
                    dcc.Graph(id='outageForecast', style={'width': '95%', 'minHeight': '35vh', 'maxHeight': '40vh'}),
                ]),
                html.Div(className="row", children=[
                    html.H3(className="display-3 text-primary", children=["Actual Netload"])
                ]),
                html.Div(className="row d-flex justify-content-center", children=[
                    dcc.Store(id='actData'),
                    dcc.Graph(id='actNetload', style={'width': '95%', 'minHeight': '35vh', 'maxHeight': '40vh'}),
                ]),
                html.Div(className="row", children=[
                    html.H3(className="display-3 text-primary", children=["Ramp Forecast"])
                ]),
                html.Div(className="row d-flex justify-content-center", children=[
                    dcc.Store(id='rampData'),
                    dcc.Graph(id='rampForecast', style={'width': '95%', 'minHeight': '35vh', 'maxHeight': '40vh'}),
                ]),
                html.Div(className="row", children=[
                    html.H3(className="display-3 text-primary", children=["Load Forecast"])
                ]),
                html.Div(className="row d-flex justify-content-center", children=[
                    dcc.Store(id='loadTest'),
                    dcc.Graph(id='loadForecast', style={'width': '95%', 'minHeight': '35vh', 'maxHeight': '40vh'}),
                ]),
                html.Div(className="row", children=[
                    html.H3(className="display-3 text-primary", children=["Load Actuals"])
                ]),
                html.Div(className="row d-flex justify-content-center", children=[
                    dcc.Store(id='load_act_data'),
                    dcc.Graph(id='load_act', style={'width': '95%', 'minHeight': '35vh', 'maxHeight': '40vh'}),
                ]),


        ])], style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Wind Forecast', children=[
                html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid", children=[

                    html.Div(className="row d-flex justify-content-between", children=[
                        html.Div(className="col-6", children=[
                            html.H3(className="display-3 text-primary", children=["Wind Forecast"])
                        ]),
                        html.Div(className="col-6 d-flex justify-content-end align-items-center ", children=[
                            # netload update button
                            html.Button(id='windButton', children=['Update'], className='btn btn-lg btn-primary')
                        ]),

                    ]),

                    dcc.Store(id='windgraphData'),
                    html.Div(className="row d-flex justify-content-center", children=[
                        dcc.Graph(id='windGraph',style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
                    ]),
                    html.Div(className="row", children=[
                        html.Div(className="col-6", children=[
                            html.Div(className="row d-flex justify-content-center m-3", children=[
                                html.Div(className="col-6", children=[
                                    dcc.Dropdown(id="region_left",
                                                 options=[{'label': x, 'value': x}
                                                          for x in wind_regions],
                                                 value='WEST'),
                                ])

                            ]),

                            dcc.Store(id='windleftData'),
                            html.Div(className="row d-flex justify-content-center m-1", children=[
                                dcc.Graph(id='dynam_left',
                                          style={'width': '95%', 'minHeight': '30vh', 'maxHeight': '35vh'}),
                            ])


                        ]),
                        html.Div(className="col-6", children=[
                            html.Div(className="row d-flex justify-content-center m-3", children=[
                                html.Div(className="col-6", children=[
                                    dcc.Dropdown(id="region_right",
                                         options=[{'label': x, 'value': x}
                                                  for x in wind_regions],
                                         value='WEST'),
                                ])

                            ]),
                            dcc.Store(id='windrightData'),
                            html.Div(className="row d-flex justify-content-center m-1", children=[
                                dcc.Graph(id='dynam_right', style={'width': '95%', 'minHeight':'30vh', 'maxHeight':'35vh'}),
                            ]),




                        ])
                    ]),
                    html.Div(className="row ", children=[
                        html.H3(className="display-3 text-primary", children=["Wind Actuals"])
                    ]),
                    html.Div(className="row d-flex justify-content-center", children=[
                        dcc.Store(id='wind_act_data'),
                        dcc.Graph(id='wind_act',style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
                    ]),



                ])

        ], style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Solar Forecast', children=[
            html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid",children=[
                html.Div(className="row d-flex justify-content-between", children=[
                    html.Div(className="col-6", children=[
                        html.H3(className="display-3 text-primary", children=["Solar Forecast"])
                    ]),
                    html.Div(className="col-6 d-flex justify-content-end align-items-center ", children=[
                        # netload update button
                        html.Button(id='solarButton', children=['Update'], className='btn btn-lg btn-primary')
                    ]),

                ]),
                html.Div(className="row d-flex justify-content-center", children=[
                    dcc.Store(id='solarData'),
                    dcc.Graph(id='solarForecast', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'})
                ]),
                html.Div(className="row ", children=[
                    html.H3(className="display-3 text-primary", children=["Solar Actuals"])
                ]),
                html.Div(className="row d-flex justify-content-center", children=[
                    dcc.Store(id='solar_act_data'),
                    dcc.Graph(id='solar_act', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'})
                ]),

            ])
        ], style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Generation', children=[
            dcc.Tabs([
                dcc.Tab(label='Current PowerRT Data', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid", children=[
                    html.Div(className="row d-flex justify-content-between", children=[
                        html.Div(className="col-6", children=[
                            html.H3(className="display-3 text-primary", children=["Coal Generation"])
                        ]),
                        html.Div(className="col-6 d-flex justify-content-end align-items-center ", children=[
                            # netload update button
                            html.Button(id='powerButton', children=['Update'], className='btn btn-lg btn-primary')
                        ]),

                    ]),
                    html.Div(className="row d-flex justify-content-center", children=[
                        dcc.Graph(
                            id="emf-coal-fig",
                            style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}
                        )
                    ]),
                    html.Div(className="row", children=[
                        html.H3(className="display-3 text-primary", children=["Gas Generation"])
                    ]),
                    html.Div(className="row d-flex justify-content-center", children=[
                        dcc.Graph(
                            id="emf-gas-fig",
                            style={'width': '95%', 'minHeight': '35vh', 'maxHeight': '40vh'}
                        )
                    ]),
                    html.Div(className="row", children=[
                        html.H3(className="display-3 text-primary", children=["Wind Generation"])
                    ]),
                    html.Div(className="row d-flex justify-content-center", children=[
                        dcc.Graph(
                            id="emf-wind-fig",
                            style={'width': '95%', 'minHeight': '35vh', 'maxHeight': '40vh'}
                        )
                    ]),
                    html.Div(className="row ", children=[
                        html.H3(className="display-3 text-primary", children=["IR Generation"])
                    ]),
                    html.Div(className="row d-flex justify-content-center", children=[
                        dcc.Graph(
                            id="ir-fig",
                            style={'width': '95%', 'minHeight': '35vh', 'maxHeight': '40vh'}
                        )
                    ]),
                    html.Div(className="row ", children=[
                        html.H3(className="display-3 text-primary", children=["Total Generation"])
                    ]),
                    html.Div(className="row d-flex justify-content-center", children=[
                        dcc.Graph(
                            id="total-fig",
                            style={'width': '95%', 'minHeight': '35vh', 'maxHeight': '40vh'}
                        )
                    ]),
                    html.Div(className="row ", children=[
                        html.H3(className="display-3 text-primary", children=["Mix Generation"])
                    ]),
                    html.Div(className="row d-flex justify-content-center", children=[
                        dcc.Graph(
                            id="current-mix-fig",
                            style={'width': '95%', 'minHeight': '35vh', 'maxHeight': '40vh'}
                        )
                    ])
                ])], style=tab_style, selected_style=selected_tab_style),
                dcc.Tab(label='7-Day Historical PowerRT Data', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height='100vh'))], style=tab_style, selected_style=selected_tab_style),
                dcc.Tab(label='DAM Sold Data', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height='100vh'))], style=tab_style, selected_style=selected_tab_style),
            ]),
        ], style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Proxy Heat Rates', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid",children=[
            html.Div(className="row d-flex justify-content-between", children=[
                html.Div(className="col-6", children=[
                    html.H3(className="display-3 text-primary", children=["Proxy Heat Rates"])
                ]),
                html.Div(className="col-6 d-flex justify-content-end align-items-center ", children=[
                    dcc.RadioItems(
                        id='day-choice',
                        options=list(map(lambda x: dict({'label': x, 'value': x}), ['ND', 'ND+1'])),
                        value='ND',
                        labelStyle={'fontSize': 16, 'padding': '1vh', 'marginBottom': '0'},
                        inputStyle={'margin-right': '5px'}
                    ),
                ]),

            ]),

            html.Div(className="row d-flex justify-content-center", children=[
                dcc.Graph(
                    id='proxy-hr',
                    style={'width': '95%', 'minHeight': '35vh', 'maxHeight': '40vh'}
                ),
            ])
        ])], style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Historical Prices', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid", children=[
            html.Div(className="row d-flex justify-content-between", children=[
                html.Div(className="col-6", children=[
                    html.H3(className="display-3 text-primary", children=["Historicals"])
                ]),
                html.Div(className="col-6 d-flex justify-content-end align-items-center ", children=[
                    # netload update button
                    html.Button(id='historicalButton', children=['Update'], className='btn btn-lg btn-primary')
                ]),

            ]),
            html.Div(className="row d-flex justify-content-center mb-3", children=[
                dcc.Store(id='dartData'),
                dcc.Graph(id='Dart', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
            ]),
            html.Div(className="contianer", id="nodeDiv")

        ])], style=tab_style, selected_style=selected_tab_style),
    ]),
])


# AS Alley
as_layout = html.Div(children=[
    dcc.Tabs([
        dcc.Tab(label='AS Forecasts', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'),className="container-fluid", children=[
            html.Div(className="row d-flex justify-content-between", children=[
                html.Div(className="col-4 m-3", children=[
                    html.Button(id='asForButton', children=['Update'], className='btn btn-lg btn-primary'),
                ]),
                html.Div(className="col-4 m-3 d-flex justify-content-end", children=[
                    # netload update button
                    dcc.DatePickerRange(id='dateRange',
                                        min_date_allowed=date(2021, 3, 1),
                                        max_date_allowed=start_date + timedelta(days=3),
                                        # will need to adjust the max date allowed param
                                        end_date=end_date,
                                        start_date=start_date
                                        )
                ]),

            ]),
            html.Div(className="row", children=[
                html.H3(className="display-3 text-primary", children=["FX Graph"])
            ]),
            html.Div(className="row d-flex justify-content-center", children=[

                dcc.Store(id='fxData'),
                dcc.Graph(id='fxGraph', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
            ]),
            html.Div(className="row", children=[
                html.H3(className="display-3 text-primary", children=["Uplan Graph"])
            ]),
            html.Div(className="row d-flex justify-content-center", children=[
                dcc.Store(id='uplanData'),
                dcc.Graph(id='uplanGraph', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
            ]),
            html.Div(className="row", children=[
                html.Div(className="col-6", children=[
                    html.Div(className="row d-flex justify-content-center", children=[
                        html.H3(className="display-3 text-primary", children=["AS Forecast"])
                    ]),
                    html.Div(className="row", id="asTable")
                ]),
                html.Div(className="col-6", children=[
                    html.Div(className="row d-flex justify-content-center", children=[
                        html.H3(className="display-3 text-primary", children=["BRP AS Forecast"])
                    ]),
                    html.Div(className="row", id="uplanTable")
                ])

            ]),
        ])], style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Ancillary Service Bid Graph', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid", children=[
            html.Div(className="row d-flex justify-content-between", children=[
                html.Div(className="col-3", children=[
                    html.H3(className="display-3 text-primary", children=["Total Offer"])
                ]),
                html.Div(className="col-3", children=[
                        html.P("Ancillary Type:"),
                        # anc dropdown, values updated when anc graph is updated
                        dcc.Dropdown(id="asType",
                                     options=[
                                         {'label': 'OFFNS', 'value': 'OFFNS'},
                                         {'label': 'ONNS', 'value': 'ONNS'},
                                         {'label': 'REGDN', 'value': 'REGDN'},
                                         {'label': 'REGUP', 'value': 'REGUP'},
                                         {'label': 'RRSGN', 'value': 'RRSGN'},
                                         {'label': 'RRSLD', 'value': 'RRSLD'},
                                         {'label': 'RRSNC', 'value': 'RRSNC'},
                                     ],
                                     value='OFFNS'
                        )
                ]),
                html.Div(className="col-3", children=[
                    html.P("Date: "),
                    # date dropdown, updated when anc data is, based on dataframe
                    dcc.Dropdown(id="date",
                                 options=ass.getDates(),
                                 value=(date.today() - timedelta(days=1)).strftime("%m/%d/%Y")
                                 ),
                ]),
                html.Div(className="col-3 d-flex justify-content-end", children=[
                    html.Button(id='ancbidButton', children=['Update'], className='btn btn-lg btn-primary')
                ]),
            ]),
            html.Div(className="row d-flex justify-content-center", children=[
                dcc.Store(id='totalOfferData'),
                dcc.Graph(id='totalOffer', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
            ]),
            html.Div(className="row", children=[
                html.H3(className="display-3 text-primary", children=["Bid Prices"])
            ]),
            html.Div(className="row d-flex justify-content-center", children=[
                dcc.Store(id='supplyData'),
                dcc.Graph(id='supplyChart', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
            ])
        ])], style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Historical AS Prices', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height='100vh'))], style=tab_style, selected_style=selected_tab_style),
    ])
])

# Congestion Corner
congestion_layout = html.Div(children=[
    dcc.Tabs([
        dcc.Tab(label='NSA Constraints', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid", children=[
            html.Div(className="row d-flex justify-content-between", children=[
                html.Div(className="col-6", children=[
                    html.H3(className="display-3 text-primary", children=["NSA Constraints"])
                ]),
                html.Div(className="col-6 d-flex justify-content-end align-items-center ", children=[
                    # netload update button
                    html.Button(id='NSAButton', children=['Update'], className='btn btn-lg btn-primary')
                ]),

            ]),
            html.Div(className="row d-flex justify-content-center mb-4", children=[
                dcc.Store(id='nsaData'),
                dcc.Graph(id='nsaGraph', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
            ]),
            html.Div(className="row d-flex justify-content-center", id='NSATable', children=[

            ])
        ])], style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='CIT', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'),className="container-fluid", children=[
            html.Div(className="row d-flex justify-content-between", children=[
                html.Div(className="col-3", children=[
                    html.Div(className="row", children=[
                        html.H5(className="text-primary", children=["Constraint"])
                    ]),
                    html.Div(className="row", children=[
                        dcc.Dropdown(
                            id='constraint-dropdown',
                            className='cit_dropdowns',
                            options=dq.getConstraints(),
                            multi=False, placeholder='Filter by Constraint...',
                            style=dict(fontSize=14),
                        ),
                    ]),
                ]),
                html.Div(className="col-3", children=[
                    html.Div(className="row", children=[
                        html.H5(className=" text-primary", children=["Contingency"])
                    ]),
                    html.Div(className="row", children=[
                        dcc.Dropdown(id='contingency-dropdown',
                                     className='cit_dropdowns',
                                     multi=False, placeholder='Choose Contingency...',
                                     style=dict(fontSize=16),
                                     ),
                    ]),
                ]),
                html.Div(className="col-3", children=[
                    html.Div(className="row", children=[
                        html.H5(className="text-primary", children=["Direction"])
                    ]),
                    html.Div(className="row", children=[
                        dcc.Dropdown(id='direction-dropdown',
                                     className='cit_dropdowns',
                                     multi=False, placeholder='Choose direction...',
                                     style=dict(fontSize=16),
                                     )
                    ])
                ])
            ]),
            html.Div(className="row", children=[
                html.Div(className="col-6", children=[
                    html.Div(className="row d-flex justify-content-center", children=[
                        html.H3(className="display-3 text-primary", children=["CIT Asset"])
                    ]),
                    html.Div(className="row d-flex justify-content-center", id='CIT_asset',
                             children=[
                    ]),
                ]),
                html.Div(className="col-6", children=[
                    html.Div(className="row d-flex justify-content-center", children=[
                        html.H3(className="display-3 text-primary", children=["CIT Hub"])
                    ]),
                    html.Div(className="row d-flex justify-content-center", id='CIT_hub',
                             children=[
                             ]),
                ]),
            ]),
            html.Div(className="row", children=[
                html.H3(className="display-3 text-primary", children=["Asset Shift"])
            ]),
            html.Div(className="row", id='shift_div', children=[

            ])
        ])], style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Point to Point Analysis', children=[
            dcc.Tabs([
                dcc.Tab(label='Last 7 Days', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid", children=[
                    html.Div(className="row justify-content-md-center", children=[
                        html.Button(id='ptpButton', children=['Update'], className='btn btn-lg btn-primary')
                    ]),
                    html.Div(className="row d-flex justify-content-between", children=[
                        html.Div(className="col-4", children=[
                            html.Div(className="row d-flex justify-content-center", children=[
                                html.H5(className="text-primary", children=["Top On"])
                            ]),
                            html.Div(className="row d-flex justify-content-center", children=[
                                dash_table.DataTable(
                                    id='top_on',
                                    # className='topTables',
                                    columns=columns_all,
                                    fill_width=False
                                ),
                            ]),
                        ]),
                        html.Div(className="col-4", children=[
                            html.Div(className="row d-flex justify-content-center", children=[
                                html.H5(className="text-primary", children=["Top Off"])
                            ]),
                            html.Div(className="row  d-flex justify-content-center", children=[
                                dash_table.DataTable(
                                    id='top_off',
                                    # className='topTables',
                                    columns=columns_all,
                                    fill_width=False
                                ),
                            ]),
                        ]),
                        html.Div(className="col-4", children=[
                            html.Div(className="row d-flex justify-content-center", children=[
                                html.H5(className="text-primary", children=["ATC"])
                            ]),
                            html.Div(className="row d-flex justify-content-center", children=[
                                dash_table.DataTable(
                                    id='atc',
                                    # className='topTables',
                                    columns=columns_all,
                                    fill_width=False
                                )
                            ])
                        ]),

                    ]),

                    html.Div(className="row d-flex justify-content-center m-4", children=[
                        html.Div(className="col-6", children=[
                            dcc.Dropdown(
                                id='path-choice',
                                placeholder='choose a path...',

                            ),
                        ])

                    ]),
                    html.Div(className="row",id="path_profitability", children=[

                    ])
                ]),], style=tab_style, selected_style=selected_tab_style),
                dcc.Tab(label='Proxy Days', children=[html.Div(style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), className="container-fluid", children=[
                    html.Div(className="row", children=[
                        html.Div(className="col-3 d-flex flex-column justify-content-center", children=[
                            dcc.RadioItems(
                                id='day-choice',
                                options=list(map(lambda x: dict({'label': x, 'value': x}), ['ND', 'ND+1'])),
                                value='ND',
                                labelStyle={'fontSize': 16, 'padding': '1vh', 'marginBottom': '0'},
                                inputStyle={'margin-right': '5px'}
                            ),

                        ]),
                        html.Div(className="col-6", children=[
                            html.Div(className="row d-flex justify-content-center", children=[
                                html.P(
                                    "Proxy Day Nodal Spread Profile",
                                    style=dict(fontSize=16, fontWeight='bold', textAlign='center', marginTop='1vh'),
                                ),
                            ]),
                            html.Div(className="row m-3", children=[
                                html.Div(className="col-6", children=[
                                    dcc.Dropdown(
                                        id='sink-choice',
                                        options=[{'label': i, 'value': i} for i in node_dict.keys()],
                                        placeholder='Sink node'
                                    ),
                                ]),
                                html.Div(className="col-6", children=[
                                    dcc.Dropdown(
                                        id='source-choice',
                                        options=[{'label': i, 'value': i} for i in node_dict.keys()],
                                        placeholder='Source node'
                                    ),
                                ]),
                            ])
                        ]),

                    ]),
                    html.Div(className="row", children=[
                        html.Div(className="col-6", children=[
                            html.Div(className="row", children=[
                                dcc.Graph(
                                    id='daspread-return',
                                    style=dict(height='65vh'),
                                ),
                            ]),
                            html.Div(className="row m-3", children=[
                                dcc.Slider(
                                    id='he-slider',
                                    min=0,
                                    max=24,
                                    step=1,
                                    value=0,
                                    marks={str(i): str(i) for i in range(0, 25)}
                                ),
                            ])
                        ]),
                        html.Div(className="col-6", children=[
                            html.Div(className="row", children=[
                                dcc.Graph(
                                    id='hour-return',
                                    style=dict(height='65vh'),
                                ),
                            ])
                        ])
                    ])

                ])], style=tab_style, selected_style=selected_tab_style),
            ]),
        ], style=tab_style, selected_style=selected_tab_style),
    ])
])


# Asset Dashboard
assets_layout = html.Div(className="container-fluid", style=dict(backgroundColor='#f0f0f0', height="100%", minHeight='100vh'), children=[
    html.Div(className="row d-flex justify-content-between", children=[
        html.Div(className="col-3", children=[
            html.Button(id='AssetsButton',className="btn btn-lg btn-primary", children=['Update']),
        ]),
        html.Div(className="col-3", children=[
            dcc.RadioItems(
                id='market-choice',
                options=[{'label': 'Real Time', 'value': 'RT'},
                         {'label': 'Day Ahead', 'value': 'DA'}],
                value='DA',
                labelStyle={'fontSize': 16, 'padding': '1vh', 'marginBottom': '0'},
                inputStyle={'margin-right': '5px'}
            ),
        ]),
        html.Div(className="col-3", children=[
            dcc.Dropdown(
                id='assetDate',
                options=ass.getDatesAssets(),
                value=date.today().strftime("%m/%d/%Y")
                # value= (date.today()-timedelta(days=1)).strftime("%m/%d/%Y")
            ),
        ]),
    ]),
    html.Div(className="row", children=[
        html.H3(className="display-3 text-primary", children=["Asset Graph"])
    ]),
    html.Div(className="row d-flex justify-content-center", children=[
        dcc.Store(id='masterData'),
        dcc.Graph(id='master-price', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
    ]),
    html.Div(className="row", children=[
        html.H3(className="display-3 text-primary", children=["Asset Graph"])
    ]),
    html.Div(className="row d-flex justify-content-center", children=[
        dcc.Store(id='hubData'),
        dcc.Graph(id='hub-price', style={'width': '95%', 'minHeight':'35vh', 'maxHeight':'40vh'}),
    ]),
    html.Div(className="row", children=[
        html.H3(className="display-3 text-primary", children=["Asset Graphs"])
    ]),
    html.Div(id="asset_graphs_div")
])

# Power BI Links
power_bi_layout = html.Div(children=[
    html.Div(className="container-fluid d-flex flex-column justify-content-center align-items-center", children=[

            html.Div(className="col-6 m-5 d-flex flex-column align-items-center justify-content-center", children=[
                html.A('ICE Forwards',
                       style={'font-size':'24px'},
                       href='https://app.powerbi.com/groups/eac87a79-730b-4de6-8622-4dfc066d1f5d/reports/6d252bd5-fce8-4cb3-ab54-c41ff2a37796/ReportSection299d06f0942674dce843',
                       className='link-primary font-weight-bold', target='_blank'),
                html.A('PnL',
                       style={'font-size': '24px'},
                       href='https://app.powerbi.com/groups/eac87a79-730b-4de6-8622-4dfc066d1f5d/reports/101c705e-3ad1-491a-b6d8-4a8f65d2128b/ReportSectionabc701467783e3700255',
                       className='link-primary font-weight-bold', target='_blank'),
                html.A('Optimizer Results',
                       style={'font-size': '24px'},
                       href='https://app.powerbi.com/groups/eac87a79-730b-4de6-8622-4dfc066d1f5d/reports/5ce74f1f-e702-4b0a-8b10-225f8b329138/ReportSection',
                       className='link-primary font-weight-bold', target='_blank')
            ])
    ])
])
