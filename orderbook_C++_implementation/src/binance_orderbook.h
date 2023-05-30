// src/binance_orderbook.h
#pragma once

#include "exchange.h"
#include <vector>
#include <string>

class Binance : public Exchange {
public:
    Binance(std::string name, std::string api_url);
    std::vector<std::vector<std::string>> fetch_orderbook() override;
};
