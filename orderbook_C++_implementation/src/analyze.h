#pragma once

#include <vector>
#include <string>

// Function declarations
void print_orderbook(const std::vector<std::vector<std::string>>& orderbook);
void plot_orderbook_depth(const std::vector<std::vector<std::string>>& orderbook, int plot_height = 20, int plot_width = 80);
void print_orderbook_stats(const std::vector<std::vector<std::string>>& orderbook); 