# orderbook/analyze.py
import pandas as pd
import matplotlib.pyplot as plt
import time
import subprocess
import requests

# Set the time delay in seconds between each iteration
delay = 0.1
price_range = 50  # Price range for analysis

while True:
    # Execute the main.py script to update the CSV data
    subprocess.run(['python3', 'main.py'])

    # Load the updated orderbook data from the CSV files
    bids_df = pd.read_csv('aggregated_bids.csv')
    asks_df = pd.read_csv('aggregated_asks.csv')

    # Get the current BTC price from binance
    response = requests.get('https://api.binance.com/api/v3/ticker/price', params={'symbol': 'BTCUSDT'})
    current_price = float(response.json()['price'])
    
    # Calculate cumulative sums for bids and asks
    bids_df['cumulative_size'] = bids_df['size'].cumsum()
    asks_df['cumulative_size'] = asks_df['size'].cumsum()

    # Analyze the volumes within the price range
    price_min = current_price - price_range
    price_max = current_price + price_range
    bid_size = bids_df[(bids_df['price'] >= price_min) & (bids_df['price'] <= current_price)]['size'].sum()
    ask_size = asks_df[(asks_df['price'] <= price_max) & (asks_df['price'] >= current_price)]['size'].sum()

    # Clear the previous plot
    plt.clf()

    plt.title("Aggregated Orderbook BTC/USD")
    # Plot the updated cumulative sums
    plt.plot(bids_df['price'], bids_df['cumulative_size'], label='Bids', color='green')
    plt.plot(asks_df['price'], asks_df['cumulative_size'], label='Asks', color='red')

    plt.xlabel('Price')
    plt.ylabel('Cumulative Size')
    plt.legend()

    # Set the tick interval for the price axis to 25 dollars
    plt.xticks(range(int(min(bids_df['price'])), int(max(asks_df['price'])) + 1, 25))

    # Add text to display current price and volume analysis within the price range
    plt.text(0.95, 0.9, f'Current Price: {current_price:.2f}', transform=plt.gca().transAxes, ha='right')
    plt.text(0.95, 0.8, f'Bid Volume: {bid_size:.2f}', transform=plt.gca().transAxes, ha='right')
    plt.text(0.95, 0.7, f'Ask Volume: {ask_size:.2f}', transform=plt.gca().transAxes, ha='right')

    plt.draw()
    plt.pause(0.01)

    time.sleep(delay)