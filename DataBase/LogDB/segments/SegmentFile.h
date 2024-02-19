//
// Created by Gustavo on 18/02/2024.
//

#ifndef LOGDB_SEGMENTFILE_H
#define LOGDB_SEGMENTFILE_H

#include <fstream>
#include <typeinfo>
#include <memory>
#include "../log/LogModel.h"


class SegmentFile {
public:
    explicit SegmentFile(std::string& modelName, size_t totalSize);
    std::streampos insert(LogModel& model);
    void read(LogModel& model, std::streampos pos);
    std::streampos tell();
    void remove();

protected:
    long long objectSize;
    std::string fileName;
    std::unique_ptr<std::ofstream> writer;
    std::unique_ptr<std::ifstream> reader;
};


#endif //LOGDB_SEGMENTFILE_H
