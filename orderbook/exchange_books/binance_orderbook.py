# orderbook/binance_orderbook.py
import requests
import pandas as pd

class Exchange:
    def __init__(self, name, api_url):
        self.name = name
        self.api_url = api_url

    def fetch_orderbook(self):
        raise NotImplementedError()

class Binance(Exchange):
    def fetch_orderbook(self):
        response = requests.get(self.api_url + 'api/v3/depth?symbol=BTCUSDT&limit=1000')
        data = response.json()
        bids = pd.DataFrame(data['bids'], columns=['Price', 'Size'])
        bids['Side'] = 'buy'
        asks = pd.DataFrame(data['asks'], columns=['Price', 'Size'])
        asks['Side'] = 'sell'
        return pd.concat([bids, asks], ignore_index=True)
    

if __name__ == '__main__':
    binance = Binance('Binance', 'https://api.binance.com/')
    binance.fetch_orderbook()
    print(binance.fetch_orderbook())
