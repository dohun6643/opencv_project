from jetbot import Robot
from jetbot import Camera
from IPython.display import display
from jetbot import bgr8_to_jpeg
import traitlets, time, subprocess, os
import ipywidgets.widgets as widgets

robot = Robot()

# 연결된 camera 화면 image view window 생성
image = widgets.Image(format='jpeg', width=300, height=300)
display(image)

# camera instance 생성
camera = Camera.instance(width=300, height=300)

# camera를 image view창에 뿌려주기
camera_link = traitlets.dlink((camera, 'value'), (image, 'value'), transform=bgr8_to_jpeg)

# make directory in jupyter notebook
subprocess.call(['mkdir', '-p', 'snapshots'])

# snapshot image size set
snapshot_image = widgets.Image(format='jpeg', width=300, height=300)

# snapshot function
def snapshot(change):
    # save snapshot onclick
    if change['new']:
        strpath = 'snapshots/'
        dirobj = os.listdir(strpath)
        count = len(dirobj)
        file_path = 'snapshots/%05d.jpg' %count # 00000.jpg의 순서대로 만들어짐
        
        # write snapshot to file (we use image value instead of camera because it's already in JPEG format)
        with open(file_path, 'wb') as f:
            filechanged = bgr8_to_jpeg(camera.value) # bgr8을 jpeg로 형식 변환
            f.write(filechanged)
            
        # display snapshot that was saved
        snapshot_image.value = filechanged

# snap image view
display(snapshot_image)

# jetbot snapshot images send to local computer
'''
In jetbot terminal
PC로 보낼 image 파일들이 있는 경로로 이동
cd Notebooks/snapshots/

tar cvf image.tar * # tar는 zip과 같은 형식, 생성하고자 하는 이름.tar * (*)를 줌으로써 모든 파일 tar함

scp image.tar rapa@192.168.0.39:/home/rapa/Downloads # scp로 만든 tar local pc로 전송

In local terminal
전송받은 경로로 들어가서
tar xvf image.tar # tar파일 압축 해제
'''