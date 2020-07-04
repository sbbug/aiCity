'''
'''
import cv2
import json
import sys
import Parameters
import numpy as np
# from Algorithm.KNN import Knn  # 必须使用from Algorithm.KNN import Knn 而不是from KNN import Knn
import Functions
from Algorithm.Model.VGG import Vgg
import os


def imgPreProcess(img):
    # gamma变换
    img = Functions.adjustGamma(img, 3.8)
    # 灰度图变换
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # # 直方图均衡化
    # base = cv2.equalizeHist(base)
    # front = cv2.equalizeHist(front)
    # 高斯滤波
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # if parameters.debug:
    #     cv2.imshow("template", base)
    #     cv2.imshow("frame", front)
    #     cv2.waitKey(0)
    # 获取边缘轮廓
    img = cv2.Canny(img, 100, 200)
    # 进行腐蚀操作
    # opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, (3, 3))
    # if parameters.debug:
    #     cv2.imshow("template", base)
    #     cv2.imshow("frame", front)
    #     cv2.waitKey(0)
    # 图像线性变换
    # base = base*0.8
    # front = front*0.8

    # 图像二值化
    # _ ,base = cv2.threshold(base, 150, 255, cv2.THRESH_BINARY)
    # _ ,front = cv2.threshold(front, 150, 255, cv2.THRESH_BINARY)

    # ganmam变换
    return img


def differentRegionsFilter(differentRegions, ROIs):
    """
    筛选变化区域
    :param differentRegions: 变化区域列表
    :param ROIs: ROIs
    :return: 筛选后的变化区域列表
    """
    ROIContours = [np.array(ROI) for ROI in ROIs]
    res = []
    # 中心是否出现在ROI中，ROI以外去掉
    for r in differentRegions:
        center = (r[0] + r[2] // 2, r[1] + r[3] // 2)
        isInROI = False
        for ROIContour in ROIContours:
            if cv2.pointPolygonTest(ROIContour, center, False) >= 0:
                isInROI = True
                break
        if isInROI == True:
            res.append(r)

    return res


# 基于Background Subtraction的异常检测算法
def getAbnormalRegions(frame):
    '''
    :param frame:
    :return:
    '''
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    diff = fgbg.apply(frame)
    diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)
    # diff[diff == 127] = 255

    cv2.imshow("diff", diff)
    cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 该函数计算一幅图像中目标的轮廓
    # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
    resTemp = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > Parameters.MIN_ABNORMAL_AREA_THRESHOLD]

    # 过滤包含关系的区域
    res = []

    def isContain(bbox1, bbox2):
        """
        bbox1是否包含bbox2？
        :param bbox1:
        :param bbox2:
        :return:
        """
        return bbox1[0] <= bbox2[0] and bbox1[1] <= bbox2[1] and \
               bbox1[0] + bbox1[2] >= bbox2[0] + bbox2[2] and bbox1[1] + bbox1[3] >= bbox2[1] + bbox2[3]

    for bbox1 in resTemp:
        isContained = False
        for bbox2 in resTemp:
            if bbox1 == bbox2: continue
            if isContain(bbox2, bbox1) == True:
                isContained = True
                break
        if isContained == False:
            res.append(bbox1)

    return res, diff


def getDifferentRegions(base, front):
    '''
    # 使用帧差法判断某一个区域是否已经发生变化
    :param base: 基准帧
    :param front: 当前帧
    :return:(x,y,w,h) 异常位置
    '''

    base = imgPreProcess(base)
    front = imgPreProcess(front)

    # if parameters.debug:
    #     cv2.imshow("template",base)
    #     cv2.imshow("frame", front)
    #     cv2.waitKey(0)
    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))

    # 使用帧差
    diff = cv2.absdiff(base, front)
    diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]  # 二值化阈值处理
    diff = cv2.dilate(diff, es, iterations=2)  # 形态学膨胀

    # if parameters.debug:
    #     cv2.imshow("diff",diff)
    #     cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 该函数计算一幅图像中目标的轮廓
    # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
    resTemp = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > Parameters.MIN_ABNORMAL_AREA_THRESHOLD]

    # 过滤包含关系的区域
    res = []

    def isContain(bbox1, bbox2):
        """
        bbox1是否包含bbox2？
        :param bbox1: 
        :param bbox2: 
        :return: 
        """
        return bbox1[0] <= bbox2[0] and bbox1[1] <= bbox2[1] and \
               bbox1[0] + bbox1[2] >= bbox2[0] + bbox2[2] and bbox1[1] + bbox1[3] >= bbox2[1] + bbox2[3]

    for bbox1 in resTemp:
        isContained = False
        for bbox2 in resTemp:
            if bbox1 == bbox2: continue
            if isContain(bbox2, bbox1) == True:
                isContained = True
                break
        if isContained == False:
            res.append(bbox1)

    return res, diff


def judgeAbnormalType(image, which_model="vgg"):
    """
    判断异常类型
    :param image: 异常图像
    :return: 异常类型
    """

    model = None

    if which_model == "knn":
        # model = Knn()
        pass
    elif which_model == "vgg":
        model = Vgg()

    label_index = model.getAbnormalType(image)
    print("label_index", label_index)
    return Parameters.VGG_LABELS[label_index]


