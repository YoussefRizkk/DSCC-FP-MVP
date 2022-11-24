import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from DSCC_FP_MVP_StatisticalAnalysis import StatisticalAnalysis as Stat
from DSCC_FP_MVP_Storage import MySQLDatabase as db

# Create a connection
connect_engine = Stat.create_connection(
    'root', 'password', 'localhost', 'new123')


class VisualizeData(Stat):
    def __init__(self, connect_engine, table_name) -> None:
        super().__init__(connect_engine, table_name)

    def plot_data_as_timeseries(self, col_name):
        self.fetch_data_from_sql_server()
        df = self.df_fetch_from_sql
        df.Date = pd.to_datetime(df.Date)
        fig = plt.figure()
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        ax.plot(df.Date, df[col_name])
        # print(df.dtypes)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
        ax.set_xlabel('Time')
        ax.set_ylabel(col_name)
        ax.set_title(col_name)
        return ax


if __name__ == "__main__":
    # Visualize data for a single  ticker
    a = VisualizeData(connect_engine, 'tsla')
    a.fetch_data_from_sql_server()
    print(a.df_fetch_from_sql)
    ax_open = a.plot_data_as_timeseries('Open')
    ax_high = a.plot_data_as_timeseries('High')
    plt.show()
