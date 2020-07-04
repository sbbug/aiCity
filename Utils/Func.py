
import cv2
import Parameters
from Functions import getProjectContext
import time
import os
import matplotlib.pyplot as plt

def monitor_show(cameras):
    # 显示高度
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, 1.03 * height, '%s' % int(height))

    nowDate = str(time.strftime("%Y-%m-%d", time.localtime()))
    nowDatePath = getProjectContext() + os.path.join(Parameters.CAMERA_LOG, nowDate)
    # 如果当前目录不存在创建一个新的目录
    if not os.path.exists(nowDatePath):
        os.makedirs(nowDatePath)

    while True:
        camera_list = list()
        detect_queue_list = list()
        for c in cameras:
            camera_list.append(c.cam_id.split("_")[1])
            detect_queue_list.append(c.getDetectQSize())

        autolabel(plt.bar(range(len(detect_queue_list)), detect_queue_list, color='rgb', tick_label=camera_list))

        plt.savefig(os.path.join(nowDatePath,"queue_size.jpg"))
        time.sleep(2)