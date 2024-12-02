cmake_minimum_required(VERSION 3.10)

# 设置项目名称
project(CMakeProject1)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 14)

# 设置 OpenCV 的包含路径
include_directories("C:/D/opencv/build/include")

# 设置 OpenCV 的库文件路径
link_directories("C:/D/opencv/build/x64/vc16/lib")

# 添加源文件
add_executable(CMakeProject1 CMakeProject1.cpp)  # 请根据需要添加实际源文件

# 链接 OpenCV 库
target_link_libraries(${PROJECT_NAME} opencv_world4100d)

# 如果需要，设置调试模式的库链接
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    target_link_libraries(${PROJECT_NAME} opencv_world4100d)
else()
    target_link_libraries(${PROJECT_NAME} opencv_world4100)
endif()
