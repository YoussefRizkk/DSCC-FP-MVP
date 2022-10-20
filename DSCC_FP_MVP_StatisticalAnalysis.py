from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import DSCC_FP_MVP_Configuration as config


class StatisticalAnalysis():
    def __init__(self) -> None:
        # Create a SQL engine
        self.connect_engine = create_engine(
            # Creating a connection using the server username, password and db name
            "mysql+mysqlconnector://{}:{}@{}/{}".format(
                'root', 'password', 'localhost', 'stock_database')
        )

    def import_data_from_server(self, query):
        self.df = pd.read_sql_query(query, self.connect_engine)
        return self.df

    def statistical_calc_col(self, df, col_name):
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

    def describe_dataframe(self, dataframe):
        df_statistical = pd.DataFrame(columns=['Minimum', 'Maximum',
                                               'Range', 'Median', 'Mean', 'Variance', 'Standard_Deviation'])
        col_name_list = ['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']
        for col_name in col_name_list:
            df = self.statistical_calc_col(dataframe, col_name)
            df_statistical = pd.concat([df_statistical, df])
        df_statistical.index = col_name_list
        return df_statistical


stat = StatisticalAnalysis()
df = stat.import_data_from_server('SELECT * FROM AAPL')
stat_df = stat.describe_dataframe(df)
print(stat_df)
