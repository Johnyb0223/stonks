import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import time

# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate CCI
def calculate_cci(data, window=20):
    tp = (data['High'] + data['Low'] + data['Close']) / 3  # Typical price
    sma = tp.rolling(window=window).mean()
    mean_deviation = tp.rolling(window=window).apply(lambda x: (x - x.mean()).abs().mean(), raw=False)
    cci = (tp - sma) / (0.015 * mean_deviation)
    return cci

def get_pe_ratio(ticker):
    try:
        stock_info = yf.Ticker(ticker).info
        pe_ratio = stock_info.get('trailingPE', None)
        return pe_ratio
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Function to download stock data and check moving average crossover with RSI and CCI conditions
def check_moving_average_crossover(ticker, min_price=50, rsi_window=14, rsi_threshold=50):
    # Download historical stock data
    end_date = datetime.today().date()  # Today's date
    start_date = end_date - timedelta(days=60)  # Get last 60 days of data
    
    # Pause to avoid hitting API rate limits
    time.sleep(.2)  # Sleep for 2 seconds between requests (adjust as needed)

    data = yf.download(ticker, start=start_date, end=end_date)

    # Check if the data is empty (in case of failed download)
    if data.empty:
        print(f"Warning: No data found for {ticker}. Skipping...")
        return False
    
    # Fetch stock info only once
    stock_info = yf.Ticker(ticker).info

    # Calculate moving averages, RSI, and CCI
    data['5_MA'] = data['Close'].rolling(window=5).mean()
    data['20_MA'] = data['Close'].rolling(window=20).mean()
    data['RSI'] = calculate_rsi(data, window=rsi_window)
    data['CCI'] = calculate_cci(data, window=20)
    
    # Get the latest values
    latest_close = data['Close'].iloc[-1].item()
    latest_rsi = data['RSI'].iloc[-1].item()
    latest_cci = data['CCI'].iloc[-1].item()

    # Get P/E ratio
    pe_ratio = stock_info.get('trailingPE', None)
    
    # Check conditions (crossover, RSI, CCI, P/E ratio)
    if latest_close > min_price:
        if data['5_MA'].iloc[-2] < data['20_MA'].iloc[-2] and data['5_MA'].iloc[-1] > data['20_MA'].iloc[-1]:
            if data['5_MA'].iloc[-1] > data['5_MA'].iloc[-3]:
                if latest_rsi < rsi_threshold:
                    if latest_cci > 0:
                        if pe_ratio < 25:
                            if pe_ratio > 18:
                                return True
    
    return False
