// src/exchange.cpp
#include "exchange.h"
#include <curl/curl.h>
#include <iostream>

std::string Exchange::http_get(std::string url) {
    std::cout << "Fetching URL: " << url << std::endl;
    CURL* curl;
    CURLcode res;
    std::string readBuffer;

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        
        // Disable SSL verification (not recommended for production)
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
        
        // Timeout options
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10L);
        curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT, 5L);
        
        // Add User-Agent header
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "Mozilla/5.0");
        
        char errbuf[CURL_ERROR_SIZE];
        curl_easy_setopt(curl, CURLOPT_ERRORBUFFER, errbuf);
        
        res = curl_easy_perform(curl);
        if(res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n%s\n", 
                    curl_easy_strerror(res), errbuf);
        } else {
            long response_code;
            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
            std::cout << "HTTP Response code: " << response_code << std::endl;
        }
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();

    std::cout << "Response length: " << readBuffer.length() << std::endl;
    if(readBuffer.length() < 1000) {  // Only print if response is not too long
        std::cout << "Response: " << readBuffer << std::endl;
    }
    return readBuffer;
}


size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* userp) {
    size_t totalSize = size * nmemb;
    userp->append((char*)contents, totalSize);
    return totalSize;
}
