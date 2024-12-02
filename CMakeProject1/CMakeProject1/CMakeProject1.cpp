// CMakeProject1.cpp: 定义应用程序的入口点。
//

#include "CMakeProject1.h"


using namespace std;
using namespace cv;

// BGR到YUV I420格式转换
cv::Mat BGR2YUV_I420(const cv::Mat& bgr_image) {
    int width = bgr_image.cols;
    int height = bgr_image.rows;

    // 创建 YUV I420 格式的 cv::Mat
    cv::Mat yuv_image(height + height / 2, width, CV_8UC1);  // 一张单通道图像，行数 = 高度 + 高度/2，列数 = 宽度

    // 获取 Y、U、V 平面指针
    unsigned char* y_plane = yuv_image.data;                      // Y平面
    unsigned char* u_plane = y_plane + width * height;            // U平面
    unsigned char* v_plane = u_plane + (width / 2) * (height / 2); // V平面

    // 遍历每个像素并转换
    int y_index = 0;
    int u_index = 0;
    int v_index = 0;

    for (int i = 0; i < height; ++i) {
        for (int j = 0; j < width; ++j) {
            // 获取当前 BGR 像素
            cv::Vec3b pixel = bgr_image.at<cv::Vec3b>(i, j);
            unsigned char b = pixel[0];
            unsigned char g = pixel[1];
            unsigned char r = pixel[2];

            // YUV 转换公式
            unsigned char y = (unsigned char)(0.299 * r + 0.587 * g + 0.114 * b);
            unsigned char u = (unsigned char)(-0.147 * r - 0.289 * g + 0.436 * b + 128); // 加上偏移
            unsigned char v = (unsigned char)(0.615 * r - 0.515 * g - 0.100 * b + 128); // 加上偏移

            // 将 Y 值存入 Y平面
            y_plane[y_index++] = y;

            // U 和 V 值存入 U 平面和 V 平面（在 4:2:0 子采样中，每 4 个 Y 像素共享一个 U 和一个 V）
            if (i % 2 == 0 && j % 2 == 0) {  // 只处理偶数行列的 U 和 V 值
                u_plane[u_index++] = u;
                v_plane[v_index++] = v;
            }
        }
    }

    return yuv_image;
}

// RGB -> NV12
void rgb_to_nv12(const std::string& input_file, const std::string& output_file) {
    // 读取输入图像
    Mat image = imread(input_file);

    if (image.empty()) {
        std::cerr << "Error: Could not open or find the image!" << std::endl;
        return;
    }
    int width = image.cols;
    int height = image.rows;

    // 转换为YUV格式
    Mat yuv_image = BGR2YUV_I420(image);

    // 将YUV格式转换为NV12格式
    std::vector<unsigned char> y_plane(width * height);
    std::vector<unsigned char> uv_plane(width * height / 2);

    int y_index = 0;
    for (int i = 0; i < height; ++i) {
        for (int j = 0; j < width; ++j) {
            unsigned char y = yuv_image.at<unsigned char>(i, j);
            y_plane[y_index++] = y;
        }
    }

    int uv_index = 0;
    for (int i = 0; i < height / 2; ++i) {
        for (int j = 0; j < width / 2; ++j) {
            unsigned char u = yuv_image.at<unsigned char>(height + i, j * 2);
            unsigned char v = yuv_image.at<unsigned char>(height + i, j * 2 + 1);
            uv_plane[uv_index++] = u;
            uv_plane[uv_index++] = v;
        }
    }

    // 保存NV12格式到文件
    std::ofstream out(output_file, std::ios::binary);
    out.write(reinterpret_cast<char*>(y_plane.data()), y_plane.size());
    out.write(reinterpret_cast<char*>(uv_plane.data()), uv_plane.size());
    out.close();
}

// YUV -> BGR (NV12格式)
void YUV2BGR_NV12(const cv::Mat& yuv_image, cv::Mat& bgr_image) {
    int width = bgr_image.cols;
    int height = bgr_image.rows;

    // 获取 Y 和 UV 平面
    unsigned char* y_plane = yuv_image.data;                       // Y平面
    unsigned char* uv_plane = y_plane + width * height;            // UV平面

    bgr_image.create(height, width, CV_8UC3);  // BGR 图像，大小为高*宽，3通道

    // 遍历每个像素并转换
    for (int i = 0; i < height; ++i) {
        for (int j = 0; j < width; ++j) {
            // 获取 Y 值
            unsigned char y = y_plane[i * width + j];

            // 获取 UV 值（UV平面为每 4 个像素共享一个 U 和 V）
            int uv_index = ((i / 2) * (width / 2)) + (j / 2) * 2;
            unsigned char u = uv_plane[uv_index];
            unsigned char v = uv_plane[uv_index + 1];

            // YUV 转换为 RGB
            float r = y + 1.402 * (v - 128);
            float g = y - 0.344136 * (u - 128) - 0.714136 * (v - 128);
            float b = y + 1.772 * (u - 128);

            // 将 RGB 转换为 BGR（OpenCV 默认使用 BGR 格式）
            bgr_image.at<cv::Vec3b>(i, j)[0] = (unsigned char)std::min(std::max(b, 0.0f), 255.0f);
            bgr_image.at<cv::Vec3b>(i, j)[1] = (unsigned char)std::min(std::max(g, 0.0f), 255.0f);
            bgr_image.at<cv::Vec3b>(i, j)[2] = (unsigned char)std::min(std::max(r, 0.0f), 255.0f);
        }
    }
}

// NV12 -> RGB
void nv12_to_rgb(const std::string& input_file, const std::string& output_file, int width, int height) {
    // 读取NV12数据
    std::ifstream in(input_file, std::ios::binary);

    std::vector<unsigned char> y_plane(width * height);
    std::vector<unsigned char> uv_plane(width * height / 2);

    in.read(reinterpret_cast<char*>(y_plane.data()), y_plane.size());
    in.read(reinterpret_cast<char*>(uv_plane.data()), uv_plane.size());
    in.close();

    // 构建完整的YUV格式
    std::vector<unsigned char> yuv_data(width * height * 3 / 2);
    std::copy(y_plane.begin(), y_plane.end(), yuv_data.begin());
    std::copy(uv_plane.begin(), uv_plane.end(), yuv_data.begin() + y_plane.size());

    // 转换为OpenCV的Mat对象
    cv::Mat yuv_image(height + height / 2, width, CV_8UC1, yuv_data.data());

    // 转换为BGR格式
    cv::Mat bgr_image(height, width, CV_8UC3);
    YUV2BGR_NV12(yuv_image, bgr_image);

    // 保存为JPG文件
    cv::imwrite(output_file, bgr_image);
}

int main() {

    std::string input_file = "pic1.jpg";
    std::string nv12_file = "test1_nv12.yuv";
    std::string output_file = "test1_reconstructed.jpg";


    auto start = chrono::high_resolution_clock::now();


    // RGB -> NV12
    rgb_to_nv12(input_file, nv12_file);

    // NV12 -> RGB
    int width = 640;  // 图像宽度
    int height = 480; // 图像高度
    nv12_to_rgb(nv12_file, output_file, width, height);
    auto end = chrono::high_resolution_clock::now();

    chrono::duration<double> duration = end - start;
    double time_taken = duration.count();

    double fps = 1.0 / time_taken;  // 帧率，单位：帧每秒


    cout << "Time taken to process one image: " << time_taken << " seconds" << endl;
    cout << "Frame rate: " << fps << " FPS" << endl;

    return 0;
}
