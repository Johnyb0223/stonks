import yfinance as yf
import math
import pandas as pd
from datetime import datetime, timedelta

class YahooFinanceAPI:
    def __init__(self):
        pass

    def get_current_price(self, symbol) -> float:
        '''
        returns the current price of a stock. if the stock is not found, raises an exception
        '''
        stock = yf.Ticker(symbol)
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        if math.isnan(current_price):
            raise Exception(f"Stock {symbol} not found")
        return float(current_price)
    
    def fetch_stock_data(self, ticker, start_date=None, end_date=None):
        end_date = end_date or datetime.today().date()
        start_date = start_date or (end_date - timedelta(days=60))
        data = yf.download(ticker, start=start_date, end=end_date)
        return data
    
    def fetch_stock_info(self, ticker):
        stock_info = yf.Ticker(ticker).info
        return stock_info
