import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
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
df.Date = pd.to_datetime(df.Date)
# print(df)

# Instantiation of figure object
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot(df.Date, df.Open)
print(df.dtypes)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
plt.show()

# sns.lineplot(x=df.Date, y=df.Open)
# plt.show()
