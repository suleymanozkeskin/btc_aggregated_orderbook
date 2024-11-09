# orderbook/coinbase_orderbook.py
import requests
import pandas as pd

class Exchange:
    def __init__(self, name, api_url):
        self.name = name
        self.api_url = api_url

    def fetch_orderbook(self):
        raise NotImplementedError()

class Coinbase(Exchange):
    def fetch_orderbook(self):
        response = requests.get(self.api_url + 'products/BTC-USD/book?level=2')
        data = response.json()
        bids = pd.DataFrame(data['bids'], columns=['Price', 'Size', '_'])
        bids['Side'] = 'buy'
        asks = pd.DataFrame(data['asks'], columns=['Price', 'Size', '_'])
        asks['Side'] = 'sell'
        return pd.concat([bids, asks], ignore_index=True)

if __name__ == '__main__':
    coinbase = Coinbase('Coinbase', 'https://api.pro.coinbase.com/')
    print(coinbase.fetch_orderbook())
