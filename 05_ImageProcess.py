# 모듈 불러오기
import cv2 as cv
import numpy as np
import os
import sys



# GStreamer 파이프라인 얻기
def GetGstreamerPipeline(
    capture_width=640,
    capture_height=480,
    display_width=640,
    display_height=480,
    framerate=10,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

# VideoCapture 얻기
def GetVideoCapture():
    # 카메라 장치 얻기
    pipeline = GetGstreamerPipeline(200, 200, 200, 200, 200)    
    cap = cv.VideoCapture(pipeline)

    return cap

# filter 적용하기
def GetFilter(img_data):
    height = img_data.shape[0]
    width = img_data.shape[1]

    # Gray 로 변환하기
    img_gray = cv.cvtColor(img_data, cv.COLOR_BGR2GRAY)

    # threshold 적용하기
    result, img_thresh = cv.threshold(img_gray, 100, 255, cv.THRESH_BINARY_INV)

    # 침식 연산 적용하기
    kernel = np.ones((3, 3), np.uint8)
    img_erode = cv.erode(img_thresh, kernel, iterations=5)

    # 위에 색깔 0으로 만들기
    img_erode[0:20, 0:width] = 0

    return img_erode

# 가장 큰 외곽선 찾기
def FindMaxContour(img_data):
    pass
# main 함수
def main():
    #
    strdir = os.getcwd() + "/images/"
    files = os.listdir(strdir)

    for file in files:
        # 이미지 파일 읽기
        img = cv.imread(strdir + file)

        img_erode = GetFilter(img)       

        cv.imshow("TITLE", img_erode)

        keydata = cv.waitKey(10)
        if keydata == ord('q'):
            break
    
#
if __name__ == "__main__":
    main()
