#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include "../lib/json.hpp"
#include <curl/curl.h>

using json = nlohmann::json;
using namespace std;

// Forward declaration of WriteCallback
size_t WriteCallback(void* contents, size_t size, size_t nmemb, string* userp);

class Exchange {
public:
    Exchange(string name, string api_url) : name(name), api_url(api_url) {}
    virtual vector<vector<string>> fetch_orderbook() = 0;  // Pure virtual function

protected:
    string name;
    string api_url;
};

class Bybit : public Exchange {
public:
    Bybit(string name, string api_url) : Exchange(name, api_url) {}

    vector<vector<string>> fetch_orderbook() override {
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

private:
    string http_get(string url) {
        CURL* curl;
        CURLcode res;
        string readBuffer;

        curl_global_init(CURL_GLOBAL_DEFAULT);
        curl = curl_easy_init();
        if(curl) {
            curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
            res = curl_easy_perform(curl);
            if(res != CURLE_OK) {
                fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
            }
            curl_easy_cleanup(curl);
        }
        curl_global_cleanup();

        return readBuffer;
    }
};

// Definition of WriteCallback
size_t WriteCallback(void* contents, size_t size, size_t nmemb, string* userp) {
    size_t totalSize = size * nmemb;
    userp->append((char*)contents, totalSize);
    return totalSize;
}

int main() {
    Bybit bybit("Bybit", "https://api.bybit.com/");
    vector<vector<string>> orderbook = bybit.fetch_orderbook();

    // Print the orderbook
    for (const auto& row : orderbook) {
        for (const auto& cell : row) {
            cout << cell << ' ';
        }
        cout << '\n';
    }
}

// under src/ directory:
// compile with: g++ -I../lib -o bybit_orderbook bybit_orderbook.cpp -lcurl
// execute with: ./bybit_orderbook

// to benchmark the execution time:
// time ./bybit_orderbook