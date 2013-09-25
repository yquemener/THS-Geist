//#include "cv.h"
//#include "highgui.h"
#include <stdio.h>
#include <stdlib.h>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <sstream>
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/features2d/features2d.hpp"

// Create a new Haar classifier
static cv::CascadeClassifier cascade;

// Function prototype for detecting and drawing an object from an image
void detect_and_draw( IplImage* image );

// Create a string that contains the cascade name
const char* cascade_name =
    "haarcascade_frontalface_alt.xml";
/*    "haarcascade_profileface.xml";*/



// Main function, defines the entry point for the program.
int main( int argc, char** argv )
{
    cv::VideoCapture capture;
    cv::Mat frame;
    cascade.load(cascade_name);
    
    // This works on a D-Link CDS-932L
    const std::string videoStreamAddress = "http://192.168.1.253/nphMotionJpeg?Resolution=320x240&amp;Quality=Standard&.mjpg";

    //open the video stream and make sure it's opened
    if(!capture.open(videoStreamAddress)) {
        std::cout << "Error opening video stream or file" << std::endl;
        return -1;
    }

    // Create a new named window with title: result
    cvNamedWindow( "Result", 1 );

    // Find if the capture is loaded successfully or not.

    // If loaded succesfully, then:
    // Capture from the camera.
    for(;;)
    {   
        cv::Mat gray;
        for(int i=0;i<10;i++)
            capture.grab();
        capture >> frame;
        cv::cvtColor(frame, gray, CV_BGR2GRAY);

        std::vector<cv::Rect> results;
        cascade.detectMultiScale(gray, results, 1.1, 3, 0);
        int dx=0;
        int dy=0;
        for(std::vector<cv::Rect>::iterator it=results.begin();
        it!=results.end();
        it++)
        {
          cv::Rect r = *it;
          std::cout << "_" << r.x << "_\t_" << r.y << "_\t" << std::endl;
          dx = r.x + r.width/2;
          dy = r.y + r.height/2;
        }
        std::stringstream ss;
        ss << "wget -q -O /dev/null \"http://192.168.1.253/nphControlCamera?Width=";
        ss << gray.cols;
        ss << "&Height=";
        ss << gray.rows;
        ss << "&Direction=Direct&NewPosition.x=" << dx;
        ss << "&NewPosition.y=" << dy<<"\"";
        if((dx!=0)||(dy!=0))
        {
            std::cout << ss.str() << std::endl;
            system(ss.str().c_str());
                
        }
        imshow("Result",gray);
        // Wait for a while before proceeding to the next frame
        if( cvWaitKey( 10 ) >= 0 )
            break;
        
    }

    return 0;
}

