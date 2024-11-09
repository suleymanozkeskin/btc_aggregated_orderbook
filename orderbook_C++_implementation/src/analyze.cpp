#include "analyze.h"
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <iomanip>
#include <cmath>
#include <algorithm>
#include <sstream>

using namespace std;

// Function implementations
void plot_orderbook_depth(const vector<vector<string>>& orderbook, int plot_height, int plot_width) {
    // Separate bids and asks
    map<double, double> bids_map, asks_map;
    double min_price = stod(orderbook[0][0]);
    double max_price = min_price;
    
    for (const auto& row : orderbook) {
        double price = stod(row[0]);
        double size = stod(row[1]);
        string side = row[2];
        
        min_price = min(min_price, price);
        max_price = max(max_price, price);
        
        if (side == "buy") {
            bids_map[price] += size;
        } else {
            asks_map[price] += size;
        }
    }

    // Calculate cumulative sizes
    vector<pair<double, double>> bids, asks;
    double cum_size = 0;
    
    // Cumulative bids (from highest to lowest)
    for (auto it = bids_map.rbegin(); it != bids_map.rend(); ++it) {
        cum_size += it->second;
        bids.push_back({it->first, cum_size});
    }
    
    // Cumulative asks (from lowest to highest)
    cum_size = 0;
    for (auto it = asks_map.begin(); it != asks_map.end(); ++it) {
        cum_size += it->second;
        asks.push_back({it->first, cum_size});
    }

    // Find maximum cumulative size for scaling
    double max_cum_size = 0;
    if (!bids.empty()) max_cum_size = max(max_cum_size, bids.back().second);
    if (!asks.empty()) max_cum_size = max(max_cum_size, asks.back().second);

    // Print the plot
    cout << "\nOrderbook Depth Chart (cumulative):\n";
    cout << string(plot_width + 10, '-') << endl;

    // Plot rows
    for (int i = 0; i < plot_height; ++i) {
        double size_threshold = max_cum_size * (plot_height - i - 1) / plot_height;
        
        // Print size scale
        cout << fixed << setprecision(2) << setw(8) << size_threshold << " |";
        
        // Find bid/ask positions for this row
        string row(plot_width, ' ');
        
        // Plot bids (left side, using '#')
        for (const auto& bid : bids) {
            if (bid.second >= size_threshold) {
                int pos = plot_width/2 - (int)((max_price - bid.first) / (max_price - min_price) * (plot_width/2));
                pos = max(0, min(plot_width-1, pos));
                row[pos] = '#';
            }
        }
        
        // Plot asks (right side, using '@')
        for (const auto& ask : asks) {
            if (ask.second >= size_threshold) {
                int pos = plot_width/2 + (int)((ask.first - min_price) / (max_price - min_price) * (plot_width/2));
                pos = max(0, min(plot_width-1, pos));
                row[pos] = '@';
            }
        }
        
        cout << row << endl;
    }
    
    // Print price scale
    cout << string(9, ' ');
    cout << string(plot_width, '-') << endl;
    cout << setw(9) << " " << fixed << setprecision(1) << min_price;
    cout << string(plot_width/2 - 12, ' ') << "Price";
    cout << string(plot_width/2 - 12, ' ') << max_price << endl;
    
    // Print legend
    cout << "\nLegend: # = Bids, @ = Asks\n";
}

