//
// Created by Gustavo on 18/02/2024.
//

#include "SegmentFile.h"

SegmentFile::SegmentFile(std::string& modelName, size_t totalSize) {
    this->fileName = modelName + ".gm";
    this->writer = std::make_unique<std::ofstream>(fileName);
    this->reader = std::make_unique<std::ifstream>(fileName);
    this->objectSize = static_cast<long long>(totalSize);
}

std::streampos SegmentFile::insert(LogModel& model) {
    char arr[this->objectSize];
    char *buff = &arr[0];
    buff = model.serialize(&buff);
    std::streampos pos = writer->tellp();
    this->writer->write(buff, this->objectSize);
    this->writer->flush();
    return pos;
}

void SegmentFile::read(LogModel& model, std::streampos pos) {
    this->reader->seekg(pos, std::ios::beg);
    char arr[this->objectSize];
    char *buff = &arr[0];
    reader->read(arr, this->objectSize);
    model.deserialize(&buff);
}

std::streampos SegmentFile::tell() {
    return this->writer->tellp();
}

void SegmentFile::remove() {
    this->reader->close();
    this->writer->close();
    std::remove(this->fileName.c_str());
}