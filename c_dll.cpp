#include <iostream>
#include <algorithm>
#include <vector>
#include <math.h>
#include <string>
#include <opencv2/core.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <omp.h>
using namespace std;
using namespace cv;
class frameProcessing
{
    private:
        cv::Mat pythonSideMatData, input, result;
        int height, width, dataLength;
        void imageProcessing()
        {
            cv::cvtColor(input, result, cv::COLOR_BGR2GRAY);
            cv::cvtColor(result, result, cv::COLOR_GRAY2BGR);
        }
        void prepareOutputImage(void)
        {
            uchar* returnData = (uchar*)pythonSideMatData.data;
            uchar* resultData = (uchar*)result.data;
            dataLength = height * width * 3;
            #pragma omp parallel
            {
                for(int idx = 0 ; idx < dataLength ; idx++)
                {
                    returnData[idx] = resultData[idx];
                }
            }
        }
        void prepareInputImage(uint8_t *data)
        {
            pythonSideMatData = cv::Mat(height, width, CV_8UC3, data);
            input = pythonSideMatData.clone();
        }
    public:
        void startPoint(uint8_t *data, int _height, int _width)
        {
            height = _height;
            width = _width;
            prepareInputImage(data);
            cv::imshow("before_in_dll", input);
            imageProcessing();
            prepareOutputImage();
            cv::imshow("after_in_dll", pythonSideMatData);
            cv::waitKey(1);
            return;
        }
        frameProcessing(void)
        {
            cv::namedWindow("before_in_dll", cv::WINDOW_GUI_EXPANDED);
            cv::namedWindow("after_in_dll", cv::WINDOW_GUI_EXPANDED);
        }
        ~frameProcessing(void)
        {
            cv::destroyAllWindows();
        }
};
extern "C"
{
    using namespace std;
    using namespace cv;
    frameProcessing* frameProcessing_new() {return new frameProcessing();}
    void frameProcessing_startPoint(frameProcessing* frameprocessing, uint8_t *data, int height, int width)
    {
        frameprocessing -> startPoint(data, height, width);
    }
}
