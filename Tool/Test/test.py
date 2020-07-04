import cv2 as cv2
import Functions
import Parameters
import numpy as np

ipConfig = Functions.loadIPConfig(Functions.getProjectContext() + Parameters.CAMERAS_CONFIG)
now = -1
camera_num = len(ipConfig)

while now < camera_num:
    now += 1
    now = now % camera_num
    camID = ipConfig[now]["cam_id"]
    camUrl = Functions.getCameraUrl(ipConfig[now])
    cap = cv2.VideoCapture(camUrl)

    print("当前检测的摄像头", camID)
    if cap.isOpened() == False:
        print("%s is not opened!", camID)
        res = {"cam_id": camID, "frame": np.zeros((1280, 720, 3), np.uint8)}
        continue
    ret, frame = cap.read()
    cap.release()
    if frame.shape==(1080, 1920, 3):
        print(camID)
    if camID == "camera_39":
        break
