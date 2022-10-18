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

print(f'Conncted to database {connect_db}')
# Create a cursor object
db_cursor_object = connect_db.cursor()

# Fetch data and put in a dataframe
db_cursor_object.execute('USE stock_database')
db_cursor_object.execute('SELECT * FROM AAPL')
# print(db_cursor_object)
asd = db_cursor_object.fetchall()
# print(asd)
df = pd.DataFrame(asd, columns=my_dict.keys())
# print(df)

df1 = pd.read_sql_query('SELECT * FROM AAPL', connect_db)
print(df1)
# Statistical Analysis

# Create an SQL engine
connect_engine = create_engine(
    "mysql+pymysql://root:password@localhost/stock_database"
)

df1 = pd.read_sql_query('SELECT * FROM AAPL', connect_engine)
print(df1)
