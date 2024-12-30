import requests
import math
from Pulldatachecks import stockpicker
from dotenv import load_dotenv
import os
import yfinance as yf

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")

base_url = "https://paper-api.alpaca.markets"
account_url = f"{base_url}/v2/account"
orders_url = f"{base_url}/v2/orders"
quote_url = "https://data.alpaca.markets/v2/stocks/quotes/latest"

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": api_key,
    "APCA-API-SECRET-KEY": secret_key,
    "content-type": "application/json"
}

def get_buying_power():
    response = requests.get(account_url, headers=headers)
    account_info = response.json()
    return float(account_info['buying_power'])

def get_current_price(symbol):
    stock = yf.Ticker(symbol)
    current_price = stock.history(period="1d")['Close'].iloc[-1]
    return float(current_price) if not math.isnan(current_price) else 0

def place_market_order(symbol, qty):
    payload = {
        "symbol": symbol,
        "qty": qty,
        "side": "buy",
        "type": "market",
        "time_in_force": "day",
    }
    response = requests.post(orders_url, json=payload, headers=headers)
    return response.json()

def delete_all_orders():
    response = requests.delete(orders_url, headers=headers)
    if response.status_code == 207:
        print("All open orders have been attempted to be cancelled.")
    elif response.status_code == 500:
        print("Failed to cancel some orders.")
    else:
        print(f"Unexpected response: {response.status_code}")

def get_open_positions():
    response = requests.get(f"{base_url}/v2/positions", headers=headers)
    if response.status_code == 200:
        positions = response.json()
        return [position['symbol'] for position in positions]
    else:
        print(f"Failed to retrieve positions: {response.status_code}")
        return []

def main():
    delete_all_orders()  # Delete all open orders before placing new ones

    tickers = stockpicker()
    open_positions = get_open_positions()
    buying_power = get_buying_power()
    total_notional = buying_power * 0.20

    # Filter out tickers with a zero asking price or already have positions
    valid_tickers = []
    for ticker in tickers:
        if ticker in open_positions:
            print(f"Skipping {ticker} as it already has an open position.")
            continue

        current_price = get_current_price(ticker)
        if current_price > 0:
            valid_tickers.append((ticker, current_price))
        else:
            print(f"Skipping {ticker} due to zero asking price.")

    if not valid_tickers:
        print("No valid tickers to trade.")
        return

    notional_per_order = total_notional / len(valid_tickers)

    for ticker, current_price in valid_tickers:
        print(f"Current price for {ticker}: {current_price}")
        qty = math.floor(notional_per_order / current_price)
        if qty > 0:
            order_response = place_market_order(ticker, qty)
            print(f"Order response for {ticker}: {order_response}")
        else:
            print(f"Insufficient funds to buy any shares of {ticker}")

if __name__ == "__main__":
    main()