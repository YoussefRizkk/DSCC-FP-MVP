from DSCC_FP_MVP_Storage import MySQLDatabase as db
# from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# Create an SQL DB connection
connect_engine = db.create_connection(
    'root', 'password', 'localhost', 'new123')


class StatisticalAnalysis(db):
    created_stat_object_list = []

    def __init__(self, connect_engine, table_name) -> None:
        # Takes the connection created previously
        # Use that connection to fetch the corresponding table_name
        # And fetch the data from MySQL server
        self.connect_engine = connect_engine
        self.table_name = table_name
        # Use the method from the parent class-MySQLDatabase by using super()
        # Here i used this method to fetch the data from the SQL server.
        # The variables to compute this is defined above.
        super().fetch_data_from_sql_server()
        StatisticalAnalysis.created_stat_object_list.append(self)

    @staticmethod
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

    def describe_dataframe(self):
        df_statistical = pd.DataFrame(columns=['Minimum', 'Maximum',
                                               'Range', 'Median', 'Mean', 'Variance', 'Standard_Deviation'])
        col_name_list = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        for col_name in col_name_list:
            df = StatisticalAnalysis.statistical_calc_col(
                self.df_fetch_from_sql, col_name)
            df_statistical = pd.concat([df_statistical, df])
        df_statistical.index = col_name_list
        return df_statistical

    def __repr__(self) -> str:
        return f'SA_{self.table_name}'


if __name__ == '__main__':
    stat = StatisticalAnalysis(connect_engine, 'tsla')
    # df = stat.import_data_from_server('SELECT * FROM AAPL')
    stat_df = stat.describe_dataframe()
    print(stat_df)
    print(StatisticalAnalysis.created_stat_object_list)
