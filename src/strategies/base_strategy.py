import pandas as pd
from yahoo_finance_api import YahooFinanceAPI

class BaseStrategy:

    def __init__(self):
        pass

    def calculate_rsi(self, data, window=14):
        delta = data['Close'].diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_cci(self, data, window=20):
        tp = (data['High'] + data['Low'] + data['Close']) / 3  # Typical price
        sma = tp.rolling(window=window).mean()
        mean_deviation = tp.rolling(window=window).apply(lambda x: (x - x.mean()).abs().mean(), raw=False)
        cci = (tp - sma) / (0.015 * mean_deviation)
        return cci

    def check_moving_average_crossover(self, ticker, min_price=50, rsi_window=14, rsi_threshold=50):

        yahoo_finance = YahooFinanceAPI()
        stock_info = yahoo_finance.fetch_stock_info(ticker)
        data = yahoo_finance.fetch_stock_data(ticker)

        if data.empty:
            print(f"Warning: No data found for {ticker}. Skipping...")
            return False

        data['5_MA'] = data['Close'].rolling(window=5).mean()
        data['20_MA'] = data['Close'].rolling(window=20).mean()
        data['13_MA'] = data['Close'].rolling(window=13).mean()
        data['RSI'] = self.calculate_rsi(data, window=rsi_window)
        data['CCI'] = self.calculate_cci(data, window=20)
        
        latest_close = data['Close'].iloc[-1].item()
        latest_rsi = data['RSI'].iloc[-1].item()
        latest_cci = data['CCI'].iloc[-1].item()
        pe_ratio = stock_info.get('trailingPE', None)

        # Check conditions (crossover, RSI, CCI, P/E ratio)
        if latest_close > min_price:
            if data['5_MA'].iloc[-2] < data['20_MA'].iloc[-2] and data['5_MA'].iloc[-1] > data['20_MA'].iloc[-1]:
                if data['5_MA'].iloc[-1] > data['5_MA'].iloc[-3]:
                    if data['13_MA'].iloc[-1] > data['13_MA'].iloc[-3]:
                        if latest_rsi < rsi_threshold:
                            if latest_cci > 0:
                                if pe_ratio and 18 < pe_ratio < 25:
                                    return True

        return False

    def stockpicker(self):
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        sp500_tickers = tables[0]['Symbol'].tolist()
        sp500_tickers = [ticker for ticker in sp500_tickers if isinstance(ticker, str) and len(ticker) <= 5]

        stocks_above_150_with_crossover = []

        for stock in sp500_tickers:
            if self.check_moving_average_crossover(stock):
                stocks_above_150_with_crossover.append(stock)
    
        return stocks_above_150_with_crossover