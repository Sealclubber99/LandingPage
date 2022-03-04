import sqlalchemy, urllib
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text
import pyodbc
import pandas as pd
from datetime import datetime, timedelta, date
import time
import numpy as np

def proxy_hours(sql_string):
    driver = '{ODBC Driver 17 for SQL Server}'
    server = "brptemp.database.windows.net"
    database = 'ErcotMarketData'
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    conn_string = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
    conn = pyodbc.connect(conn_string)
    df = pd.read_sql(sql_string, conn)
    conn.close()

    return df
def proxy_days(sql_string):
    driver = '{ODBC Driver 17 for SQL Server}'
    server = "brptemp.database.windows.net"
    database = 'ErcotMarketData'
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    conn_string = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
    conn = pyodbc.connect(conn_string)
    df = pd.read_sql(sql_string, conn)
    conn.close()

    return df

def uplan_dbConnect(onTime):
    server = "23.100.120.200"
    database = "LCGProj_ERCOT_ADP"
    username = "UplanA"
    password = "Bro@dRe@chP0wer"
    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str,fast_executemany=True)
    if onTime:
        today = date.today()
    else:
        today = date.today() - timedelta(days=1)
    var_name = '\'ERCOT_ADP_' + str(today) + '\''
    sql = "SELECT [scenarioid] FROM [scenario] where name = " + var_name
    # sql = "SELECT * FROM [scenario]"
    df = pd.read_sql_query(sql, engine)
    scenario_id = df.loc[0, 'scenarioid']
    # print(type(scenario_id))
    db_name = '[outasprice_' + str(scenario_id) + ']'
    # print(db_name)
    sql = "SELECT [timestamp], [product], [price] FROM " + db_name
    df = pd.read_sql_query(sql, engine)
    # print(df['product'].unique())

    test_pivot = df.pivot_table(values='price', index='timestamp', columns='product', aggfunc='first').reset_index().rename_axis(None,axis=1)
    pivot_frame = test_pivot.rename(columns={2:'regup',3:'regdn',4:'rrs',5:'non-spin'}).round(3)
    return(pivot_frame)


def getConstraints():
    driver = '{ODBC Driver 17 for SQL Server}'
    server = "brptemp.database.windows.net"
    database = 'ErcotMarketData'
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    conn_string = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    conn = pyodbc.connect(conn_string)
    sql_string = "SELECT DISTINCT [ConstraintName] FROM [dbo].[Asset_Shift_Factors]"

    df = pd.read_sql(sql_string, conn)
    conn.close()
    names = df['ConstraintName'].tolist()
    return [{'label': i, 'value': i} for i in names]

def getContingencies(constraint):
    driver = '{ODBC Driver 17 for SQL Server}'
    server = "brptemp.database.windows.net"
    database = 'ErcotMarketData'
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    conn_string = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    conn = pyodbc.connect(conn_string)
    sql_string = "SELECT DISTINCT [ContingencyName] FROM [dbo].[Asset_Shift_Factors] where ConstraintName = '" + constraint + "'"

    df = pd.read_sql(sql_string, conn)

    conn.close()
    names = df['ContingencyName'].tolist()
    return [[{'label': i, 'value': i} for i in names]]

def getDirections(contingency, constraint):
    driver = '{ODBC Driver 17 for SQL Server}'
    server = "brptemp.database.windows.net"
    database = 'ErcotMarketData'
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    conn_string = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    conn = pyodbc.connect(conn_string)
    sql_string = "SELECT [Direction] FROM [dbo].[Asset_Shift_Factors] where [ContingencyName] = '" + contingency + "' and [ConstraintName] = '" + constraint + "'"

    df = pd.read_sql(sql_string, conn)
    print(df)
    conn.close()
    if df.empty:
        return False
    return [{'label': i, 'value': i} for i in df['Direction'].tolist()]



def getactnetload():
    server = "brptemp.database.windows.net"
    database = "APX"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    sql = "SELECT [datetime],[netload],[actnetload],[ramprate],[actramprate] FROM [dbo].[temp_netload] where datetime >= dateadd(day,-5,convert(date,getdate()))"
    df = pd.read_sql_query(sql, engine)
    df.replace(0, np.NaN, inplace=True)
    return df

def CIT_data(constraint, contingency):
    driver = '{ODBC Driver 17 for SQL Server}'
    server = "brptemp.database.windows.net"
    database = 'ErcotMarketData'
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    conn_string = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
    conn = pyodbc.connect(conn_string)
    sql_string = "SELECT * FROM [dbo].[Asset_Shift_Factors] where [ContingencyName] = '" + contingency + "' and ConstraintName = '" + constraint + "'"

    df = pd.read_sql(sql_string, conn)
    conn.close()

    return df

