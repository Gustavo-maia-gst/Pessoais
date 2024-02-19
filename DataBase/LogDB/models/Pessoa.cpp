//
// Created by Gustavo on 18/02/2024.
//

#include "Pessoa.h"

Pessoa::Pessoa() = default;

Pessoa::Pessoa(long id, const std::string &name, int age) {
    this->id = id;
    this->name = name;
    this->age = age;
}

size_t Pessoa::getTotalSize() {
    size_t totalSize = 0;

    totalSize += sizeof(long);                      // Size of id
    totalSize += sizeof(size_t);                    // Size of the string
    totalSize += sizeof(int);                       // Size of the age

    return totalSize;
}

char* Pessoa::serialize(char **buff) {
    char *start = *buff;

    LogModel::serializeValue<long>(buff, this->id);
    LogModel::serializeString(buff, this->name, this->nameSize);
    LogModel::serializeValue<int>(buff, this->age);

    return start;
}

char* Pessoa::deserialize(char **buff) {
    char *start = *buff;

    LogModel::deserializeValue<long>(buff, this->id);
    LogModel::deserializeString(buff, this->name, this->nameSize);
    LogModel::deserializeValue<int>(buff, this->age);

    return start;
}
