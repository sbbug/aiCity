import os
from Functions import getMasked,getProjectContext
import cv2

if __name__ == "__main__":

    cam_id = "ba8d8a7a20a64abbb0699664f1f118f4"
    angle_id = "2"

    img = cv2.imread(
        getProjectContext() + "Resources/HttpCameras/2020-05-25/"+cam_id+"/"+angle_id+"/0b88b1cd-83d4-418b-8a22-24aa272ea8b7.jpg")


    print(img.shape)
    img = cv2.resize(img,(1280,720))
    mask = getMasked(img,"ba8d8a7a20a64abbb0699664f1f118f4_2")

    cv2.imwrite("temp.jpg",mask)

    # cv2.imshow("res",mask)