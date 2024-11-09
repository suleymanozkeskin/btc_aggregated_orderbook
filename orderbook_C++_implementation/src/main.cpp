// src/main.cpp
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
#include <fstream>
#include <map>
#include "bybit_orderbook.h"
#include "okex_orderbook.h"
#include "binance_orderbook.h"
#include "analyze.h"

using namespace std;

int main() {
    Bybit bybit("Bybit", "https://api.bybit.com/");
    OKEx okex("OKEx", "https://www.okx.com/");
    Binance binance("Binance", "https://api.binance.com/");

    // Fetch orderbook data
    vector<vector<string>> bybit_orderbook = bybit.fetch_orderbook();
    vector<vector<string>> okex_orderbook = okex.fetch_orderbook();
    vector<vector<string>> binance_orderbook = binance.fetch_orderbook();

    // Concatenate orderbooks
    vector<vector<string>> master_orderbook;
    if (!bybit_orderbook.empty())
        master_orderbook.insert(master_orderbook.end(), bybit_orderbook.begin(), bybit_orderbook.end());
    if (!okex_orderbook.empty())
        master_orderbook.insert(master_orderbook.end(), okex_orderbook.begin(), okex_orderbook.end());
    if (!binance_orderbook.empty())
        master_orderbook.insert(master_orderbook.end(), binance_orderbook.begin(), binance_orderbook.end());

    // Sort the orderbook by price (descending)
    sort(master_orderbook.begin(), master_orderbook.end(), [](vector<string> a, vector<string> b) {
        return stod(a[0]) > stod(b[0]);
    });

    // Save the orderbook to a csv file
    ofstream file("orderbook.csv");
    if (file.is_open()) {
        file << "Price,Size,Side\n";
        for (auto& row : master_orderbook) {
            double price = stod(row[0]);
            double size = stod(row[1]);
            string side = row[2];
            file << price << ',' << size << ',' << side << '\n';
        }
        file.close();
    } else {
        cerr << "Unable to open file";
        return 1;
    }

    // Print the orderbook
    print_orderbook(master_orderbook);

    // Print statistics and visualization
    print_orderbook_stats(master_orderbook);
    plot_orderbook_depth(master_orderbook);

    return 0;
}

// under src/ directory:
// execute with: ./main 