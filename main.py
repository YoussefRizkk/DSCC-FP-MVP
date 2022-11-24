from DSCC_FP_MVP_FetchData import FetchData as fd
from DSCC_FP_MVP_Storage import MySQLDatabase as db
from DSCC_FP_MVP_StatisticalAnalysis import StatisticalAnalysis as sa

# Create an SQL DB connection
connect_engine = db.create_connection(
    'root', 'password', 'localhost', 'new_stock_db')
# List of Ticker Symbols For Which the data needs to be fetched
ticker_list = ['AAPL', 'SMSN.IL', 'TSLA']

# Iterate through the list of ticker symbols
for idx, ticker_symbol in enumerate(ticker_list):
    # Create the ticker object
    db(ticker_symbol)
    # Ingest the data using the object's memory location
    db.created_db_ticker_object_list[idx].ingest_df_to_sql()


# Apply the fetch_data_from_to_date method for all tickers and ingest into the Database
# for idx, ticker_object in enumerate(tickers_object_list):
#     df = ticker_object.fetch_data_from_to_date()
#     db(ticker_object.ticker, df)
#     db.created_db_ticker_object_list[idx].ingest_df_to_sql()
#     print(f'DATA INSERTED FOR {ticker_object.ticker}')
#     sa(connect_engine, db.created_db_ticker_object_list[idx].table_name)
#     print(f'COMPUTING STATISTICAL DATA FOR {ticker_object.ticker}')
#     df_statistical = sa.created_stat_object_list[idx].describe_dataframe()

# Fetch data from the SQL databse locally
# print(connect_engine)
# stat = sa(connect_engine)
# df = stat.import_data_from_server('SELECT * FROM AAPL')
# for idx, ticker_object in enumerate(tickers_object_list):
#     print(idx, ticker_object)
