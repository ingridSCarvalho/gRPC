cmake_minimum_required(VERSION 3.16)
project(DictionaryServer)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Encontre as dependências Protobuf e gRPC
find_package(Protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)


# Diretórios de include
include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${Protobuf_INCLUDE_DIRS})

# Adicione o executável do servidor
add_executable(server
    server/main.cpp
    server/dictionary.grpc.pb.cc
    server/dictionary.pb.cc
)

# Link com bibliotecas gRPC e Protobuf
target_link_libraries(server
    gRPC::grpc++
    gRPC::grpc++_reflection
    protobuf::libprotobuf
)

# Opcional: Definir flags de compilação
target_compile_options(server
    PRIVATE
    -Wall
    -Wextra
    -Wpedantic
)