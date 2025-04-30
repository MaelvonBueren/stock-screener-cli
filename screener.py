import pandas as pd 
import numpy as np 
import yfinance as yf 
import datetime as dt 
from pandas_datareader import data as pdr 

tickers = [ticker.strip().upper() for ticker in input("Enter ticker symbols separated by commas: ").split(',')]
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

data = yf.download(tickers, start=start_date, end=end_date)
data = data.dropna(axis=1, how='all')

print(data.head())
