#include "../lib/json.hpp"
#include "../lib/csv.hpp"
#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <string>
#include <algorithm>
#include <unistd.h> 
#include <curlpp/cURLpp.hpp>
#include <curlpp/Easy.hpp>
#include <curlpp/Options.hpp>



struct OrderBook {
    double Price;
    double Size;
    std::string Side;
};

double get_current_btc_price() {
    // Use curlpp to perform a GET request to Binance API
    curlpp::Easy request;
    request.setOpt<curlpp::Options::Url>("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT");
    std::ostringstream response_stream;
    request.setOpt<curlpp::Options::WriteStream>(&response_stream);
    request.perform();

    // Use nlohmann::json to parse the JSON response
    nlohmann::json response_json = nlohmann::json::parse(response_stream.str());
    return response_json["price"].get<double>();
}

std::vector<OrderBook> parse_orderbook_csv(const std::string& filename) {
    std::vector<OrderBook> orderbook;
    csv::CSVReader reader(filename);
    for (csv::CSVRow& row : reader) {
        OrderBook entry;
        entry.Price = row["Price"].get<double>();
        entry.Size = row["Size"].get<double>();
        entry.Side = row["Side"].get<>();
        orderbook.push_back(entry);
    }
    return orderbook;
}

