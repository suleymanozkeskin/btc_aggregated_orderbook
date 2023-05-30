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
    data_fetched = QtCore.pyqtSignal(pd.DataFrame, float)

    def run(self):
        while True:
            # Execute the main.py script to update the CSV data
            subprocess.run(['python3', 'main.py'])

            # Get the current BTC price from binance
            response = requests.get('https://api.binance.com/api/v3/ticker/price', params={'symbol': 'BTCUSDT'})
            current_price = float(response.json()['price'])

            # Load the updated orderbook data from the CSV file
            orderbook = pd.read_csv('orderbook.csv')

            # Calculate cumulative sums for buy and sell sides
            orderbook['Buy'] = orderbook[orderbook['Side'] == 'buy']['Size'].cumsum()
            orderbook['Sell'] = orderbook[orderbook['Side'] == 'sell']['Size'].cumsum()

            self.data_fetched.emit(orderbook, current_price)

            # Wait for the specified delay before the next iteration
            time.sleep(delay)


app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(title="Aggregated Orderbook BTC/USD")
plot = win.addPlot()
plot.setLabel('left', 'Cumulative Size')
plot.setLabel('bottom', 'Price')

curve_buy = plot.plot(pen='g')  # green pen for buy
curve_sell = plot.plot(pen='r')  # red pen for sell

title = pg.LabelItem(justify='right')
win.addItem(title)

worker = Worker()
thread = QtCore.QThread()

def on_data_fetched(orderbook, current_price):
    # Analyze the buy and sell sides within the price range
    price_min = current_price - price_range
    price_max = current_price + price_range
    buy_size = orderbook[(orderbook['Price'] >= price_min) & (orderbook['Price'] <= price_max) & (orderbook['Side'] == 'buy')]['Size'].sum()
    sell_size = orderbook[(orderbook['Price'] >= price_min) & (orderbook['Price'] <= price_max) & (orderbook['Side'] == 'sell')]['Size'].sum()

    # Update the plots
    curve_buy.setData(orderbook['Price'], orderbook['Buy'])
    curve_sell.setData(orderbook['Price'], orderbook['Sell'])

    # Update the title
    title_text = f'Current Price: {current_price:.2f} | Buy Size: {buy_size:.2f} | Sell Size: {sell_size:.2f}'
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

