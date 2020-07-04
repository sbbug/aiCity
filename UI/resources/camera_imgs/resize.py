
import cv2


im = cv2.imread("./camera_2.jpg")

im = cv2.resize(im,(320,200))

cv2.imwrite("./camera_2.jpg",im)