def abnormalDetection(frame, camID, which="one"):
    """
    :param frame: 图像 
    :param camID: 摄像头信息
    :return: 异常信息
    """
    if which == "one":
        template = cv2.imread(Parameters.IMAGE_TEMPLATE + camID + ".jpg")
        differentRegions, diff = getDifferentRegions(template, frame)
    elif which == "two":
        differentRegions = getAbnormalRegions(frame)

    # if we need update template
    # if functions.judgeUpdateTemplate(frame,differentRegions):
    #    functions.isExistTempalte(camID, frame, cover=True)
    #    print("模板更新完毕")
    #    return [] ,diff

    camConfigFile = open(Functions.getProjectContext() + Parameters.IMAGE_CONFIG + camID + ".json")
    camConfig = json.load(camConfigFile)

    # 筛选变化区域
    differentRegions = differentRegionsFilter(differentRegions, camConfig["ROI"])

    # 判断异常类型
    # print("# 判断异常类型")

    res = [{"cam_id": camID, "type": judgeAbnormalType(frame[r[1]:r[1] + r[3], r[0]:r[0] + r[2]]), "x": r[0], "y": r[1],
            "w": r[2], "h": r[3]} for r in differentRegions]

    return res, diff


def calIOU(a, b):
    """
    :param a: box1 (x, y, w, h)
    :param b: box2
    :return:
    """
    w_intsec = np.maximum(0, (np.minimum(a[0] + a[2], b[0] + b[2]) - np.maximum(a[0], b[0])))
    h_intsec = np.maximum(0, (np.minimum(a[1] + a[3], b[1] + b[3]) - np.maximum(a[1], b[1])))
    s_intsec = w_intsec * h_intsec
    s_a = a[2] * a[3]
    s_b = b[2] * b[3]
    if float((s_a + s_b - s_intsec)) == 0.0 or float(s_intsec) == 0.0:
        return 0.0
    return float(s_intsec) / float((s_a + s_b - s_intsec))


def findTrueAbnormals(camID, abnormals, frame):
    """
    # 从log文件判断是否之前都有问题？存在时间超过设定阈值为异常，否则可能是移动目标干扰
    :param camID:
    :param abnormals:
    :return: 
    """

    print("检查真异常")
    # 将之前的异常载入内存
    import time
    import os

    nowDate = str(time.strftime("%Y-%m-%d", time.localtime()))
    nowDatePath = Functions.getProjectContext() + os.path.join(Parameters.CAMERA_LOG, nowDate)
    file = open(nowDatePath + "/" + camID + ".log", "r")
    preAbnormals = {}
    maxTime = 0
    minTime = sys.maxsize
    for line in file.readlines():
        elements = line.strip().split(" ")
        imgId = str(elements[0])
        time = int(elements[1])
        maxTime = max(time, maxTime)
        minTime = min(time, minTime)
        type = elements[2]
        x = int(elements[3])
        y = int(elements[4])
        w = int(elements[5])
        h = int(elements[6])
        # 根据时间戳将同一个场景下同一时刻的异常存到列表
        if preAbnormals.__contains__(time):
            preAbnormals[time].append((type, x, y, w, h, imgId, time))
        else:
            preAbnormals[time] = [(type, x, y, w, h, imgId, time)]

    if Parameters.debug:
        print("maxTime - minTime")
        print(maxTime - minTime)

    if maxTime - minTime < 6:  # 未达到规定时间的最小值，避免系统启动初期的误报
        print("return []")
        return []

    # revised by Hongwei Sun 20191211
    reportAbnormals = []
    for abnormal in abnormals:

        isOccurInAllPreOneTimeAbnormals = False

        for key in preAbnormals.keys():  # per time point

            haveSameAbnormal = False

            for preOneTimeAbnormal in preAbnormals[key]:

                # 当新检测到的异常的在之前存在时，退出当前检测

                if preOneTimeAbnormal[0] == abnormal["type"] and \
                        calIOU((preOneTimeAbnormal[1], preOneTimeAbnormal[2], preOneTimeAbnormal[3],
                                preOneTimeAbnormal[4]),
                               (abnormal["x"], abnormal["y"], abnormal["w"],
                                abnormal["h"])) > 0.5 and abs(
                    abnormal['time'] - preOneTimeAbnormal[
                        6]) > Parameters.abnormalMinTimeThreshold:  # need consider time diff

                    print('---', preOneTimeAbnormal[0] == abnormal["type"] and \
                          calIOU((preOneTimeAbnormal[1], preOneTimeAbnormal[2], preOneTimeAbnormal[3],
                                  preOneTimeAbnormal[4]),
                                 (abnormal["x"], abnormal["y"], abnormal["w"],
                                  abnormal["h"])) > 0.5 and abs(
                        abnormal['time'] - preOneTimeAbnormal[
                            6]) > Parameters.abnormalMinTimeThreshold)
                    haveSameAbnormal = True
                    abnormal['imgId'] = preOneTimeAbnormal[5]

                    break
            if haveSameAbnormal == True:
                isOccurInAllPreOneTimeAbnormals = True
                break

        # 将真异常添加进去
        # revised by mjs on 26th Dec: add 'and abnormal['score'] > 0.8'
        if isOccurInAllPreOneTimeAbnormals:  # and abnormal['score'] >= 0.8:
            print("add")
            reportAbnormals.append(abnormal)

    return reportAbnormals


if __name__ == "__main__":

    images = os.listdir(Functions.getProjectContext() + "Algorithm/Model/images/")

    for img in images:
        img_data = cv2.imread(Functions.getProjectContext() + "Algorithm/Model/images/" + img)

        judgeAbnormalType(img_data)
