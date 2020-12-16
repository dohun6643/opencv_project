# 모듈 불러오기
import cv2 as cv
import numpy as np
import os
import sys
import time


# 매개변수 검사하기
g_bDisplay = 0
if len(sys.argv) > 1:
    g_bDisplay = int(sys.argv[1])

# img 출력하기
def ShowImage(str_title, img_data):
    if g_bDisplay:
        cv.imshow(str_title, img_data)

# 키 입력받기
def InputKey():
    keydata = 0
    if g_bDisplay:
        keydata = cv.waitKey(1)
    # else:
    #     str = input("입력> ")
    #     keydata = str.strip()
    #     keydata = ord(keydata[0])

    return keydata

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

# RecordVideo 함수
def RecordVideo(strfile, second):
    # 카메라 장치 얻기
    width = 200
    height = 200
    fps = 10
    pipeline = GetGstreamerPipeline(width, height, width, height, fps)

    # 카메라 장치 얻기
    cap = cv.VideoCapture(pipeline)

    # 비디오 파일 열기
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    video = cv.VideoWriter(strfile, fourcc, fps, (width, height))

    i = 0
    while cap.isOpened():
        # 이미지 읽기
        result, img = cap.read()

        # 저장하기
        if result:
            video.write(img)
            ShowImage("TITLE", img)
        
        # 키 입력받기
        result = InputKey()
        if result == ord('q'):
            break

        # 대기시간
        time.sleep(0.1)
        i = i + 1
        if i > second * 10:
            break
    
    # 해제하기
    if cap.isOpened():
        cap.release()

    if video.isOpened():
        video.release()

    cv.destroyAllWindows()

# main
def main():
    strfile = input("녹화 파일명> ")
    second = int(input("놕화 시간 (초단위)> ").strip())

    RecordVideo(strfile, second)

# 메인 함수 호출하기
if __name__ == "__main__":
    main()


