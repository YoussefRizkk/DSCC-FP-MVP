import mysql.connector
import pandas as pd

# Create a MySQL connection object
db_connector = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password'
)

print(db_connector)
# Create a cusor object
db_cursor_object = db_connector.cursor()


# Create a database
def create_database(database_name):
    try:
        db_cursor_object.execute(f'DROP DATABASE IF EXISTS {database_name}')
        db_cursor_object.execute(f'CREATE DATABASE {database_name}')
    except:
        print(f'Couldn\'t create the database')


def create_table(database_name, table_name, columns_as_dict):
    db_cursor_object.execute(f'USE {database_name}')
    column_as_list = []
    for column in columns_as_dict:
        column_as_list.append(f'{column} {columns_as_dict[column]}')
    column_as_str = str(column_as_list)
    column_as_str = column_as_str.replace('\'', '')
    column_as_str = column_as_str.replace('[', '')
    column_as_str = column_as_str.replace(']', '')
    db_cursor_object.execute(f'CREATE TABLE {table_name} ({column_as_str})')
    print(column_as_str)


def ingest_dataframe(df, table_name):
    column_as_str = str(df.columns.values)
    column_as_str = column_as_str.replace('\'', '')
    column_as_str = column_as_str.replace('[', '')
    column_as_str = column_as_str.replace(']', '')
    column_as_str = column_as_str.replace(' ', ', ')
    for column, rows in df.iterrows():
        db_cursor_object.execute(
            f'INSERT INTO {table_name}({column_as_str}) VALUES {tuple(rows.values)}')


my_dict = {'Date': 'VARCHAR(12)',
           'Open': 'FLOAT',
           'High': 'FLOAT',
           'Low': 'FLOAT',
           'Close': 'FLOAT',
           'Adj_Close': 'FLOAT',
           'Volume': 'FLOAT'}

df = pd.read_csv('fetched_data.csv')

create_database('stock_price')
create_table('stock_price', 'AAPL', my_dict)
ingest_dataframe(df, 'AAPL')

db_connector.commit()