void print_orderbook_stats(const vector<vector<string>>& orderbook) {
    double total_bid_size = 0;
    double total_ask_size = 0;
    double bid_volume = 0;
    double ask_volume = 0;
    double highest_bid = -1;
    double lowest_ask = -1;
    
    for (const auto& row : orderbook) {
        double price = stod(row[0]);
        double size = stod(row[1]);
        string side = row[2];
        
        if (side == "buy") {
            total_bid_size += size;
            bid_volume += price * size;
            highest_bid = max(highest_bid, price);
        } else {
            total_ask_size += size;
            ask_volume += price * size;
            lowest_ask = (lowest_ask < 0) ? price : min(lowest_ask, price);
        }
    }
    
    // Helper function to format numbers with commas
    auto format_with_commas = [](double value, int precision = 2) -> string {
        ostringstream ss;
        ss << fixed << setprecision(precision);
        ss << value;
        string str = ss.str();
        int pos = str.find('.');
        if (pos == string::npos) pos = str.length();
        while (pos > 3) {
            pos -= 3;
            str.insert(pos, ",");
        }
        return str;
    };
    
    cout << "\nOrderbook Statistics:\n";
    cout << string(50, '-') << endl;
    cout << fixed << setprecision(2);
    cout << "Highest Bid: $" << format_with_commas(highest_bid) << endl;
    cout << "Lowest Ask:  $" << format_with_commas(lowest_ask) << endl;
    cout << "Spread:      $" << format_with_commas(lowest_ask - highest_bid) << endl;
    cout << "Spread %:    " << ((lowest_ask - highest_bid) / lowest_ask * 100) << "%" << endl;
    cout << "\nBid Side:\n";
    cout << "- Total Size:  " << format_with_commas(total_bid_size, 8) << " BTC" << endl;
    cout << "- Total Value: $" << format_with_commas(bid_volume) << " USD" << endl;
    cout << "\nAsk Side:\n";
    cout << "- Total Size:  " << format_with_commas(total_ask_size, 8) << " BTC" << endl;
    cout << "- Total Value: $" << format_with_commas(ask_volume) << " USD" << endl;
}

void print_orderbook(const vector<vector<string>>& orderbook) {
    // Column headers
    const vector<string> headers = {"Price", "Size", "Side"};
    
    // Determine maximum width for each column including headers
    vector<size_t> col_widths(headers.size());
    for (size_t i = 0; i < headers.size(); i++) {
        col_widths[i] = headers[i].length();
    }

    // Find maximum width needed for each column from data
    for (const auto& row : orderbook) {
        for (size_t i = 0; i < row.size(); i++) {
            // For price, format with 2 decimal places
            if (i == 0) {
                ostringstream ss;
                ss << fixed << setprecision(2) << stod(row[i]);
                col_widths[i] = max(col_widths[i], ss.str().length());
            }
            // For size, format with 8 decimal places
            else if (i == 1) {
                ostringstream ss;
                ss << fixed << setprecision(8) << stod(row[i]);
                col_widths[i] = max(col_widths[i], ss.str().length());
            }
            else {
                col_widths[i] = max(col_widths[i], row[i].length());
            }
        }
    }

    // Print top border
    cout << "+";
    for (size_t i = 0; i < col_widths.size(); i++) {
        cout << string(col_widths[i] + 2, '-');
        cout << (i < col_widths.size() - 1 ? "+" : "+");
    }
    cout << "\n";

    // Print headers
    cout << "|";
    for (size_t i = 0; i < headers.size(); i++) {
        cout << " " << left << setw(col_widths[i]) << headers[i] << " |";
    }
    cout << "\n";

    // Print separator
    cout << "+";
    for (size_t i = 0; i < col_widths.size(); i++) {
        cout << string(col_widths[i] + 2, '-');
        cout << (i < col_widths.size() - 1 ? "+" : "+");
    }
    cout << "\n";

    // Print data rows
    for (const auto& row : orderbook) {
        cout << "|";
        for (size_t i = 0; i < row.size(); i++) {
            cout << " ";
            if (i == 0) {
                // Price column with 2 decimal places
                cout << fixed << setprecision(2) 
                     << setw(col_widths[i]) << stod(row[i]);
            }
            else if (i == 1) {
                // Size column with 8 decimal places
                cout << fixed << setprecision(8) 
                     << setw(col_widths[i]) << stod(row[i]);
            }
            else {
                cout << left << setw(col_widths[i]) << row[i];
            }
            cout << " |";
        }
        cout << "\n";
    }

    // Print bottom border
    cout << "+";
    for (size_t i = 0; i < col_widths.size(); i++) {
        cout << string(col_widths[i] + 2, '-');
        cout << (i < col_widths.size() - 1 ? "+" : "+");
    }
    cout << "\n";
}
