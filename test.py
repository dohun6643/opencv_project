# jupyter notebook test용
# button 생성 및 클릭으로 motion 구동, jetbot camera 연결

from jetbot import Robot
import ipywidgets.widgets as widgets
from jetbot import Camera
import traitlets, time
from IPython.display import display
from jetbot import bgr8_to_jpeg

robot = Robot()

# make button
button_layout = widgets.Layout(width='100px', height='80px', align_self='center')
stop_button = widgets.Button(description='stop', button_style='danger', layout=button_layout)
forward_button = widgets.Button(description='forward', layout=button_layout)
backward_button = widgets.Button(description='backward', layout=button_layout)
left_button = widgets.Button(description='left', layout=button_layout)
right_button = widgets.Button(description='right', layout=button_layout)

# def button
def stop(change):
    robot.stop()
    
def step_forward(change):
    robot.forward(0.1)
    
def step_backward(change):
    robot.backward(0.1)

def step_left(change):
    robot.left(0.1)
    
def step_right(change):
    robot.right(0.1)

# link buttons to actions
stop_button.on_click(stop)
forward_button.on_click(step_forward)
backward_button.on_click(step_backward)
left_button.on_click(step_left)
right_button.on_click(step_right)

# display buttons
middle_box = widgets.HBox([left_button, stop_button, right_button], layout=widgets.Layout(align_self='center'))
controls_box = widgets.VBox([forward_button, middle_box, backward_button])
display(controls_box)

# 연결된 camera 화면 image view window 생성
image = widgets.Image(format='jpeg', width=300, height=300)
display(image)

# camera instance 생성
camera = Camera.instance(width=300, height=300)

# camera를 image view창에 뿌려주기
camera_link = traitlets.dlink((camera, 'value'), (image, 'value'), transform=bgr8_to_jpeg)

# jetbot zigzag
from jetbot import Robot
import math
import time

robot = Robot()

def Runcar(radius, offset, angle, factor, sleeptime):
    for i in range(0, angle):
        left_speed = radius * math.sin(i*3.14/180) * factor + offset
        right_speed = (radius -2) * math.sin(i*3.14/180) * factor + offset
        robot.set_motors(left_speed, right_speed)
        time.sleep(sleeptime)
        
    for i in range(0, angle):
        left_speed = (radius - 2) * math.sin(i*3.14/180) * factor + offset
        right_speed = radius * math.sin(i*3.14/180) * factor + offset
        robot.set_motors(left_speed, right_speed)
        time.sleep(sleeptime)

Runcar(4, 0.1, 10, 0.2, 0.2)
Runcar(4, 0.1, 10, 0.2, 0.2)
time.sleep(3)
robot.stop()


# jupyter copy
from jetbot import Robot
from jetbot import Camera
from IPython.display import display
from jetbot import bgr8_to_jpeg
import time, numpy as np, cv2 as cv
import ipywidgets.widgets as widgets
import matplotlib.pyplot as plt

robot = Robot()

camera = Camera.instance(width=300, height=300)
originalCam = widgets.Image(format='jpeg', width=300, height=300)
grayCam = widgets.Image(format='jpeg', width=300, height=300)
threshCam = widgets.Image(format='jpeg', width=300, height=300)
cannyCam = widgets.Image(format='jpeg', width=300, height=300)

def convertGray(img):
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5,5), 0)
    return imgBlur

def applyThreshold(convertGray):
    ret,thresh = cv.threshold(convertGray, 100, 255, cv.THRESH_OTSU + cv.THRESH_BINARY_INV)
    return thresh

def applyCanny(applyThreshold):
    canny = cv.Canny(applyThreshold, 0, 1500)
    kernel = np.ones((5,5), np.uint8)
    imgDilate = cv.dilate(canny, kernel, iterations=1)
    return imgDilate

