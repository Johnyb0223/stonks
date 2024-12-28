import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Step 1: Calculate the date for one month ago
end_date = datetime.today().date()  # Today's date
start_date = end_date - timedelta(days=60)  # 30 days ago (approximately last month)

# Step 2: Download AAPL stock data for the last month
data = yf.download("AAPL", start=start_date, end=end_date)

# Step 3: Ensure the date is in the correct format and reset the index
data.reset_index(inplace=True)

# Step 4: Convert the 'Date' column to a string format (optional: you can adjust the format)
data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')

# Step 5: Calculate the 5-day and 20-day moving averages
data['5_MA'] = data['Close'].rolling(window=5).mean()
data['20_MA'] = data['Close'].rolling(window=20).mean()


# Step 6: Flatten column names in case there's a MultiIndex
data.columns = [col if isinstance(col, str) else col[1] for col in data.columns]

# Step 7: Export the cleaned data to Excel
data.to_excel("AAPL_moving_averages.xlsx", index=False, engine="openpyxl")

print("Data with 5-day and 20-day moving averages exported to 'AAPL_moving_averages.xlsx'.")
