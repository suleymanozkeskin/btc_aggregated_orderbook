# BTC Aggregated Orderbook

BTC Aggregated Orderbook repository contains C++ and Python implementation which fetches orderbook data from multiple cryptocurrency exchanges, aggregates the data, and visualizes the cumulative size of buy and sell orders over time.

## Features

- Fetches orderbook data from multiple exchanges (Bybit, OKEx, Binance, etc.)
- Aggregates the orderbook data into a single DataFrame
- Calculates cumulative sums for buy and sell sides
- Dynamically updates and visualizes the cumulative size using Matplotlib
- Analyzes the current price and determines which side (buy or sell) has more cumulative size within a specific price range

## Prerequisites

- Python 3.x
- Pandas library
- Matplotlib library
- Requests library
- PyQT5 library (for visualization)
- Depending on your system, you may need some additional libraries for C++ implementation.

## Installation

1. Clone the repository:

    git clone <https://github.com/suleymanozkeskin/btc_aggregated_orderbook.git>

2. Install the required libraries:

    pip install pandas matplotlib requests pyqt5

## Usage

1. Run the `main.py` script to fetch orderbook data from the exchanges and save it to a CSV file:

    python main.py

2. Run the `analyze.py` script to visualize the cumulative size of buy and sell orders over time:

    python analyze.py

3. Alternatively, you can run analyze_PyQT.py to visualize the orderbook data using PyQT5:

    python analyze_PyQT.py

The script will continuously update the plot and display the current price and side with more cumulative size within a specific price range.

## Contributions

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Authors

- Suleyman Ozkeskin - [suleymanozkeskin.com](https://suleymanozkeskin.com)
- Egehan Usluer - (<https://github.com/EgehanU>)

## To Do

- [ ] Add more exchanges
- [ ] Add more features
- [ ] Add statistical analysis
- [ ] Depending on your needs, subscribe to the exchanges' websocket APIs to get real-time orderbook data instead of fetching it periodically.
- [ ] Currently, data is being saved to a CSV file and then read from it. This is not the most efficient way to do it. Instead, you can use a database to store the data and read it from there. Or, you can use the memory to store the data and read it from there. This might be a faster approach.
- [ ] Add a GUI to the C++ implementation for easier usage and visualization. Currently, the C++ implementation is only a console application and does not visualize the data as Python implementation does.

## License

This project is licensed under the MIT License.
