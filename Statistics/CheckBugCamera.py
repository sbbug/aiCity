import os
from Functions import getProjectContext
from Parameters import HTTP_CAMERAS,NEW_CAMERAS_CONFIG
from Functions import getProjectContext,loadIPConfig

if __name__ == "__main__":
    dir = "Resources/HttpCameras"
    date = "2020-05-26"

    now_cameras = []

    for idx, camera in enumerate(os.listdir(getProjectContext() + os.path.join(dir, date))):


        now_cameras.append(camera)

        for angle in os.listdir(getProjectContext() + os.path.join(dir, date, camera)):
            pass

            # print("------",angle)

    ipConfig = loadIPConfig(getProjectContext() + NEW_CAMERAS_CONFIG)

    for c in HTTP_CAMERAS:
        if c not in now_cameras:
            for cam in ipConfig:
                if cam['cam_id']==c:
                    print(c,cam['address'])