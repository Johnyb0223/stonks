import yfinance as yf
from datetime import datetime, timedelta

# Function to download stock data and check moving average crossover
def check_moving_average_crossover(ticker, min_price=150):
    # Download historical stock data (adjust start date as needed)
    end_date = datetime.today().date()  # Today's date
    start_date = end_date - timedelta(days=60)  # Get last 60 days of data
    
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # Check if the data is empty (in case of failed download)
    if data.empty:
        print(f"Warning: No data found for {ticker}. Skipping...")
        return False
    
    # Calculate 5-day and 20-day moving averages
    data['5_MA'] = data['Close'].rolling(window=5).mean()
    data['20_MA'] = data['Close'].rolling(window=20).mean()
    
    # Get the latest close price as a scalar
    latest_close = data['Close'].iloc[-1].item()
    
    # Check if the stock price is above the threshold
    if latest_close > min_price:
        # Check for crossover condition (5_MA crosses above 20_MA)
        if data['5_MA'].iloc[-2] < data['20_MA'].iloc[-2] and data['5_MA'].iloc[-1] > data['20_MA'].iloc[-1]:
            # Check if the slope of the 5-day moving average is positive
            if data['5_MA'].iloc[-1] > data['5_MA'].iloc[-3]:  # Compare the current 5_MA with its value two days ago
                return True
    
    return False

