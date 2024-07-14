//
// Created by Gustavo on 18/02/2024.
//

#ifndef LOGDB_PESSOA_H
#define LOGDB_PESSOA_H

#include "../log/LogModel.h"

class Pessoa : public LogModel {
public:
    std::string name;
    int age = 0;

    Pessoa();
    Pessoa(long id, const std::string& name, int age);
    static size_t getTotalSize();
    char* serialize(char **buff) override;
    char* deserialize(char **buff) override;

private:
    size_t nameSize = 40;
};


#endif //LOGDB_PESSOA_H
