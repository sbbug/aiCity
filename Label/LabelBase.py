'''
这个脚本文件用来抓取每个摄像头的base图像，并保存到文件
'''
import sys
sys.path.append("..")
import cv2
from Functions import loadIPConfig,getCameraUrl,isExistTempalte,getProjectContext
import Parameters
import Label.Label as label
import os

# 生成图像模板，图像名字是cam_id
def isExistTempalte(camera_id,img_tpl=None,cover=False):
    '''
    :param img_tpl: 传入当前摄像头下的模板图像
    :param camera_id: 摄像头对应的编号
    :param cover: 是否覆盖，默认False不覆盖
    :return:
    '''
    now_path = os.path.join("camera",camera_id+ ".jpg")

    # 如果当前模板文件不存在，则将模板存进去
    if os.path.exists(now_path)==False:
        cv2.imwrite(now_path, img_tpl)

    # 如果cover==True,说明需要覆盖
    if cover==True:
        cv2.imwrite(now_path, img_tpl)

    # 返回当前模板的图像
    return cv2.imread(now_path)

if __name__ =="__main__":


   label = label.Label()

   cameras = loadIPConfig(getProjectContext() + Parameters.CAMERAS_CONFIG)
   cv2.namedWindow('image')

   for camera in cameras:

       # 获取当前摄像机的url
       url = getCameraUrl(camera)
       print(url)

       # 开始读取视频流
       cap = cv2.VideoCapture(url)

       if(cap.isOpened()==False):
           continue

       # 获取摄像头第一帧数据
       while (cap.isOpened()):

           ret, frame = cap.read()
           if ret == False:
               break

           if frame is None:
               break

           frame = cv2.resize(frame,(1280,720))
           cv2.imshow("image", frame)
           flag = cv2.waitKey(2)
           if (flag & 0xFF) == ord('s'):  # n键代表切换到下一个
               isExistTempalte(camera['cam_id'],frame)
               break

       cap.release()

   cv2.destroyAllWindows()