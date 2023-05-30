#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include "../lib/json.hpp"
#include <curl/curl.h>
#include "okex_orderbook.h"

using json = nlohmann::json;
using namespace std;

OKEx::OKEx(string name, string api_url) : Exchange(name, api_url) {}

vector<vector<string>> OKEx::fetch_orderbook() {
    string response = http_get(api_url + "api/v5/market/books?instId=BTC-USDT&sz=400");
    json data = json::parse(response);

    if(data["code"] == "0") {
        vector<vector<string>> bids, asks;
        for (auto& item : data["data"][0]["bids"]) {
            bids.push_back({item[0].get<string>(), item[1].get<string>(), "buy"});
        }
        for (auto& item : data["data"][0]["asks"]) {
            asks.push_back({item[0].get<string>(), item[1].get<string>(), "sell"});
        }
        bids.insert(bids.end(), asks.begin(), asks.end());
        return bids;
    } else {
        cerr << "Error fetching orderbook: " << data["msg"].get<string>() << '\n';
        return {};
    }
}
