import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to download stock data and check moving average crossover with RSI condition
def check_moving_average_crossover(ticker, min_price=150, rsi_window=14, rsi_threshold=40):
    # Download historical stock data (adjust start date as needed)
    end_date = datetime.today().date() # Today's date
    start_date = end_date - timedelta(days=50)  # Get last 60 days of data
    
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # Check if the data is empty (in case of failed download)
    if data.empty:
        print(f"Warning: No data found for {ticker}. Skipping...")
        return False
    
    # Calculate 5-day and 20-day moving averages
    data['5_MA'] = data['Close'].rolling(window=5).mean()
    data['20_MA'] = data['Close'].rolling(window=20).mean()
    
    # Calculate RSI
    data['RSI'] = calculate_rsi(data, window=rsi_window)
    
    # Get the latest close price and RSI as scalars
    latest_close = data['Close'].iloc[-1].item()  # Use .item() to get a scalar value
    latest_rsi = data['RSI'].iloc[-1].item()      # Use .item() to get a scalar value

    
    # Check if the stock price is above the threshold
    if latest_close > min_price:
        # Check for crossover condition (5_MA crosses above 20_MA)
        if data['5_MA'].iloc[-2] < data['20_MA'].iloc[-2] and data['5_MA'].iloc[-1] > data['20_MA'].iloc[-1]:
            # Check if the slope of the 5-day moving average is positive
            if data['5_MA'].iloc[-1] > data['5_MA'].iloc[-3]:
                # Check if RSI is below the threshold
                if latest_rsi < rsi_threshold:
                    return True
    
    return False
