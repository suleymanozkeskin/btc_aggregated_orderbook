// src/main.cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include "bybit_orderbook.h"
#include "okex_orderbook.h"
#include "binance_orderbook.h"

using namespace std;

// Forward declaration of print_orderbook
void print_orderbook(const vector<vector<string>>& orderbook);

int main() {
    Bybit bybit("Bybit", "https://api.bybit.com/");
    OKEx okex("OKEx", "https://www.okex.com/");
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

    return 0;
}

void print_orderbook(const vector<vector<string>>& orderbook) {
    for (const auto& row : orderbook) {
        cout << "Price: " << row[0] << ", Size: " << row[1] << ", Side: " << row[2] << '\n';
    }
}

// under src/ directory:
// compile with: g++ -I../lib -o main main.cpp -lcurl
// execute with: ./main 