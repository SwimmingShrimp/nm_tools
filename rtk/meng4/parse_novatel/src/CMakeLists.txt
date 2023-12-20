cmake_minimum_required(VERSION 3.5)

set(SOURCES
  ./novatel/novatel.cpp
  ./main.cc

)

set(CMAKE_CXX_STANDARD 11)

ADD_EXECUTABLE(parse_novatel ${SOURCES})
