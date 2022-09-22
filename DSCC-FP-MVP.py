import yfinance as yf
import pandas as pd

mst = yf.Ticker('SMSN.IL')
print(mst.info)
print(type(mst))

data = yf.download('SMSN.IL', start='2021-01-01', end='2021-12-31')
data.to_csv('SMSN.csv')
