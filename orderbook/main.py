import pandas as pd
from bybit_orderbook import Bybit
from coinbase_orderbook import Coinbase
from okex_orderbook import OKEx
from binance_orderbook import Binance

# Initialize exchange objects
bybit = Bybit('Bybit', 'https://api.bybit.com/')
coinbase = Coinbase('Coinbase', 'https://api.pro.coinbase.com/')
okex = OKEx('OKEx', 'https://www.okex.com/')
binance = Binance('Binance', 'https://api.binance.com/')

# Fetch orderbook data
bybit_orderbook = bybit.fetch_orderbook()
coinbase_orderbook = coinbase.fetch_orderbook()
okex_orderbook = okex.fetch_orderbook()
binance_orderbook = binance.fetch_orderbook()

# Select only the relevant columns for each DataFrame
bybit_orderbook = bybit_orderbook[['Price', 'Size', 'Side']]
coinbase_orderbook = coinbase_orderbook[['Price', 'Size', 'Side']]
okex_orderbook = okex_orderbook[['Price', 'Size', 'Side']]
binance_orderbook = binance_orderbook[['Price', 'Size', 'Side']]

# Concatenate the modified DataFrames
orderbook = pd.concat([bybit_orderbook, okex_orderbook, binance_orderbook], ignore_index=True)


# You may want to sort the orderbook based on price
orderbook = orderbook.sort_values(by=['Price'], ascending=False).reset_index(drop=True)

# Save the orderbook to a csv file
orderbook.to_csv('orderbook.csv', index=False)


if __name__ == '__main__':
    # print each exchange's orderbook with respective title
    # print(bybit.name)
    # print(bybit_orderbook)
    # print(coinbase.name)
    # print(coinbase_orderbook)
    # print(okex.name)
    # print(okex_orderbook)
    # print(binance.name)
    # print(binance_orderbook)
    print(orderbook)