def detecting(img, applyCanny):
    contours, _ = cv.findContours(applyCanny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        epsilon = 0.01 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)
        cv.drawContours(img, [approx], 0, (255, 0, 0), 2)
    return img

display(widgets.HBox((originalCam, grayCam)))
display(widgets.HBox((threshCam, cannyCam)))

while True :
    img = (camera.value)
    grayimg = convertGray(img)
    threshimg = applyThreshold(grayimg)
    cannyimg = applyCanny(threshimg)
    detectimg = detecting(img, cannyimg)
    
    originalCam.value= bgr8_to_jpeg(img,100)
    grayCam.value = bgr8_to_jpeg(grayimg,100)
    threshCam.value = bgr8_to_jpeg(threshimg,100)
    cannyCam.value = bgr8_to_jpeg(cannyimg,100)
    
    time.sleep(0.1)

# ---------------------------------------------------------------------------
from jetbot import Robot
from jetbot import Camera
from IPython.display import display
from jetbot import bgr8_to_jpeg
import time, traitlets, subprocess, os
import ipywidgets.widgets as widgets
import numpy as np, cv2 as cv
robot = Robot()

def stop(change):
    robot.stop()
    
def forward(change):
    robot.set_motors(0.11,0.1) # 좌우 모터 출력값이 달라 직선으로 가게하기 위해 개별적으로 모터 제어
                               # 모터의 최소 출력값이 0.1

def turnLeft(change): # 약 90도 좌향좌
    robot.right_motor.value = 0.1
    time.sleep(2.4) # 이 기체는 왼쪽 모터의 출력이 조금 더 쎈것 같음 
    robot.stop()

def turnRight(change): # 약 90도 우향우
    robot.left_motor.value = 0.1
    time.sleep(2.8)
    robot.stop()

def detourLeft(change): # 좌로 우회
    for i in range(0,5):
        robot.set_motors(0.15, 0.1)
        time.sleep(1)
    
    robot.stop()
    
def detourRight(change): # 우로 우회
    for i in range(0,5):
        robot.set_motors(0.1, 0.15)
        time.sleep(1)
    
    robot.stop()
    
def snapshot(change):
    # save snapshot onclick
#     if change['new']:
    strpath = 'snapshots/'
    dirobj = os.listdir(strpath)
    count = len(dirobj)
    file_path = 'snapshots/%05d.jpg' %count
        
        # write snapshot to file (we use image value instead of camera because it's already in JPEG format)
    with open(file_path, 'wb') as f:
        filechanged = bgr8_to_jpeg(camera.value)
        f.write(filechanged)
            
        # display snapshot that was saved
    snapshot_image.value = filechanged

    # create buttons
button_layout = widgets.Layout(width='100px', height='80px', align_self='center')
stop_button = widgets.Button(description='stop', button_style='danger', layout=button_layout)
forward_button = widgets.Button(description='forward', layout=button_layout)
snapshot_button = widgets.Button(description='snapshot', layout=button_layout)

detourLeft_button = widgets.Button(description='detourLeft', layout=button_layout)
detourRight_button = widgets.Button(description='detourRight', layout=button_layout)

turnLeft_button = widgets.Button(description='turnLeft', layout=button_layout)
turnRight_button = widgets.Button(description='turnRight', layout=button_layout)

# display buttons
middle_box = widgets.HBox([detourLeft_button, stop_button, detourRight_button], layout=widgets.Layout(align_self='center'))
bottom_box = widgets.HBox([turnLeft_button, snapshot_button, turnRight_button], layout=widgets.Layout(align_self='center'))
controls_box = widgets.VBox([forward_button, middle_box, bottom_box])

display(controls_box)

# link buttons to actions
stop_button.on_click(stop)
forward_button.on_click(forward)

detourLeft_button.on_click(detourLeft)
detourRight_button.on_click(detourRight)

turnLeft_button.on_click(turnLeft)
turnRight_button.on_click(turnRight)

snapshot_button.on_click(snapshot)