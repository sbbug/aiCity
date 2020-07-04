import cv2

from Functions import loadIPConfig, getProjectContext, getCameraUrl
import Parameters
import os
if __name__ == "__main__":

    ipConfig = loadIPConfig(getProjectContext() + Parameters.CAMERAS_CONFIG)

    for c in ipConfig:
        url = getCameraUrl(c)
        print("...")
        cap = cv2.VideoCapture(url)
        print(url)
        frame = None
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.resize(frame,(1280,720))
            if ret is True:
                break

        for points in Parameters.CAM_ANCHORS[c['cam_id']]:

            x1 = points[0]
            y1 = points[1]
            x2 = x1+points[2]
            y2 = y1+points[3]

            cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 3)  # 画出最终的矩形

            cv2.imwrite(os.path.join(getProjectContext(),'Resources/Cache',c['cam_id']+".jpg"),frame)
