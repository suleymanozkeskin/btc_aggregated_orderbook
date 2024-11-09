# orderbook/okex_orderbook.py
import requests
import pandas as pd

class Exchange:
    def __init__(self, name, api_url):
        self.name = name
        self.api_url = api_url

    def fetch_orderbook(self):
        raise NotImplementedError()

class OKEx(Exchange):
    def fetch_orderbook(self):
        response = requests.get(self.api_url + 'api/v5/market/books?instId=BTC-USDT&sz=400')  # Add sz parameter here
        data = response.json()
        if data.get('code') == '0':
            orderbook = data['data'][0]  # Access the first element of the data array
            bids = pd.DataFrame(orderbook['bids'], columns=['Price', 'Size', '_', '_'])
            bids['Side'] = 'buy'
            asks = pd.DataFrame(orderbook['asks'], columns=['Price', 'Size', '_', '_'])
            asks['Side'] = 'sell'
            return pd.concat([bids, asks], ignore_index=True)
        else:
            print('Error fetching orderbook:', data.get('msg'))
            return None



if __name__ == '__main__':
    okex = OKEx('OKEx', 'https://www.okex.com/')
    print(okex.fetch_orderbook())
