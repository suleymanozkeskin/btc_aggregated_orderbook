#pragma once

#include "exchange.h"
#include <vector>
#include <string>

class OKEx : public Exchange {
public:
    OKEx(std::string name, std::string api_url);
    std::vector<std::vector<std::string>> fetch_orderbook() override;
};
