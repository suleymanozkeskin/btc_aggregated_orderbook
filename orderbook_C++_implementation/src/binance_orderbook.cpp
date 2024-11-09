// src/binance_orderbook.cpp
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include "../lib/json.hpp"
#include <curl/curl.h>
#include "binance_orderbook.h"

using json = nlohmann::json;
using namespace std;

Binance::Binance(string name, string api_url) : Exchange(name, api_url) {}

vector<vector<string>> Binance::fetch_orderbook() {
    string response = http_get(api_url + "api/v3/depth?symbol=BTCUSDT&limit=1000");
    
    if(response.empty()) {
        cerr << "Error: Empty response from Binance API" << endl;
        return {};
    }

    try {
        json data = json::parse(response);
        vector<vector<string>> bids, asks;
        for (auto& item : data["bids"]) {
            bids.push_back({item[0].get<string>(), item[1].get<string>(), "buy"});
        }
        for (auto& item : data["asks"]) {
            asks.push_back({item[0].get<string>(), item[1].get<string>(), "sell"});
        }
        bids.insert(bids.end(), asks.begin(), asks.end());
        return bids;
    } catch (const json::parse_error& e) {
        cerr << "JSON parse error: " << e.what() << '\n';
        cerr << "Response was: " << response << '\n';
        return {};
    } catch (const exception& e) {
        cerr << "Error: " << e.what() << '\n';
        return {};
    }
}
