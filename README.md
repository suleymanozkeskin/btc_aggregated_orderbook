# BTC Aggregated Orderbook

BTC Aggregated Orderbook is a Python script that fetches orderbook data from multiple cryptocurrency exchanges, aggregates the data, and visualizes the cumulative size of buy and sell orders over time.

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
- Bybit API key (optional, for Bybit exchange)
- Coinbase API key (optional, for Coinbase exchange)
- OKEx API key (optional, for OKEx exchange)
- Binance API key (optional, for Binance exchange)

## Installation

1. Clone the repository:

    git clone <https://github.com/suleymanozkeskin/btc_aggregated_orderbook.git>

2. Install the required libraries:

    pip install pandas matplotlib requests

## Usage

1. Run the `main.py` script to fetch orderbook data from the exchanges and save it to a CSV file:

    python main.py

2. Run the `analyze.py` script to visualize the cumulative size of buy and sell orders over time:

    python analyze.py

The script will continuously update the plot and display the current price and side with more cumulative size within a specific price range.

## Contributions

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