def shiftFactors(direction, contingency, constraint):
    driver = '{ODBC Driver 17 for SQL Server}'
    server = "brptemp.database.windows.net"
    database = 'ErcotMarketData'
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    conn_string = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
    conn = pyodbc.connect(conn_string)
    sql_string = "SELECT * FROM [dbo].[master_shift_factors] where [ContingencyName] = '" + contingency + "' and [Direction] = '" + direction + "' and [ConstraintName] = '" + constraint + "'"
    df = pd.read_sql(sql_string, conn)
    conn.close()

    return df



def CIT_data_direction(constraint, contingency, direction):
    driver = '{ODBC Driver 17 for SQL Server}'
    server = "brptemp.database.windows.net"
    database = 'ErcotMarketData'
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    conn_string = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
    conn = pyodbc.connect(conn_string)
    sql_string = "SELECT * FROM [dbo].[Asset_Shift_Factors] where [ContingencyName] = '" + contingency + "' and [Direction] = '" + direction + "' and [ConstraintName] = '" + constraint + "'"

    df = pd.read_sql(sql_string, conn)
    conn.close()

    return df

def fx(startDate, endDate):

    server = "brptemp.database.windows.net"
    database = "APX"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    sql = "SELECT * FROM [dbo].[as_forecast] where OperatingDate >= '" + startDate + "' and OperatingDate < '" + endDate + "'"
    # sql = "SELECT TOP (6000) * FROM [dbo].[as_forecast]"
    df = pd.read_sql_query(sql, engine)
    # df.to_csv(r'C:\Users\sealc\OneDrive\Desktop\CaseyDash\venv\DailyData' + '\\' + 'test.csv')
    return df.round(2)

def getORDC():
    server = "brptemp.database.windows.net"
    database = "ErcotMarketData"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"
    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    sql = "SELECT * FROM [dbo].[ordc_forecast]"

    df = pd.read_sql_query(sql, engine)
    return df.round(2)

def getInertia():
    server = "brptemp.database.windows.net"
    database = "ErcotMarketData"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    sql = "SELECT TOP (80000) [id],[dtm_created],[dtm_updated],[source],[dtm],[value],[data_id],[field_id] FROM [dbo].[spider_isosystemdatavalue] where field_id = 8 order by id desc"
    df = pd.read_sql_query(sql, engine)
    return df


def getFrequency():
    server = "brptemp.database.windows.net"
    database = "ErcotMarketData"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    sql = "SELECT TOP (100000) [id],[dtm_created],[dtm_updated],[source],[dtm],[value],[data_id],[field_id] FROM [dbo].[spider_isosystemdatavalue] where field_id = 1 order by id desc"
    df = pd.read_sql_query(sql, engine)
    return df

def AggASSupply(type_as, date_as):
    server = "brptemp.database.windows.net"
    database = "ErcotMarketData"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    sql = "SELECT * FROM [dbo].[Agg_AS_Curves] where [AncillaryType] = '" + type_as + "' and DeliveryDate = '" + date_as + "'"
    # sql = "SELECT * FROM [dbo].[Agg_AS_Curves]'"
    df = pd.read_sql_query(sql, engine)
    df['Quantity'] = df['Quantity'].astype(float)
    df['Price'] = df['Price'].astype(float)

    # df['HourEnding'] = df['HourEnding'].apply(lambda s: int(s.split(':')[0])) -1
    # df['datetime'] = df['DeliveryDate'] + ' ' + df['HourEnding'].astype(str) + ':00:00'
    # df['datetime'] = pd.to_datetime(df['datetime'],infer_datetime_format=True)
    return df

def getHistorical():
    server = "brptemp.database.windows.net"
    database = "ErcotMarketData"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    sql = "SELECT [flowdate],[flowhour],[daprice],[rtprice],[dart],[node] FROM [dbo].[prices_indexed] where flowdate >= dateadd(day,-10,getdate()) and node in ('HB_NORTH','HB_BUSAVG','HB_HOUSTON','HB_WEST','HB_SOUTH')"
    df = pd.read_sql_query(sql, engine)
    print('this is df:')
    print(df)
    df['datetime'] = pd.to_datetime(df['flowdate'].astype(str) + '  ' + df['flowhour'].astype(str), infer_datetime_format=True)
    return df.drop(['flowdate','flowhour'], axis = 1)



