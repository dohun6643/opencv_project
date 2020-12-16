from cv2 import cv2 as cv

img = cv.imread("/home/dohun/Documents/snapshots/01.jpg")
cv.imshow("image", img)
print(img.shape)
# (462, 623, 3)

imgResize = cv.resize(img, (200, 200))
cv.imshow("image Resize", imgResize)
print(imgResize.shape)

#150~200

print(type(img))
imgCropped = img[0:100, 0:0]
# cv.imshow("image Cropped", imgCropped)

cv.waitKey(0)

