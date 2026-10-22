cmake_minimum_required(VERSION 4.3)

set(CMAKE_EXPERIMENTAL_CXX_IMPORT_STD "451f2fe2-a8a2-47c3-bc32-94786d8fc91b")

project(MatrixLab LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_SCAN_FOR_MODULES ON)
set(CMAKE_CXX_MODULE_STD ON)

add_executable(matrix_mul)

target_sources(matrix_mul PRIVATE
    cpp/main.cpp
)

target_sources(matrix_mul
    PUBLIC FILE_SET CXX_MODULES FILES
        cpp/matrix_io.cppm
        cpp/matrix_ops.cppm
)
