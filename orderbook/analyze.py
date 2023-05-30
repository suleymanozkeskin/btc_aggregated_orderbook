import pandas as pd
import matplotlib.pyplot as plt
import time
import subprocess

import requests

# Set the time delay in seconds between each iteration
delay = 0.2
price_range = 50  # Price range for analysis

while True:
    # Execute the main.py script to update the CSV data
    subprocess.run(['python3', 'main.py'])

    # Load the updated orderbook data from the CSV file
    orderbook = pd.read_csv('orderbook.csv')

    # Calculate cumulative sums for buy and sell sides
    orderbook['Buy'] = orderbook[orderbook['Side'] == 'buy']['Size'].cumsum()
    orderbook['Sell'] = orderbook[orderbook['Side'] == 'sell']['Size'].cumsum()

    # Get the current BTC price from binance
    response = requests.get('https://api.binance.com/api/v3/ticker/price', params={'symbol': 'BTCUSDT'})
    current_price = float(response.json()['price'])
    
    # Analyze the buy and sell sides within the price range
    price_min = current_price - price_range
    price_max = current_price + price_range
    buy_size = orderbook[(orderbook['Price'] >= price_min) & (orderbook['Price'] <= price_max) & (orderbook['Side'] == 'buy')]['Size'].sum()
    sell_size = orderbook[(orderbook['Price'] >= price_min) & (orderbook['Price'] <= price_max) & (orderbook['Side'] == 'sell')]['Size'].sum()

    # Clear the previous plot
    plt.clf()

    plt.title("Aggregated Orderbook BTC/USD")
    # Plot the updated cumulative sums for buy and sell sides
    plt.plot(orderbook['Price'], orderbook['Buy'], label='Buy')
    plt.plot(orderbook['Price'], orderbook['Sell'], label='Sell')

    plt.xlabel('Price')
    plt.ylabel('Cumulative Size')
    plt.legend()

    # Set the tick interval for the price axis to 25 dollars
    plt.xticks(range(int(min(orderbook['Price'])), int(max(orderbook['Price'])) + 1, 25))

    # Add text to display current price and buy/sell analysis within the price range
    plt.text(0.95, 0.9, f'Current Price: {current_price:.2f}', transform=plt.gca().transAxes, ha='right')
    plt.text(0.95, 0.8, f'Buy Size: {buy_size:.2f}', transform=plt.gca().transAxes, ha='right')
    plt.text(0.95, 0.7, f'Sell Size: {sell_size:.2f}', transform=plt.gca().transAxes, ha='right')

    plt.draw()
    plt.pause(0.01)  # Add a small delay to allow the plot to update

    # Wait for the specified delay before the next iteration
    time.sleep(delay)

