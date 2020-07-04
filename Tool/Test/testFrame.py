import os
import cv2
import numpy as np
img_path = "Resources/ImageTemplate"

def showGrid(key_imgs):
    '''
    :param key_imgs: dict of camera key:cam_id value:img_data
    :return: grid
    '''
    i=1
    temp = []
    rows = []
    for key in key_imgs.keys():
        if i % 6 == 0:
            temp.append(key_imgs[key])
            i += 1
            row = np.hstack(temp)
            rows.append(row)
            temp.clear()
        else:
            temp.append(key_imgs[key])
            i += 1
    if len(temp) > 0 and len(temp) < 6:
        while True:
            if len(temp) == 6:
                break
            temp.append(np.zeros((100, 200, 3), np.uint8))
        row = np.hstack(temp)
        rows.append(row)

    show = np.vstack(rows)

    return show

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        print("x:",x,"y:",y)
        i = x // 200
        j = y // 100
        num = j*6+i
        cv2.namedWindow(img_names[num])
        # cv2.startWindowThread()
        # cv2.imshow(img_names[num],img_big_datas[img_names[num].split(".")[0]])
        cv2.destroyWindow(img_names[num])
        print("quit")


if __name__=="__main__":
    cv2.namedWindow("display")
    cv2.setMouseCallback("display", on_EVENT_LBUTTONDOWN)
    while True:
        img_names = os.listdir(img_path)
        print("---")
        img_small_datas = {}
        img_big_datas = {}
        for img_name in img_names:
            img = cv2.imread(os.path.join(img_path,img_name))
            img_big_datas[img_name.split(".")[0]] = cv2.resize(img,(800,500))
            img = cv2.resize(img,(200,100))
            img_small_datas[img_name.split(".")[0]] = img
        #print(img_datas)
        show = showGrid(img_small_datas)
        cv2.imshow("display", show)
        cv2.waitKey(10)

