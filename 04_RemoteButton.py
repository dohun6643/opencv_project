# 리모트 버튼 만들기

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