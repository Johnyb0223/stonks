import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(ticker, start_date=None, end_date=None, filename=None):
    # Step 1: Set the end_date and start_date to defaults if not provided
    end_date = end_date or datetime.today().date()  # Default to today's date if not provided
    start_date = start_date or (end_date - timedelta(days=60))  # Default to 60 days ago if not provided

    # Step 2: Download stock data for the specified period
    data = yf.download(ticker, start=start_date, end=end_date)

    # Step 3: Ensure the date is in the correct format and reset the index
    data.reset_index(inplace=True)

    # Step 4: Convert the 'Date' column to a string format (optional: you can adjust the format)
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')

    # Step 5: Calculate the 5-day and 20-day moving averages
    data['5_MA'] = data['Close'].rolling(window=5).mean()
    data['20_MA'] = data['Close'].rolling(window=20).mean()

    # Step 6: Flatten column names in case there's a MultiIndex
    data.columns = [col if isinstance(col, str) else col[1] for col in data.columns]

    # Step 7: If filename is not provided, set it dynamically based on the ticker symbol
    if filename is None:
        filename = f"{ticker} moving average.xlsx"

    # Step 8: Export the cleaned data to Excel
    data.to_excel(filename, index=False, engine="openpyxl")

    print(f"Data with 5-day and 20-day moving averages exported to '{filename}'.")

    return data  # Return the DataFrame in case the caller wants to use it
