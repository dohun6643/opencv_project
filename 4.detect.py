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