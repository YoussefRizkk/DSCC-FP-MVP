from DSCC_FP_MVP_Storage import MySQLDatabase as db
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Create a connection with the database
connection = db.create_connection(
    'root', 'password', 'localhost', 'new_stock_db')

# Execute a sql query to fetch all the tables from the database
result_from_query = db.execute_sql_query('SHOW TABLES')
# Convert the result obtained into a list which contains the table names
sql_table_name_list = [i[0] for i in result_from_query]
df_fetch_from_sql = pd.read_sql_table(
    sql_table_name_list[0],
    connection)

df = df_fetch_from_sql.rename(columns={'Date': 'ds', 'Adj Close': 'y'})
df = df[['ds', 'y']]
m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=50)
forecast = m.predict(future)
print(type(m.plot(forecast)))
fig = m.plot(forecast)
