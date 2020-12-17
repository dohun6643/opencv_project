from cv2 import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread('/home/rapa/Downloads/snapshots/2d3c41aa-3f6f-11eb-be55-ccd9ac094070.jpg')
# cv.imshow("show", img)

imgCrop = img[133:300,0:300]
# cv.imshow("show", imgCrop)

imgGray = cv.cvtColor(imgCrop, cv.COLOR_BGR2GRAY)
# cv.imshow("show", imgGray)

imgBlur = cv.GaussianBlur(imgGray, (5,5), 0)
# cv.imshow("Blur", imgBlur)

img2 = cv.imread("/home/rapa/Downloads/snap/file_00617.png", cv.IMREAD_GRAYSCALE)
cv.imshow("eoh image", img2)
print(img2.shape)

img2Blur = cv.GaussianBlur(img2, (5,5), 0)
cv.imshow("eoh blur", img2Blur)

ret,thresh1 = cv.threshold(imgBlur, 100, 255, cv.THRESH_BINARY) 
ret,thresh2 = cv.threshold(imgBlur, 100, 255, cv.THRESH_BINARY_INV) 
ret,thresh3 = cv.threshold(imgBlur, 100, 255, cv.THRESH_TRUNC) 
ret,thresh4 = cv.threshold(imgBlur, 100, 255, cv.THRESH_TOZERO)
ret,thresh5 = cv.threshold(imgBlur, 100, 255, cv.THRESH_TOZERO_INV)
ret,thresh6 = cv.threshold(imgBlur, 100, 255, cv.THRESH_OTSU)

# cv.imshow("show1",thresh1)
# cv.imshow("show2",thresh2)
# cv.imshow("show3",thresh3)
# cv.imshow("show4",thresh4)
# cv.imshow("show5",thresh5)
# cv.imshow("show6", thresh6)

ret,Thresh1 = cv.threshold(img2Blur, 100, 255, cv.THRESH_BINARY)
ret,Thresh2 = cv.threshold(img2Blur, 100, 255, cv.THRESH_BINARY_INV) 
ret,Thresh3 = cv.threshold(img2Blur, 100, 255, cv.THRESH_TRUNC)
ret,Thresh4 = cv.threshold(img2Blur, 100, 255, cv.THRESH_TOZERO) 
ret,Thresh5 = cv.threshold(img2Blur, 100, 255, cv.THRESH_TOZERO_INV) 

ret,Thresh6 = cv.threshold(img2Blur, 100, 255, cv.THRESH_OTSU + cv.THRESH_BINARY_INV)

# cv.imshow("show1",Thresh1)
# cv.imshow("show2",Thresh2)
# cv.imshow("show3",Thresh3)
# cv.imshow("show4",Thresh4)
# cv.imshow("show5",Thresh5)
# cv.imshow("show6",Thresh6)

canny = cv.Canny(Thresh6, 0, 1500)
cv.imshow("Canny", canny)

kernel = np.ones((5,5), np.uint8)
imgDilate = cv.dilate(canny, kernel, iterations=1)
cv.imshow("Dilate", imgDilate)

cv.waitKey(0)

# def nothing():
#     pass

# cv.namedWindow("Canny Edge1")
# cv.namedWindow("Canny Edge2")
# cv.namedWindow("Canny Edge3")

# cv.createTrackbar("Low Threshold", "Canny Edge1", 0, 1000, nothing) # 가우시안 블러 5,5, 캐니엣지 99
# cv.createTrackbar("High Threshold", "Canny Edge1", 1000, 2000, nothing)
# cv.createTrackbar("Low Threshold", "Canny Edge2", 0, 1500, nothing) # 가우시안 블러 5,5, 캐니엣지 99
# cv.createTrackbar("High Threshold", "Canny Edge2", 0, 3000, nothing)
# cv.createTrackbar("Low Threshold", "Canny Edge3", 0, 1500, nothing) # 캐니엣지 1500
# cv.createTrackbar("High Threshold", "Canny Edge3", 0, 3000, nothing)

# while True:
#     low = cv.getTrackbarPos("Low Threshold", "Canny Edge1")
#     high = cv.getTrackbarPos("High Threshold", "Canny Edge1")
#     low1 = cv.getTrackbarPos("Low Threshold", "Canny Edge2")
#     high1 = cv.getTrackbarPos("High Threshold", "Canny Edge2")
#     low2 = cv.getTrackbarPos("Low Threshold", "Canny Edge3")
#     high2 = cv.getTrackbarPos("High Threshold", "Canny Edge3")
    
#     img_canny = cv.Canny(Thresh1, low, high)
#     img_canny1 = cv.Canny(Thresh2, low1, high1)
#     img_canny2 = cv.Canny(Thresh6, low2, high2)

#     cv.imshow("Canny Edge1", img_canny)
#     cv.imshow("Canny Edge2", img_canny1)
#     cv.imshow("Canny Edge3", img_canny2)

#     if cv.waitKey(1) == ord('q'):
#         break

"""
저장된 이미지 도로를 불러와서 어떤 필터를 적용할 것인지를 테스트 해보고
카메라에 적용하는 방법
즉, 도로 이미지에 gray, blur, threshold, canny까지 세밀하게 각 종 값들로 테스트 해보고
하나를 선택하여 카메라에 적용
"""

# jupyter notebook에 선택한 필터 적용 방법 -------------------------------------------------------------
# from jetbot import Robot
# from jetbot import Camera
# from IPython.display import display
# from jetbot import bgr8_to_jpeg
# import time, numpy as np, cv2 as cv
# import ipywidgets.widgets as widgets
# import matplotlib.pyplot as plt

# robot = Robot()

# camera = Camera.instance(width=300, height=300)
# originalCam = widgets.Image(format='jpeg', width=300, height=300)
# grayCam = widgets.Image(format='jpeg', width=300, height=300)
# threshCam = widgets.Image(format='jpeg', width=300, height=300)
# cannyCam = widgets.Image(format='jpeg', width=300, height=300)

# def convertGray(img):
#     imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#     imgBlur = cv.GaussianBlur(imgGray, (5,5), 0)
#     return imgBlur

# def applyThreshold(convertGray):
#     ret,thresh = cv.threshold(convertGray, 100, 255, cv.THRESH_OTSU + cv.THRESH_BINARY_INV)
#     return thresh

# def applyCanny(applyThreshold):
#     canny = cv.Canny(applyThreshold, 0, 1500)
#     kernel = np.ones((5,5), np.uint8)
#     imgDilate = cv.dilate(canny, kernel, iterations=1)
#     return imgDilate

#     display(widgets.HBox((originalCam, grayCam, threshCam)))
# display(widgets.HBox((threshCam, cannyCam)))

# while True :
#     img = (camera.value)
#     grayimg = convertGray(img)
#     threshimg = applyThreshold(grayimg)
#     cannyimg = applyCanny(threshimg)
    
#     originalCam.value= bgr8_to_jpeg(img,100)
#     grayCam.value = bgr8_to_jpeg(grayimg,100)
#     threshCam.value = bgr8_to_jpeg(threshimg,100)
#     cannyCam.value = bgr8_to_jpeg(cannyimg,100)
    
#     time.sleep(0.1)