# orderbook/analyze_PyQT.py
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import pandas as pd
import time
import subprocess
import requests
from threading import Thread

# Set the time delay in seconds between each iteration
delay = 0.1
price_range = 50  # Price range for analysis

class Worker(QtCore.QObject):
    data_fetched = QtCore.pyqtSignal(pd.DataFrame, pd.DataFrame, float)

    def run(self):
        while True:
            # Execute the main.py script to update the CSV data
            subprocess.run(['python3', 'main.py'])

            # Get the current BTC price from binance
            response = requests.get('https://api.binance.com/api/v3/ticker/price', params={'symbol': 'BTCUSDT'})
            current_price = float(response.json()['price'])

            # Load the updated orderbook data from the CSV files
            bids_df = pd.read_csv('aggregated_bids.csv')
            asks_df = pd.read_csv('aggregated_asks.csv')

            # Calculate cumulative sums
            bids_df['cumulative_size'] = bids_df['size'].cumsum()
            asks_df['cumulative_size'] = asks_df['size'].cumsum()

            self.data_fetched.emit(bids_df, asks_df, current_price)

            time.sleep(delay)

app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(title="Aggregated Orderbook BTC/USD")
plot = win.addPlot()
plot.setLabel('left', 'Cumulative Size')
plot.setLabel('bottom', 'Price')

curve_bids = plot.plot(pen='g')  # green pen for bids
curve_asks = plot.plot(pen='r')  # red pen for asks

title = pg.LabelItem(justify='right')
win.addItem(title)

worker = Worker()
thread = QtCore.QThread()

def on_data_fetched(bids_df, asks_df, current_price):
    # Analyze the volumes within the price range
    price_min = current_price - price_range
    price_max = current_price + price_range
    bid_size = bids_df[(bids_df['price'] >= price_min) & (bids_df['price'] <= current_price)]['size'].sum()
    ask_size = asks_df[(asks_df['price'] <= price_max) & (asks_df['price'] >= current_price)]['size'].sum()

    # Update the plots
    curve_bids.setData(bids_df['price'], bids_df['cumulative_size'])
    curve_asks.setData(asks_df['price'], asks_df['cumulative_size'])

    # Update the title
    title_text = f'Current Price: {current_price:.2f} | Bid Volume: {bid_size:.2f} | Ask Volume: {ask_size:.2f}'
    title.setText(title_text)
    title.setAttr('size', '12pt')

    # center the title
    title.anchor((0.5, 0.5), (0.5, 0.5))

worker.data_fetched.connect(on_data_fetched)
worker.moveToThread(thread)
thread.started.connect(worker.run)
thread.start()

win.show()
app.exec_()