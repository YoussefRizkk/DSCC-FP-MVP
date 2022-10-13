import DSCC_FP_MVP_Configuration as config
import mysql.connector
import pandas as pd


class MySQLDatabase:

    def __init__(self) -> None:
        # Create a connection with the SQL server
        self.connect_db = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password
        )

        # Create a cursor object
        self.db_cursor_object = self.connect_db.cursor()

    def create_database(self, database_name):
        self.db_name = database_name
        try:
            self.db_cursor_object.execute(
                f'DROP DATABASE IF EXISTS {self.db_name}')
            self.db_cursor_object.execute(f'CREATE DATABASE {self.db_name}')
            print(f'Database {self.db_name} created')
        except:
            print(f'Couldn\'t create the database')
        self.connect_db.commit()

    def create_table(self, table_name, column_and_datatype):
        self.table_name = table_name
        self.column_and_datatype = column_and_datatype
        self.db_cursor_object.execute(
            f'USE {self.db_name}'
        )
        column_as_list = []
        for column in column_and_datatype:
            column_as_list.append(f'{column} {column_and_datatype[column]}')
        column_as_str = str(column_as_list)
        column_as_str = column_as_str.replace('\'', '')
        column_as_str = column_as_str.replace('[', '')
        column_as_str = column_as_str.replace(']', '')
        self.db_cursor_object.execute(
            f'CREATE TABLE {table_name} ({column_as_str})')
        print(
            f'Table {table_name} created with columns and data types as ({column_as_str})')
        self.connect_db.commit()

    def ingest_dataframe(self, df):
        column_name = self.column_and_datatype.keys()
        self.column_name = ', '.join(column_name)
        for column, rows in df.iterrows():
            self.db_cursor_object.execute(
                f'INSERT INTO {self.table_name}({self.column_name}) VALUES {tuple(rows.values)}'
            )
        self.connect_db.commit()

    def execute_sql_command(self, command):
        self.db_cursor_object.execute(command)

    def fetch_results(self):
        return self.db_cursor_object.fetchall()


my_dict = {'Date': 'VARCHAR(12)',
           'Open': 'FLOAT',
           'High': 'FLOAT',
           'Low': 'FLOAT',
           'Close': 'FLOAT',
           'Adj_Close': 'FLOAT',
           'Volume': 'FLOAT'}

df = pd.read_csv('fetched_data.csv')
new = MySQLDatabase()
new.create_database('stock_database')
new.create_table('AAPL', my_dict)
new.ingest_dataframe(df)
sql_command = 'SELECT * FROM AAPL'
new.execute_sql_command(sql_command)
asd = new.fetch_results()
df = pd.DataFrame(asd)
df.columns = my_dict.keys()
print(df)
