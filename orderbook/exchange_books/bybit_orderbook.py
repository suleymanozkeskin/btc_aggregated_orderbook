# orderbook/bybit_orderbook.py
import requests
import pandas as pd

class Exchange:
    def __init__(self, name, api_url):
        self.name = name
        self.api_url = api_url

    def fetch_orderbook(self):
        raise NotImplementedError()

class Bybit(Exchange):
    def fetch_orderbook(self):
        response = requests.get(self.api_url + 'v5/market/orderbook', params={'category': 'spot', 'symbol': 'BTCUSDT', 'limit': 50})
        data = response.json()
        bids = pd.DataFrame(data['result']['b'], columns=['Price', 'Size'])  # Corrected
        bids['Side'] = 'buy'
        asks = pd.DataFrame(data['result']['a'], columns=['Price', 'Size'])  # Corrected
        asks['Side'] = 'sell'
        return pd.concat([bids, asks], ignore_index=True)


        
if __name__ == '__main__':
    bybit = Bybit('Bybit', 'https://api.bybit.com/')
    print(bybit.fetch_orderbook())
