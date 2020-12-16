## 1. 참고 자료
--------------------------------------------------
- blackcode <br>
https://github.com/blackcoke/Proj_road_detection- <br>

- CSI-Camera <br>
https://github.com/JetsonHacksNano/CSI-Camera <br>
GStreamer를 이용해서 카메라 이미지 획득하는 방법 설명함 <br>

<p> &nbsp; </p>

## 2. 프로그램 설치하기
--------------------------------------------------
$ sudo apt install ffmpeg <br>
$ sudo apt install v4l-utils <br>
$ sudo apt install python3-opencv -y <br>
$ sudo apt install tightvncserver <br>
$ sudo apt install libcanberra-gtk-module libcanberra-gtk3-module <br>
<p> &nbsp; </p>


## 3. 비디오 장치 정보 출력하기
--------------------------------------------------
$ sudo v4l2-ctl --list-devices
> vi-output, imx219 7-0010 (platform:54080000.vi:0):
>        /dev/video0

<img src='README/03.jpg'> <br>

$ v4l2-ctl --device=/dev/video0 --all
> Driver Info (not using libv4l2):
>>        Driver name   : tegra-video
>>        Card type     : vi-output, imx219 7-0010
>>        Bus info      : platform:54080000.vi:0
>>        Driver version: 4.9.140

>>        Capabilities  : 0x84200001
>>>                Video Capture
>>>                Streaming
>>>                Extended Pix Format
>>>                Device Capabilities

>>        Device Caps   : 0x04200001
>>>                Video Capture
>>>                Streaming
>>>                Extended Pix Format
> Priority: 2

> Video input : 0 (Camera 0: no power)

> Format Video Capture:
>>        Width/Height      : 3264/2464
>>        Pixel Format      : 'RG10'
>>        Field             : None
>>        Bytes per Line    : 6528
>>        Size Image        : 16084992
>>        Colorspace        : sRGB
>>        Transfer Function : Default (maps to sRGB)
>>        YCbCr/HSV Encoding: Default (maps to ITU-R 601)
>>        Quantization      : Default (maps to Full Range)
<p> &nbsp; </p>

## 4. 카메라 테스트하기
--------------------------------------------------
- 카메라와 연결하기 위해 GStreamer 파이프라인을 구한다.

<pre>
(예)
# 모듈 불러오기
import cv2 as cv
import numpy as np
import os
import sys


# 매개변수 검사하기
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
        result = cv.waitKey(1)
    else:
        str = input("입력> ")
        keydata = str.strip()
        result = ord(keydata[0])

    print(result)
    return result

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

# main 함수
def main():
    # 카메라 장치 얻기
    pipeline = GetGstreamerPipeline(640, 480, 640, 480, 10)

    # 비디오 장치 얻기
    cap = cv.VideoCapture(pipeline)

    while cap.isOpened():
        # 이미지 읽기
        result, img = cap.read()

        if result:
            ShowImage("TITLE", img)
        
        # 키 처리하기
        keydata = InputKey()
        if keydata == ord('q'):
            break

    # 해제하기
    if cap.isOpened():
        cap.release()

    cv.destroyAllWindows()

# 메인 함수 호출하기
if __name__ == "__main__":
    main()
</pre>
<p> &nbsp; </p>

## 5. 동영상 녹화하기
--------------------------------------------------
- JetBot에 ssh 로 접속해 실행한다.<br>
- 녹화 파일명, 녹화 시간을 지정하면 해당 시간 동안 동영상 파일을 만든다.<br>

$ python3 RecordVideo.py
> 녹화 파일명 : file.avi <br>
> 녹화 시간 (초단위 ): 10 <br>

<img src='README/05_01.jpg'>

- 옵션 1을 주면 모니터 화면에서 녹화 화면을 볼 수 있다.

$ python3 RecordVideo.py 1
> 녹화 파일명 > file.avi <br>
> 녹화 시간 (초단위 ) > 10 <br>

<img src='README/05_02.jpg'>

<p> &nbsp; </p>

## 6. 이미지 파일로 저장하기
--------------------------------------------------
- JetBot에 ssh 로 접속해 실행한다.<br>
- 파일명, 시간을 지정하면 해당 시간 동안 이미지 파일을 0.1ms 주기로 만든다.<br>

$ python CameraToImage.py

<img src='README/06_01.jpg'> <br>

<img src='README/06_02.jpg'> <br>

<img src='README/06_03.jpg'> <br>

<p> &nbsp; </p>

## 7. 리모트 버튼 만들기
--------------------------------------------------

<pre>
# 모듈 불러오기
from jetbot import Camera
from jetbot import bgr8_to_jpeg
import ipywidgets.widgets as widgets
import cv2 as cv

# Push 버튼 프로시저
def button_proc(change):
    camera_image.value = bgr8_to_jpeg(camera.value)
    
# 카메라 객체 생성하기
camera = Camera.instance()

# 이미지 위젯 등록하기
camera_image = widgets.Image(format='jpeg', width=200, height=200)
 

# 버튼 레이아웃 설정하고 버튼 생성하기
layoutButton = widgets.Layout(width='100px', height='80px')
button_push = widgets.Button(description='Push', layout=layoutButton)

# 이미지 박스 만들고 이미지 출력하기
box = widgets.HBox([camera_image, button_push], layout=widgets.Layout(align_self='center'))
display(box)

# 버튼 이벤트 핸들러 설정하기
button_push.on_click(button_proc)
</pre>

<img src='README/07_01.jpg'> <br>

<p> &nbsp; </p>
