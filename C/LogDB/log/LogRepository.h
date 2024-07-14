//
// Created by Gustavo on 18/02/2024.
//

#ifndef LOGDB_LOGREPOSITORY_H
#define LOGDB_LOGREPOSITORY_H

#include "../segments/SegmentManager.h"

template<class TModel>
class LogRepository {
public:
    LogRepository() {
        TModel model;
        this->manager = new SegmentManager(model);
    }

    void insertModel(TModel model) {
        if (this->map.count(model.id))
            throw std::domain_error("Model already are in the database");

        std::streampos pos = this->manager->insert(model, map);
        this->map[model.id] = pos;
    }

    TModel getModel(long id) {
        if (!this->map.contains(id) || this->map[id] == -1)
            throw std::domain_error("Model with id " + std::to_string(id) + " not present in the database");

        return this->manager->get(id, map);
    }

    void updateModel(TModel model) {
        if (!this->map.contains(model.id))
            throw std::domain_error("Model aren't in the database");

        std::streampos pos = this->manager->insert(model, map);
        this->map[model.id] = pos;
    }

    void deleteModel(long id) {
        this->map[id] = -1;
    }

    void deleteModel(TModel model) {
        this->deleteModel(model.id);
    }

private:
    SegmentManager<TModel>* manager;
    std::unordered_map<long, std::streampos> map;
};


#endif //LOGDB_LOGREPOSITORY_H
