# orderbook/analyze.py
import pandas as pd
import matplotlib.pyplot as plt
import time
import subprocess
import requests
from matplotlib.widgets import Button

# Set the time delay in seconds between each iteration
delay = 0.1
price_range = 50  # Price range for analysis

# Create a flag for controlling the main loop
running = True

def shutdown(event):
    """Callback function to handle shutdown when the button is clicked"""
    global running
    running = False
    plt.close('all')

# Create the main figure and axes
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # Make room for the button

# Quit button
ax_button = plt.axes([0.8, 0.05, 0.1, 0.075])  # [left, bottom, width, height]
button = Button(ax_button, 'Quit', color='lightgray', hovercolor='red')
button.on_clicked(shutdown)

while running:
    try:
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

        # Clear the previous plot but keep the button
        ax.clear()

        ax.set_title("Aggregated Orderbook BTC/USD")
        # Plot the updated cumulative sums
        ax.plot(bids_df['price'], bids_df['cumulative_size'], label='Bids', color='green')
        ax.plot(asks_df['price'], asks_df['cumulative_size'], label='Asks', color='red')

        ax.set_xlabel('Price')
        ax.set_ylabel('Cumulative Size')
        ax.legend()

        # Set the tick interval for the price axis to 25 dollars
        ax.set_xticks(range(int(min(bids_df['price'])), int(max(asks_df['price'])) + 1, 25))

        # Add text to display current price and volume analysis within the price range
        ax.text(0.95, 0.9, f'Current Price: {current_price:.2f}', transform=ax.transAxes, ha='right')
        ax.text(0.95, 0.8, f'Bid Volume: {bid_size:.2f}', transform=ax.transAxes, ha='right')
        ax.text(0.95, 0.7, f'Ask Volume: {ask_size:.2f}', transform=ax.transAxes, ha='right')

        plt.draw()
        plt.pause(0.01)

        time.sleep(delay)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        running = False

plt.close('all')