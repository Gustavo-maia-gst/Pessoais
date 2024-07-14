cmake_minimum_required(VERSION 3.27)
project(LogDB)

set(CMAKE_CXX_STANDARD 23)

add_executable(LogDB main.cpp
        log/LogModel.cpp
        log/LogModel.h
        models/Pessoa.cpp
        models/Pessoa.h
        segments/SegmentFile.cpp
        segments/SegmentFile.h
        segments/SegmentManager.h
        log/LogRepository.h
)
