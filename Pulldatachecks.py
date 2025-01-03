#THIS WORKS GREAT FOR PULLING. IT WOULD BE NICE TO ADD IN THE NASDAQ
# ADD IN THE SLOPE CHECKER, VOLUME CHECKER, REDUNDANT CROSS CHECKER
import pandas as pd
from stock_analysis import check_moving_average_crossover

def stockpicker():

    # URL for the S&P 500 Companies List on Wikipedia
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    # Use pandas to scrape the table from Wikipedia
    tables = pd.read_html(url)

    # The table containing the tickers is the first one
    sp500_tickers = tables[0]['Symbol'].tolist()

    # Filter out any rows that are NaN or invalid
    sp500_tickers = [ticker for ticker in sp500_tickers if isinstance(ticker, str) and len(ticker) <= 5]

    # List of stocks that meet the criteria
    stocks_above_150_with_crossover = []

    # Iterate through the list of tickers
    for stock in sp500_tickers:
        if check_moving_average_crossover(stock):
            stocks_above_150_with_crossover.append(stock)
    
    return stocks_above_150_with_crossover

