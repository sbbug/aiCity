import cv2
import os

CAM_PATH = "./cameras"
vars = dict()
vars['now_x'] = 0
vars['now_y'] = 0
vars['img'] = None
vars['rois'] = []
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

        vars['rois'].append([min_x,min_y,width,height])
    for points in vars['rois']:
        x1 = points[0]
        y1 = points[1]
        x2 = x1 + points[2]
        y2 = y1 + points[3]
        cv2.rectangle(vars['img'], (x1, y1), (x2, y2), (0, 255, 0), 3)
    print(vars['rois'])

if __name__=="__main__":

    img_names = os.listdir(CAM_PATH)
    cv2.namedWindow("show")
    cv2.setMouseCallback('show', OnMouseAction)
    for img_name in img_names:
        vars['img'] = cv2.imread(os.path.join(CAM_PATH,img_name))

        while True:
            cv2.imshow("show",vars['img'])
            key = cv2.waitKey(-1)
            if key == ord(' '):
                break

        # 将坐标信息写入文件
        file_path = os.path.join("txt",img_name.split(".")[0]+".txt")
        file_handler = open(file_path,"w")
        file_handler.write(str(vars['rois']))
        file_handler.close()
        vars['rois'] = []