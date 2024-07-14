#include <iostream>
#include "models/Pessoa.h"
#include "log/LogRepository.h"
#include "segments/SegmentManager.h"

int main() {
    Pessoa g(1, "G", 5);
    Pessoa gu(2, "Gu", 7);
    Pessoa gus(3, "Gus", 10);
    Pessoa gust(4, "Gust", 12);
    Pessoa gusta(5, "Gusta", 14);
    Pessoa gustav(6, "Gustav", 16);
    Pessoa gustavo(7, "Gustavo", 18);

    auto repo = new LogRepository<Pessoa>();

    repo->insertModel(g);
    repo->insertModel(gu);
    repo->insertModel(gus);
    repo->insertModel(gust);
    repo->insertModel(gusta);
    repo->insertModel(gustav);
    repo->insertModel(gustavo);

    return 0;
}