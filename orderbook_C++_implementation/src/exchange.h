// src/exchange.h
#pragma once

#include <vector>
#include <string>
#include <curl/curl.h>

class Exchange {
public:
    Exchange(std::string name, std::string api_url) : name(name), api_url(api_url) {}
    virtual std::vector<std::vector<std::string>> fetch_orderbook() = 0;  // Pure virtual function
    std::string http_get(std::string url);
protected:
    std::string name;
    std::string api_url;
};

size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* userp);
