import yfinance as yf
import pandas as pd


class FetchData:
    def __init__(self, ticker) -> None:
        self.ticker = ticker

    def fetch_data_from_to_date(self, start_date='2021-01-01', end_date='2021-12-31'):
        self.start_date = start_date
        self.end_date = end_date
        self.fetch_data = yf.download(
            self.ticker, start=self.start_date, end=self.end_date)
        return self.fetch_data

    def write_to_csv(self, filename):
        return self.fetch_data_from_to_date(self.start_date, self.end_date).to_csv(filename)


data_aapl = FetchData('AAPL')
print(data_aapl.fetch_data_from_to_date())
data_aapl.write_to_csv('test1.csv')
