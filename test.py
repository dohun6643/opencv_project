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