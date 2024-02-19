//
// Created by Gustavo on 17/02/2024.
//
#ifndef LOGDB_LOGMODEL_H
#define LOGDB_LOGMODEL_H

#include <fstream>
#include <cstring>


class LogModel {
public:
    long id = 0;

    virtual char* serialize(char **buff) = 0;
    virtual char* deserialize(char **buff) = 0;
    static size_t getTotalSize();

protected:
    static void serializeString(char **buff, const std::string& str, size_t stringSize);
    static void deserializeString(char **buff, std::string& str, size_t stringSize);

    template<typename T>
    static void serializeValue(char **buff, const T& value) {
        const char *bytes = reinterpret_cast<const char*>(&value);
        std::memcpy(*buff, bytes, sizeof(T));
        *buff += sizeof(T);
    }

    template<typename T>
    static void deserializeValue(char **buff, T& value) {
        T readen;
        std::memcpy(reinterpret_cast<char*>(&readen), *buff, sizeof(T));
        *buff += sizeof(T);
        value = readen;
    }
};


#endif //LOGDB_LOGMODEL_H
