from jetbot import Robot
import ipywidgets.widgets as widgets
from jetbot import Camera
import traitlets, time
from IPython.display import display
from jetbot import bgr8_to_jpeg

robot = Robot()

import ipywidgets.widgets as widgets
from IPython.display import display

# create two sliders with range [-1.0, 1.0]
left_slider = widgets.FloatSlider(description='left', min=-1.0, max=1.0, step=0.01, orientation='vertical')
right_slider = widgets.FloatSlider(description='right', min=-1.0, max=1.0, step=0.01, orientation='vertical')

# create a horizontal box container to place the sliders next to eachother
slider_container = widgets.HBox([left_slider, right_slider])

# display the container in this cell's output
display(slider_container)

import traitlets

left_link = traitlets.link((left_slider, 'value'), (robot.left_motor, 'value'))
right_link = traitlets.link((right_slider, 'value'), (robot.right_motor, 'value'))

left_link.unlink()
right_link.unlink()

left_link = traitlets.dlink((robot.left_motor, 'value'), (left_slider, 'value'))
right_link = traitlets.dlink((robot.right_motor, 'value'), (right_slider, 'value'))

# create buttons
button_layout = widgets.Layout(width='100px', height='80px', align_self='center')
stop_button = widgets.Button(description='stop', button_style='danger', layout=button_layout)
forward_button = widgets.Button(description='forward', layout=button_layout)
backward_button = widgets.Button(description='backward', layout=button_layout)
left_button = widgets.Button(description='left', layout=button_layout)
right_button = widgets.Button(description='right', layout=button_layout)
capture_button = widgets.Button(description='capture', layout=button_layout)

# def button
def stop(change):
    robot.stop()
    
def step_forward(change):
    robot.forward(0.2)
    
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

middle_box = widgets.HBox([left_button, stop_button, right_button], layout=widgets.Layout(align_self='center'))
controls_box = widgets.VBox([forward_button, middle_box, backward_button,capture_button])
display(controls_box)

image = widgets.Image(format='jpeg', width=300, height=300)
display(image)

camera = Camera.instance(width=300, height=300)

camera_link = traitlets.dlink((camera, 'value'), (image, 'value'), transform=bgr8_to_jpeg)

import uuid
import subprocess
camera = Camera.instance()
image = widgets.Image(format='jpeg', width=224, height=224)
snapshots = widgets.Image(format='jpeg', width=224, height=224)
camera_link = traitlets.dlink((camera, 'value'), (image, 'value'), transform=bgr8_to_jpeg)

button_layout = widgets.Layout(width='100px', height='80px')
button_snapshot = widgets.Button(description='snapshot', layout=button_layout)

middle_box = widgets.HBox([image, snapshots, button_snapshot], layout=widgets.Layout(align_self='center'))

subprocess.call(['mkdir', '-p', 'snapshots'])
def save_snapshot(change):
    file_path = 'snapshots/' + str(uuid.uuid1()) + '.jpg'
    with open(file_path, 'wb') as f:
        f.write(image.value)

    # display snapshot that was saved
    snapshots.value = image.value
    print('file_path')

button_snapshot.on_click(save_snapshot)

display(middle_box)
display(controls_box)
