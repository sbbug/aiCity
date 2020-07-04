import cv2
from Functions import getProjectContext
import time
import numpy as np
import os
SCALE = 0.8

RAW_IM_WIDTH = 1280
RAW_IM_HEIGHT = 720


def unScaleX(x):
    return int(x / SCALE)


def scaleX(x):
    return int(x * SCALE)


def scaleXY(x, y):
    return int(x * SCALE), int(y * SCALE)


def unScaleXY(x, y):
    return int(x / SCALE), int(y / SCALE)


def OnMouseAction(event, x, y, flags, param):
    global position1, position2

    image = vars['img'].copy()

    if event == cv2.EVENT_LBUTTONDOWN:  # 按下左键
        position1 = (x, y)  # 获取鼠标的坐标(起始位置)

    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:  # 按住左键拖曳不放开
        cv2.rectangle(image, position1, (x, y), (0, 255, 0), 3)  # 画出矩形选定框
        cv2.imshow('show', image)

    elif event == cv2.EVENT_LBUTTONUP:  # 放开左键
        position2 = (x, y)  # 获取鼠标的最终位置
        cv2.rectangle(image, position1, position2, (0, 0, 255), 3)  # 画出最终的矩形
        cv2.imshow('show', image)

        min_x = min(position1[0], position2[0])  # 获得最小的坐标，因为可以由下往上拖动选定框
        min_y = min(position1[1], position2[1])
        width = abs(position1[0] - position2[0])  # 切割坐标
        height = abs(position1[1] - position2[1])
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        vars['rois'].append([min_x, min_y, width, height])
        for points in vars['rois']:
            x1 = points[0]
            y1 = points[1]
            x2 = x1 + points[2]
            y2 = y1 + points[3]
            cv2.rectangle(vars['img'], (x1, y1), (x2, y2), (0, 255, 0), 3)

        time.sleep(1)
        x1_ = unScaleX(x1)
        y1_ = unScaleX(y1)
        x2_ = unScaleX(x2)
        y2_ = unScaleX(y2)

        mask_img = np.zeros((720, 1280, 3))
        mask_img[y1_:y2_, x1_:x2_] = 255
        show_mask_img = np.zeros((scaleX(720), scaleX(1280), 3))
        show_mask_img[y1:y2, x1:x2] = 255
        # print(show_mask_img)
        cv2.imwrite(os.path.join(getProjectContext()+'Resources/mask',cam_id+"_"+angle_id+".jpg"), mask_img)
        cv2.imshow('show', show_mask_img)



if __name__ == "__main__":
    vars = dict()
    vars['now_x'] = 0
    vars['now_y'] = 0
    vars['img'] = None
    vars['rois'] = []

    cam_id = "ba8d8a7a20a64abbb0699664f1f118f4"
    angle_id = "2"

    need_mask_image_dir = ""

    img = cv2.imread(
        getProjectContext() + "Resources/HttpCameras/2020-05-25/"+cam_id+"/"+angle_id+"/0b88b1cd-83d4-418b-8a22-24aa272ea8b7.jpg")

    print(getProjectContext() + "Resources/HttpCameras/2020-05-25/"+cam_id+"/"+angle_id+"/0b88b1cd-83d4-418b-8a22-24aa272ea8b7.jpg")

    print(img)
    scale = 0.8

    img = cv2.resize(img, (1280, 720))

    img = cv2.resize(img, (scaleXY(1280, 720)))

    cv2.namedWindow("show")
    cv2.setMouseCallback('show', OnMouseAction)

    vars['img'] = img

    cv2.imshow("show", img)

    cv2.waitKey(-1)
