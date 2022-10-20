from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import DSCC_FP_MVP_Configuration as config

# Create a SQL engine
connect_engine = create_engine(
    # Creating a connection using the server username, password and db name
    "mysql+mysqlconnector://{}:{}@{}/{}".format(
        'root', 'password', 'localhost', 'stock_database')
)

# Read the query and put the result in a dataframe
df = pd.read_sql_query('SELECT * FROM AAPL', connect_engine)
# print(df)

# Statistical calculations


def statistical_calc_col(df, col_name):
    min = df[col_name].min()
    max = df[col_name].max()
    data_range = abs(max-min)
    median = df[col_name].median()
    mean = df[col_name].mean()
    var = df[col_name].var()
    std = df[col_name].std()
    stat_dict = {'Minimum': min, 'Maximum': max, 'Range': data_range,
                 'Median': median, 'Mean': mean, 'Variance': var, 'Standard_Deviation': std}
    return pd.DataFrame([stat_dict])


def statistical_calc(dataframe):
    df_statistical = pd.DataFrame(columns=['Minimum', 'Maximum',
                                           'Range', 'Median', 'Mean', 'Variance', 'Standard_Deviation'])
    col_name_list = ['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']
    for col_name in col_name_list:
        df = statistical_calc_col(dataframe, col_name)
        df_statistical = pd.concat([df_statistical, df])
    df_statistical.index = col_name_list
    return df_statistical


a = statistical_calc(df)
print(a)
