import DSCC_FP_MVP_Configuration as config
from DSCC_FP_MVP_FetchData import FetchData as fd
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.types import Float, DateTime
import pandas as pd
import regex as re


class MySQLDatabase(fd):
    """A class to create an instance of MySQLDatabase in AWS cloud or locally.
        In addition will create table and ingest data from the pandas dataframe.
        Also will raed the data from the sql server.
        For AWS cloud connection, add in the host-api-url, username and password in the config file DSCC_FP_MVP_Configuration
        This class inherits from the class FechData from DSCC_FP_MVP_FetchData.py.
    """
    created_db_ticker_object_list = []

    def __init__(self, ticker_symbol) -> None:
        # To call all the methods from the base class
        super().__init__(ticker_symbol)
        # This is done bcos MySQL  only accepts lowercase as table names
        self.table_name = re.sub(r'\.', '_', ticker_symbol).lower()
        # Passing self here below will pass the object created to perform this method call
        self.dataframe = fd.fetch_data_from_to_date(self)
        # Append the list of created objects into a list
        MySQLDatabase.created_db_ticker_object_list.append(self)

    def ingest_df_to_sql(self):
        self.dataframe.to_sql(self.table_name,
                              MySQLDatabase.connect_engine,
                              if_exists='replace',
                              index=False,
                              chunksize=500,
                              dtype={
                                  'Date': DateTime,
                                  'Open': Float,
                                  'High': Float,
                                  'Low': Float,
                                  'Close': Float,
                                  'Adj Close': Float,
                                  'Volume': Float
                              }
                              )
        print(f'DATA INGESTED SUCESSFULLY')
        # MySQLDatabase.connect_engine.commit()

    @classmethod
    def create_connection(cls, username, password, host_address, database_name):
        url = f'mysql+mysqlconnector://{username}:{password}@{host_address}/{database_name}'
        cls.connect_engine = create_engine(
            url
        )
        if not database_exists(cls.connect_engine.url):
            print(
                f'Database {database_name} does not exist. Creating new database')
            create_database(cls.connect_engine.url)
            print(f'Created database {database_name}')
        return cls.connect_engine

    @classmethod
    def execute_sql_query(cls, query):
        results = MySQLDatabase.connect_engine.execute(text(query))
        return results

    def fetch_data_from_sql_server(self):
        """Fetches data from the sql server as assigns into an object variable 'df_fetch_from_sql'
           Can acess the df using this variable name
        """
        self.df_fetch_from_sql = pd.read_sql_table(
            self.table_name,
            self.connect_engine
        )
        # return self.df_fetch_from_sql

    def __repr__(self) -> str:
        return f'DB_{self.table_name}'


if __name__ == '__main__':
    # The below code is for testing
    print(f'For Testing')
    a = MySQLDatabase('AAPL')
    MySQLDatabase.create_connection(
        'root', 'password', 'localhost', 'stock_check')
    print(a.dataframe)
    a.ingest_df_to_sql()
    a.fetch_data_from_sql_server()
    print(a.df_fetch_from_sql)
