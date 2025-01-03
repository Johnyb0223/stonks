from dotenv import load_dotenv
import requests
import os

class AlpacaAPI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("ALPACA_API_KEY")
        self.secret_key = os.getenv("ALPACA_SECRET_KEY")
        self.base_url = os.getenv("BASE_ALPACA_URL")
        self.account_url = f"{self.base_url}/v2/account"
        self.orders_url = f"{self.base_url}/v2/orders"
        self.positions_url = f"{self.base_url}/v2/positions"
        self.headers = {
            "accept": "application/json",
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key,
            "content-type": "application/json"
        }

    def get_cash_balance(self):
        response = requests.get(self.account_url, headers=self.headers)
        if response.status_code == 200:
            account_info = response.json()
            return float(account_info['cash'])
        else:
            print(f"Failed to retrieve cash balance: {response.status_code}")
            return None

    def place_buy_market_order(self, symbol, qty):
        payload = {
            "symbol": symbol,
            "qty": qty,
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
        }
        response = requests.post(self.orders_url, json=payload, headers=self.headers)
        return response.json()

    def get_all_open_positions(self):
        '''
        returns a list of all open positions. This includes both buy and sell positions.

        raises an exception if the request fails
        '''
        response = requests.get(self.positions_url, headers=self.headers)
        if response.status_code == 200:
            positions = response.json()
            return [position['symbol'] for position in positions]
        else:
            print(f"Failed to retrieve positions: {response.status_code}")
            return []