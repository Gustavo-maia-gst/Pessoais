//
// Created by Gustavo on 18/02/2024.
//

#ifndef LOGDB_SEGMENTMANAGER_H
#define LOGDB_SEGMENTMANAGER_H

#include "SegmentFile.h"
#include <unordered_map>


template<class TModel>
class SegmentManager {
public:
    explicit SegmentManager(TModel& model, long logLimit = 10) {
        this->logSize = 0;
        this->segmentId = 1;
        this->logLimit = logLimit;
        this->modelName = typeid(model).name();
        this->modelSize = model.getTotalSize();
        this->file = new SegmentFile(modelName, modelSize);
    }

    std::streampos insert(TModel& model, std::unordered_map<long, std::streampos>& map) {
        if (this->logSize >= logLimit)
            this->compactSegment(map);

        this->logSize++;
        return this->file->insert(model);
    }

    TModel get(long id, std::unordered_map<long, std::streampos>& map) {
        std::streampos pos = map[id];
        TModel model;
        this->file->read(model, pos);
        return model;
    }

private:
    size_t logSize;
    size_t logLimit;
    size_t modelSize;
    long segmentId;
    std::string modelName;
    SegmentFile* file;

    void compactSegment(std::unordered_map<long, std::streampos>& map) {
        std::string fileName = modelName + "_" + std::to_string(this->segmentId++);
        auto *newFile = new SegmentFile(fileName, modelSize);
        TModel model;
        for (auto p: map) {
            this->file->read(model, p.second);
            newFile->insert(model);
        }

        this->file->remove();
        this->file = newFile;
    }
};


#endif //LOGDB_SEGMENTMANAGER_H