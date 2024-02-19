//
// Created by Gustavo on 17/02/2024.
//

#include "LogModel.h"

size_t LogModel::getTotalSize() { throw std::runtime_error("Not implemented"); }

void LogModel::serializeString(char **buff, const std::string& str, size_t stringSize) {
    if (str.size() >= stringSize) {
        throw std::range_error("String size greater than the limit");
    }
    std::memcpy(*buff, str.data(), str.size());
    *buff += str.size();
    *(++*buff) = '\0';
    *buff += stringSize - str.size() - 1;
}

void LogModel::deserializeString(char **buff, std::string& str, size_t stringSize) {
    str.resize(stringSize);
    memcpy(str.data(), *buff, stringSize);
    *buff += stringSize;
}
