# BTC Aggregated Orderbook

BTC Aggregated Orderbook repository contains C++ and Python implementation which fetches orderbook data from multiple cryptocurrency exchanges, aggregates the data, and visualizes the cumulative size of buy and sell orders over time.

## Features

- Fetches orderbook data from multiple exchanges (Bybit, OKEx, Binance, etc.)
- Aggregates the orderbook data into a single orderbook

## Prerequisites

- Python 3.x
- Pandas library
- Matplotlib library
- Requests library
- PyQT5 library (for visualization)
- C++ compiler (for C++ implementation)

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

The analyze scripts will continuously update the plot and display the current price and side with more cumulative size within a specific price range.

## C++ Implementation

To run the C++ implementation, follow these steps:

1. Compile the code using the following command:

    g++ -std=c++17 -I../lib -o main main.cpp exchange.cpp bybit_orderbook.cpp okex_orderbook.cpp binance_orderbook.cpp analyze.cpp -lcurl

2. Run the compiled program:

    ./main

3. Cli output screenshot:

    ![cli-stats](/cli-stats.png)

## Contributions

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Authors

- Suleyman Ozkeskin - [suleymanozkeskin.com](https://suleymanozkeskin.com)
- Egehan Usluer - (<https://github.com/EgehanU>)

## Known Issues

OKEx and Coinbase are not working currently.

## License

This project is licensed under the MIT License.
