import os
import cv2 as cv
import glob

inputFolder = "/home/dohun/Documents/imageroad/"
folderLen = len(inputFolder)
for img in glob.glob(inputFolder + "/*.jpg"):
    image = cv.imread(img)
    imgCropped = image[150:300, 0:300]
    cv.imwrite("ImageCropped/" + img[folderLen:], imgCropped )
    cv.imshow('imageCrop', imgCropped)
    cv.waitKey(100)
cv.destroyAllWindows()