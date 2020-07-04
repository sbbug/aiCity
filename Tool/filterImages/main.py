import os
import glob
import shutil

dir_path = "../../Resources/ReportLog/FakeAbnormal/"

if __name__ == "__main__":

    # paths = os.listdir(dir_path)
    # print(paths)
    paths = ['2019-08-15','2019-08-14','2019-08-13','2019-08-12','2019-08-11','2019-08-10']
    for path in paths:
        camera_path = os.path.join(dir_path,path)
        cameras = os.listdir(camera_path)
        print(cameras)
        for camera in cameras:
            if not camera.endswith(".log"):
                img_path = os.path.join(camera_path,camera)
                images = os.listdir(img_path)
                i=0
                for m in images:
                    im_path = os.path.join(img_path,m)
                    print(im_path)
                    shutil.copy(im_path, "./images")
                    i=i+1
                    if i==10:
                        break;
