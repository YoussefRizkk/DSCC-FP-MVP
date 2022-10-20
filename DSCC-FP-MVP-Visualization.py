from calendar import c
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import DSCC_FP_MVP_Configuration as config
import DSCC_FP_MVP_StatisticalAnalysis as Stat


class VisualizeData(Stat.StatisticalAnalysis):
    def __init__(self) -> None:
        Stat.StatisticalAnalysis.__init__(self)

    def plot_data_as_timeseries(self, col_name):
        df = self.import_data_from_server('SELECT * FROM AAPL')
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


viz_data = VisualizeData()
ax_open = viz_data.plot_data_as_timeseries('Open')
ax_high = viz_data.plot_data_as_timeseries('High')
ax_close = viz_data.plot_data_as_timeseries('Close')
plt.show()


# # Create a SQL engine


# # Read the query and put the result in a dataframe
# df = pd.read_sql_query('SELECT * FROM AAPL', connect_engine)
# df.Date = pd.to_datetime(df.Date)
# # print(df)

# # Instantiation of figure object
# fig = plt.figure()
# ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# ax.plot(df.Date, df.Open)
# print(df.dtypes)
# ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
# plt.show()

# # sns.lineplot(x=df.Date, y=df.Open)
# # plt.show()