def fixfieldID(row):
    if row['field_id'] == 30:
        return 'Deployed Reg Up'
    elif row['field_id'] == 31:
        return 'Deployed Reg Down'
    elif row['field_id'] == 32:
        return 'Reg-Up Procurement'
    elif row['field_id'] == 33:
        return 'Reg-Down Procurement'
    else:
        return None

def getregDeployment():
    server = "brptemp.database.windows.net"
    database = "ErcotMarketData"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    sql = "SELECT TOP (60000) [id],[dtm_created],[dtm_updated],[source],[dtm],[value],[data_id],[field_id] FROM [dbo].[spider_isosystemdatavalue] where field_id in (30,31,32,33) order by id desc"
    df = pd.read_sql_query(sql, engine)
    df['field type'] = df.apply(lambda row: fixfieldID(row), axis=1)

    df['dtm'] = pd.to_datetime(df['dtm'], infer_datetime_format=True)
    df['dtm'] = df['dtm'] - timedelta(hours=5 + time.localtime().tm_isdst, minutes=0)

    return (df)

def AS_Status(today, DST):
    server = "brptemp.database.windows.net"
    database = "ErcotMarketData"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    start = today
    if DST == 'DST':
        start = start - timedelta(days=30) + timedelta(hours=5, minutes=0)
    else:
        start = start - timedelta(days=30) + timedelta(hours=6, minutes=0)
    print(start)
    sql = f"SELECT [hb],[Reg Down Exhaustion],[Reg Up Exhaustion],[updateTime] FROM [dbo].[Regulation_Deployments] where [hb] >= '{start}'"
    print(sql)
    df = pd.read_sql_query(sql, engine)
    if DST == 'DST':
        df['hb'] = df['hb'] - timedelta(hours=5, minutes=0)
    else:
        df['hb'] = df['hb'] - timedelta(hours=6, minutes=0)
    return (df)

def getRegForecast(start):
    server = "brptemp.database.windows.net"
    database = "ErcotMarketData"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"
    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    sql = "SELECT * \
        from [dbo].[Reg_Deployment_Forecast] \
        WHERE [Date] >= ?;"

    df = pd.read_sql_query(sql, engine, params=[start])
    df['Exhaustion_RD']  = df['Exhaustion_RD'].transform(lambda x: x * -1)
    df.sort_values('datetime', inplace=True)
    return (df)

def getPRC():
    server = "brptemp.database.windows.net"
    database = "ErcotMarketData"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    sql = "SELECT TOP (8000) [id],[dtm_created],[dtm_updated],[source],[dtm],[value],[data_id],[field_id] FROM [dbo].[spider_isosystemdatavalue] where field_id = 42 order by id desc"
    df = pd.read_sql_query(sql, engine)
    return df

def getHDL():
    server = "brptemp.database.windows.net"
    database = "ErcotMarketData"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"
    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    sql = "SELECT TOP (1000) [id],[dtm_created],[dtm_updated],[source],[dtm],[value],[data_id],[field_id] FROM [dbo].[spider_isosystemdatavalue] WHERE field_id = 40 order by id desc"

    df = pd.read_sql_query(sql, engine)
    return (df)

def NSA_Constraints():
    server = "brptemp.database.windows.net"
    database = "meteologica"
    username = "brp_admin"
    password = "Bro@dRe@chP0wer"

    driver = '{ODBC Driver 17 for SQL Server}'
    odbc_str = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;UID=' + username + ';DATABASE=' + database + ';PWD=' + password
    connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
    engine = create_engine(connect_str, fast_executemany=True)

    sql = "SELECT *\
        FROM [dbo].[ERCOT_NSA_Constraints] \
        where RTCAExecutionTime >= dateadd(hour, -12, (select max(RTCAExecutionTime) from dbo.ERCOT_NSA_Constraints))\
        order by RTCAExecutionTime desc"
    df = pd.read_sql_query(sql, engine)
    df = df[
        ['RTCAExecutionTime', 'ContingencyID', 'ContingencyDescription', 'MonitoredElementId', 'MonitoredElementType',
         'ConstrainedSCEDLimitMW', 'PostCTGFlowMVA', 'RTCAPercentViolation']]
    # df.to_csv(r'C:\Users\sealc\PycharmProjects\LandingPage\Data\test.csv')
    df["ConstrainedSCEDLimitMW"] = pd.to_numeric(df["ConstrainedSCEDLimitMW"], downcast="float")
    df["RTCAPercentViolation"] = pd.to_numeric(df["RTCAPercentViolation"], downcast="float")
    df['MWViolation'] = abs(df['PostCTGFlowMVA']) - abs(df['ConstrainedSCEDLimitMW'])
    return df.round(2)

