// src/bybit_orderbook.cpp
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include "../lib/json.hpp"
#include <curl/curl.h>
#include "bybit_orderbook.h"

using json = nlohmann::json;
using namespace std;

Bybit::Bybit(string name, string api_url) : Exchange(name, api_url) {}

vector<vector<string>> Bybit::fetch_orderbook() {
    string response = http_get(api_url + "v5/market/orderbook?category=spot&symbol=BTCUSDT&limit=50");
    json data = json::parse(response);

    vector<vector<string>> bids, asks;
    for (auto& item : data["result"]["b"]) {
        bids.push_back({item[0].get<string>(), item[1].get<string>(), "buy"});
    }
    for (auto& item : data["result"]["a"]) {
        asks.push_back({item[0].get<string>(), item[1].get<string>(), "sell"});
    }
    bids.insert(bids.end(), asks.begin(), asks.end());
    return bids;
}
