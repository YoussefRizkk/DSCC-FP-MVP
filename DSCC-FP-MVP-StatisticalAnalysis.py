import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import DSCC_FP_MVP_Configuration as config

my_dict = {'Date': 'VARCHAR(12)',
           'Open': 'FLOAT',
           'High': 'FLOAT',
           'Low': 'FLOAT',
           'Close': 'FLOAT',
           'Adj_Close': 'FLOAT',
           'Volume': 'FLOAT'}

# Create a SQL connection
connect_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password'
)

# Create an SQL engine
connect_engine = create_engine(
    "mysql+mysqlconnector://root:password@localhost/stock_database"
)

df1 = pd.read_sql_query('SELECT * FROM AAPL', connect_engine)
print(df1)
