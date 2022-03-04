import pandas as pd
import DoQueries as dq
# from dash import dash_table
import pickle
import dash_table

# 105T105_1
# SBRESAL8
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
asset_dict = {
    'ALVIN_RN': 10016433362,
    'BRPANGLE_RN': 10016437282,
    'BRPMAGNO_RN': 10016437280,
    'BRP_BRAZ_RN': 10016437281,
    'BRP_DIKN_RN': 10016437279,
    'BRP_LOOP_RN': 10016473683,
    'BRP_SWNY_RN': 10016473684,
    'BRHEIGHT_RN': 10016437277,
    'ODESW_RN': 10016433361,
}
hub_dict = {
    'HB_HUBAVG': 10000698382,
    'HB_HOUSTON': 10000697077,
    'HB_NORTH': 10000697078,
    'HB_SOUTH': 10000697079,
    'HB_PAN': 10015999590,
    'HB_WEST': 10000697080,
}
gen_path = r'C:\Users\sealc\PycharmProjects\BroadReachProject\venv\Scripts\Data\generator_dict.pkl'
with open(gen_path, 'rb') as handle:
    gen_dict = pickle.load(handle)


def getCIT(constraint, contingency):
    df = dq.CIT_data(constraint, contingency)

    sf = df.loc[:, df.columns.isin(asset_dict.keys())]

    sf = sf.T.reset_index()
    # print(sf)
    sf.rename(columns={"index": "Asset", 0:"Shift Factor"}, inplace=True)
    # print(sf)
    xf = df.loc[:, df.columns.isin(hub_dict.keys())]
    xf = xf.T.reset_index()

    xf.rename(columns={"index": "Hub", 0:"Shift Factor"}, inplace=True)
    asset_table = dash_table.DataTable(
        data=sf.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in sf.columns],
        id='asset_table_cit',
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell,
        # style_data_conditional=table_style
    )
    hub_table = dash_table.DataTable(
        data=xf.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in xf.columns],
        id='hub_table_cit',
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell,
        # style_data_conditional=table_style
    )
    return asset_table, hub_table


#     '11T436_1' 'SHIWCIT8'

def getCITDirection(constraint, contingency, direction):
    df = dq.CIT_data_direction(constraint, contingency, direction)

    sf = df.loc[:, df.columns.isin(asset_dict.keys())]

    sf = sf.T.reset_index()
    sf.rename(columns={"index": "Asset", 0:"Shift Factor"}, inplace=True)
    # # print(sf)
    # sf.columns = ['Asset', 'Shift Factor']
    # # print(sf)
    xf = df.loc[0:, df.columns.isin(hub_dict.keys())]
    xf = xf.T.reset_index()

    xf.rename(columns={"index": "Hub", 0: "Shift Factor"}, inplace=True)
    asset_table = dash_table.DataTable(
        data=sf.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in sf.columns],
        id='asset_table_cit',
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell,
        # style_data_conditional=table_style
    )
    hub_table = dash_table.DataTable(
        data=xf.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in xf.columns],
        id='hub_table_cit',
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell,
        # style_data_conditional=table_style
    )
    return asset_table, hub_table


#     '11T436_1' 'SHIWCIT8'

def update_shift_table(constraint, contingency, direction):
    df = dq.shiftFactors(direction, contingency, constraint)

    # sf = df.loc[:, df.columns.isin(gen_dict['solar'].values())]
    # sf = sf.T.reset_index()
    # sf = sf.dropna()
    # sf.to_csv(r'C:\Users\sealc\PycharmProjects\LandingPage\Data\test.csv', index=False)
    # print("sf")
    # print(sf.shape)
    tf = df.loc[:, df.columns.isin(gen_dict['thermal'].values())]
    #
    df.to_csv(r'C:\Users\sealc\PycharmProjects\LandingPage\Data\test.csv', index=False)
    tf = tf.T.reset_index()
    tf = tf.dropna()
    # tf.to_csv(r'C:\Users\sealc\PycharmProjects\LandingPage\Data\test.csv', index=False)
    print(df.shape)
    tf.columns = ['Generator', 'Shift Factor']

    wf = df.loc[:, df.columns.isin(gen_dict['wind'].values())]
    wf = wf.T.reset_index()
    wf = wf.dropna()
    wf.columns = ['Generator', 'Shift Factor']
    try:
        # sf.columns = ['Generator', 'Shift Factor']
        print("idk")
    except:
        print("failure")
        return [],[]

    thermal_table = dash_table.DataTable(
        data=tf.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in tf.columns],
        id='thermal_table_cit',
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell,
        # style_data_conditional=table_style
    )

    # solar_table = dash_table.DataTable(
    #     data=sf.to_dict('records'),
    #     columns=[{'name': i, 'id': i} for i in sf.columns],
    #     id='solar_table_cit',
    #     style_table=style_table,
    #     style_header=style_header,
    #     style_cell=style_cell,
    #     # style_data_conditional=table_style
    # )

    wind_table = dash_table.DataTable(
        data=wf.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in wf.columns],
        id='wind_table_cit',
        style_table=style_table,
        style_header=style_header,
        style_cell=style_cell,
        # style_data_conditional=table_style
    )
    return wind_table, thermal_table,

