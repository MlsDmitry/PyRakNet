cmake_minimum_required(VERSION 3.19)

project(pyraknet)

find_package(PythonInterp)
find_package(PythonLibs)

set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_BUILD_TYPE DEBUG)


set(CMAKE_CXX_COMPILE_FEATURES "${CMAKE_C_COMPILE_FLAGS} -Wregister")

add_subdirectory(RakNet)

add_library(pyraknet MODULE RakNet/Source/pyraknet_wrap.cxx)
target_include_directories(pyraknet PRIVATE RakNet/Source ${PYTHON_INCLUDE_DIRS})
target_link_libraries(pyraknet RakNetDLL ${PYTHON_LIBRARIES})

set_target_properties(pyraknet PROPERTIES
    PREFIX "_"
)