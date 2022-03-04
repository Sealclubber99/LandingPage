window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        seven_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Seven Day Load Forecast',
                'legend': {'title': {'text': 'region'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'DateTime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'Value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        asGraph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'BRP Forecast Curves',
                'legend': {'title': {'text': 'region'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'DateTime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'Price'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        fxGraph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'AS Forecast Curves',
                'legend': {'title': {'text': 'region'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'DateTime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'Price'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        outage_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Outage Forecast',
                'legend': {'title': {'text': ''}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'DateTime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'TotalResourceMW'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        solar_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Solar Forecast',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'DateTime'}, 'gridcolor':'#222222'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        wind_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Total Wind Forecast',
                'legend': {'title': {'text': 'region'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'DateTime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        wind_graphs: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Wind by Region',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'DateTime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        netchange_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Netload Change',
                'legend': {'title': {'text': 'Report Time'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'DateTime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'net_load'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        netload_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Netload Forecast',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'DateTime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'Value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        load_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Total Load Forecast',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'DateTime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'Value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        actnet_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Netload Actuals',
                'legend': {'title': {'text': ''}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'Date'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': ''}, 'gridcolor':'#b3b3b3'}}
            };
        },
        ramp_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Ramp Rates',
                'legend': {'title': {'text': ''}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'Date'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': ''}, 'gridcolor':'#b3b3b3'}}
            };
        },
        dart_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Historical Dart',
                'legend': {'title': {'text': 'Node'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'Dart'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'datetime'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        total_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Total Offer through the Day',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'Quantity'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'Hour Ending'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        Bid_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Bid Prices for Selected Hours',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'Quantity'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'Price'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        NSA_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'NSA Constraints',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'RTCA Execution Time'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'MW Violation'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        asset_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Asset Prices',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'datetime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        frequency_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Frequency',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'datetime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        inertia_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Inertia',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'datetime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        hub_graph: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Hub Prices',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'datetime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        actuals_wind: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Wind Actuals',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'datetime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        actuals_solar: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Solar Actuals',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'datetime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        actuals_load: function(data) {
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'}, 'title':'Load Actuals',
                'legend': {'title': {'text': 'type'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'datetime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}}
            };
        },
        regtrans_graph: function(data){
            return {
                'data':data,
                'layout': {'font': {'color': '#222222'},
                'legend': {'title': {'text': 'Reg'}, 'tracegroupgap': 0},
                'margin': {'t': 60},
                'paper_bgcolor': '#F7F7F7',
                'plot_bgcolor': '#F7F7F7',
                'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'datetime'}, 'gridcolor':'#000000'},
                'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}}
            };

        },
        HDL_graph: function(data){
            return {
                'data':data,
                'layout':{
                    'annotations': [{'showarrow': false,
                                'text': 'Minor Price Risk',
                                'x': 1,
                                'xanchor': 'right',
                                'xref': 'x domain',
                                'y': 1500,
                                'yanchor': 'bottom',
                                'yref': 'y'},
                               {'showarrow': false,
                                'text': 'Major Price Risk',
                                'x': 1,
                                'xanchor': 'right',
                                'xref': 'x domain',
                                'y': 1100,
                                'yanchor': 'bottom',
                                'yref': 'y'}],
                    'shapes': [{'line': {'color': 'orange', 'dash': 'dot'},
                           'type': 'line',
                           'x0': 0,
                           'x1': 1,
                           'xref': 'x domain',
                           'y0': 1500,
                           'y1': 1500,
                           'yref': 'y'},
                          {'line': {'color': 'red', 'dash': 'dot'},
                           'type': 'line',
                           'x0': 0,
                           'x1': 1,
                           'xref': 'x domain',
                           'y0': 1100,
                           'y1': 1100,
                           'yref': 'y'}],
                    'font': {'color': '#222222'},
                    'legend': {'tracegroupgap': 0},
                    'paper_bgcolor': '#F7F7F7',
                    'plot_bgcolor': '#F7F7F7',
                    'title': {'text': 'HDL'},
                    'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'dtm'}, 'gridcolor':'#000000'},
                    'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}
                }
            };
        },
        PRC_graph: function(data){
                return{
                'data':data,
                'layout':{
                    'annotations': [{'showarrow': false,
                                'text': 'Price Risk',
                                'x': 1,
                                'xanchor': 'right',
                                'xref': 'x domain',
                                'y': 3000,
                                'yanchor': 'bottom',
                                'yref': 'y'}],
                    'shapes': [{'line': {'color': 'orange', 'dash': 'dot'},
                           'type': 'line',
                           'x0': 0,
                           'x1': 1,
                           'xref': 'x domain',
                           'y0': 1500,
                           'y1': 1500,
                           'yref': 'y'}],
                    'font': {'color': '#222222'},
                    'legend': {'tracegroupgap': 0},
                    'paper_bgcolor': '#F7F7F7',
                    'plot_bgcolor': '#F7F7F7',
                    'title': {'text': 'PRC'},
                    'xaxis': {'anchor': 'y', 'domain': [0.0, 1.0], 'title': {'text': 'dtm'}, 'gridcolor':'#000000'},
                    'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0], 'title': {'text': 'value'}, 'gridcolor':'#b3b3b3'}
                }
            };
        }

    }
});