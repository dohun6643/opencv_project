from jetbot import Robot
from IPython.display import display
import time, math
import ipywidgets.widgets as widgets

def stop(change):
    robot.stop()
    
def forward(change):
    robot.set_motors(0.11,0.1) # 좌우 모터 출력값이 달라 직선으로 가게하기 위해 개별적으로 모터 제어
                               # 모터의 최소 출력값이 0.1

def backward(change):
    robot.backward(0.1)

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

# if use controller --------------------------------------------------------------------------------------------------------
# create buttons
button_layout = widgets.Layout(width='100px', height='80px', align_self='center')
stop_button = widgets.Button(description='stop', button_style='danger', layout=button_layout)
forward_button = widgets.Button(description='forward', layout=button_layout)
backward_button = widgets.Button(description='backward', layout=button_layout)

detourLeft_button = widgets.Button(description='detourLeft', layout=button_layout)
detourRight_button = widgets.Button(description='detourRight', layout=button_layout)

turnLeft_button = widgets.Button(description='turnLeft', layout=button_layout)
turnRight_button = widgets.Button(description='turnRight', layout=button_layout)

# display buttons
middle_box = widgets.HBox([detourLeft_button, stop_button, detourRight_button], layout=widgets.Layout(align_self='center'))
bottom_box = widgets.HBox([turnLeft_button, backward_button, turnRight_button], layout=widgets.Layout(align_self='center'))
controls_box = widgets.VBox([forward_button, middle_box, bottom_box])

display(controls_box)

# link buttons to actions
stop_button.on_click(stop)
forward_button.on_click(forward)
backward_button.on_click(backward)

detourLeft_button.on_click(detourLeft)
detourRight_button.on_click(detourRight)

turnLeft_button.on_click(turnLeft)
turnRight_button.on_click(turnRight)
# -------------------------------------------------------------------------------------------------------------------------------

# if use code -------------------------------------------------------------------------------------------------------------------