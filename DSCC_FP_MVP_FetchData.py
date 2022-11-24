import yfinance as yf
import pandas as pd


class FetchData:
    """A class to fetch the stock data. 
    """
    created_object_list = []  # A list to add the objects created

    def __init__(self, ticker) -> None:
        """A method to instantiate stock

        Args:
            ticker (string): A single ticker symbol
        """
        self.ticker = ticker
        # Append the instantiated object to the list
        FetchData.created_object_list.append(self)

    def fetch_data_from_to_date(self, start_date='2021-01-01', end_date='2021-12-31', interval='1d') -> pd.core.frame.DataFrame:
        """Fetch data using Yahoo finance API

        Args:
            start_date (str, optional): Start date (yyyy-mm-dd) for fetching the data. Defaults to '2021-01-01'.
            end_date (str, optional): End date (yyyy-mm-dd) for fetching the data. Defaults to '2021-12-31'.
            interval (str, optional): The interval for which the data is to be fetched. Defaults to '1d'.

        Returns:
            pandas.core.frame.DataFrame: Returns a pandas dataframe
        """
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.fetch_data = yf.download(
            self.ticker, start=self.start_date, end=self.end_date, interval=self.interval, group_by='ticker')
        return self.fetch_data.reset_index()

    def write_to_csv(self, filename='fetched_data.csv'):
        """To save the retrived data as a csv file

        Args:
            filename (str, optional): The filename to be saved. Defaults to 'fetched_data.csv'

        Returns:
            .csv file: Returns a csv file
        """
        return self.fetch_data_from_to_date(self.start_date, self.end_date).to_csv(filename)

    @classmethod
    def create_ticker_objects(cls, ticker_symbols: list) -> list:
        """A method to create new objects based on the number of stock tickers in the list given.
           Returns the list of objects created using the class FetchData

        Args:
            ticker_symbols (list): Ticker sysmbols of stock as a list

        Returns:
            list: List of all the obejcts created using the class FetchData
        """
        assert isinstance(ticker_symbols, list), 'The input should be a list'
        for ticker in ticker_symbols:
            FetchData(ticker)
        return FetchData.created_object_list

    def __repr__(self) -> str:
        return f'Ticker_{self.ticker}'


if __name__ == '__main__':
    # data_aapl = FetchData('AAPL')
    # data_aapl.fetch_data_from_to_date(
    #     start_date='2021-01-01', end_date='2021-12-31')
    # # data_aapl.write_to_csv()
    # FetchData.object_list[0].write_to_csv('test.csv')
    FetchData.create_ticker_objects(['AAPL'])
    print(FetchData.created_object_list)
    for i in FetchData.created_object_list:
        df = i.fetch_data_from_to_date()
    print(df)
