import math
from strategies.base_strategy import BaseStrategy
from alpaca_api import AlpacaAPI
from yahoo_finance_api import YahooFinanceAPI

def main():
    # instantiate alpaca api
    alpaca = AlpacaAPI()
    # instantiate yahoo finance api
    yahoo_finance = YahooFinanceAPI()
    # get list of tickers to trade
    tickers = BaseStrategy().stockpicker()
    # get list of open positions
    open_positions = alpaca.get_all_open_positions()
    # get available cash balance
    available_cash_balance = alpaca.get_cash_balance()

    total_notional = available_cash_balance * 0.20

    # Filter out tickers with a zero asking price or already have positions
    valid_tickers = []
    for ticker in tickers:
        if ticker in open_positions:
            print(f"Skipping {ticker} as it already has an open position.")
            continue

        try:
            current_price = yahoo_finance.get_current_price(ticker)
        except Exception as e:
            print(f"Error fetching current price for {ticker}: {e}")
            continue

        if current_price > 0:
            valid_tickers.append((ticker, current_price))
        else:
            print(f"Skipping {ticker} due to zero asking price.")

    if not valid_tickers:
        print("No valid tickers to trade.")
        return

    notional_per_order = total_notional / len(valid_tickers)

    for ticker, current_price in valid_tickers:
        qty = math.floor(notional_per_order / current_price)
        if qty > 0:
            alpaca.place_buy_market_order(ticker, qty)
            print(f"Placed order for {qty} shares of {ticker} at ${current_price:.2f} per share")

if __name__ == "__main__":
    main()