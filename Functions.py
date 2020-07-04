'''
项目中需要用到的工具方法
'''

import numpy as np
import cv2
import os
import Parameters
import json
from scipy import spatial
import shutil


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


# 加载摄像头基本信息
def loadIPConfig(camera_config_path):
    '''
    :param camera_config_path:摄像头属性配置文件路径
    :return: 摄像头配置列表
    '''
    file = open(camera_config_path, encoding="utf-8")
    result = json.load(file)
    cameras = [c for c in result['cameras']]

    return cameras


# 加载摄像头基本信息
def loadTargetIPConfig(camera_config_path):
    '''
    :param camera_config_path:摄像头属性配置文件路径
    :return: 摄像头配置列表
    '''
    file = open(camera_config_path, encoding="utf-8")
    result = json.load(file)
    cameras = [c for c in result['cameras'] if c['cam_id'] in Parameters.detect_cameras]

    return cameras


# 传入摄像头相关的信息，然后返回一个url地址
def getCameraUrl(info, camera_proto="rtsp"):
    if info['username'] == '':
        return info['ip']

    camera_url = camera_proto + "://" + info['username'] + ":" + info['password'] + "@" + info['ip'] + ":" + info[
        'port'] + "/"
    return camera_url


# 根据摄像头编号寻找每一个摄像头下的ROI配置信息
def getSpacesList(camera_id):
    """  
    :param camera_id: 
    :return: 
    """
    # 文件异常处理
    try:
        file = open(Parameters.IMAGE_CONFIG + str(camera_id) + ".json")
    except IOError:
        print("Error: 没有找到文件或读取文件失败")

    result = json.load(file)
    spaces = []
    for s in result['spaces']:
        spaces.append(result['spaces'][s])

    return spaces


# 生成图像模板，图像名字是cam_id
def isExistTempalte(camera_id, img_tpl=None, cover=False):
    '''
    :param img_tpl: 传入当前摄像头下的模板图像
    :param camera_id: 摄像头对应的编号
    :param cover: 是否覆盖，默认False不覆盖
    :return:
    '''
    now_path = getProjectContext() + Parameters.IMAGE_TEMPLATE + camera_id + ".jpg"

    # 如果当前模板文件不存在，则将模板存进去
    if os.path.exists(now_path) == False:
        cv2.imwrite(now_path, img_tpl)

    # 如果cover==True,说明需要覆盖
    if cover == True:
        cv2.imwrite(now_path, img_tpl)

    # 返回当前模板的图像
    return cv2.imread(now_path)


# 获取项目目录里的的根目录绝对位置,比如:G:\公司项目\现在\垃圾异常检测项目\代码\new\CityManager
# 仅支持英文路径
def getProjectContext():
    # 获取当前文件路径
    current_path = os.path.abspath(__file__)
    # 获取当前文件的父目录
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".") + "/"
    return father_path.replace("\\", "/")


def isType(str_1):
    if str_1 == "暴露垃圾":
        return "ExposedTrash"
    elif str_1 == "乱设或损坏户外设施":
        return "UoDofacilities"
    elif str_1 == "擅自占用道路堆物、施工":
        return "UORoads"
    elif str_1 == "占道无证经营、跨门营业":
        return "IllegalStand"
    elif str_1 == "ExposedTrash" or str_1 == "exposedTrash":
        return "暴露垃圾"
    elif str_1 == "UoDOFacilities" or str_1 == "uoDoFacility":
        return "乱设或损坏户外设施"
    elif str_1 == "UORoads" or str_1 == "uoRoad":
        return "擅自占用道路堆物、施工"
    elif str_1 == "IllegalStand" or str_1 == "illegalStand":
        return "占道无证经营、跨门营业"


# 对图像进行gamma变换
def adjustGamma(image, gamma=1.0):
    return ((np.power(image / 255.0, 1.0 / gamma)) * 255.0).astype("uint8")


def judgeUpdateTemplate(frame, abnormals, flag=True):
    '''
    :param frame: 当前帧
    :param abnormals: 异常位置集合
    :param camId: 摄像头编号
    :return:
    '''
    # print("num of abnormal ",len(abnormals))
    # if len(abnormals)!=0 and len(abnormals) > parameters.DIFF_REGION_NUM:
    #     return True

    h, w, _ = frame.shape
    a = [0, 0, w, h]

    updateThreold = 0.0
    if flag:
        updateThreold = Parameters.TPL_UPDATE_TURE_THREOLD
    else:
        updateThreold = Parameters.TPL_UPDATE_FALSE_THREOLD

    for abnormal in abnormals:

        b = [abnormal[0], abnormal[1], abnormal[2], abnormal[3]]
        res = calIOU(a, b)
        print("res", res)
        if res > updateThreold:
            return True
    return False


def copyDetectImageToReportedDataset(im_path, new_image_name):
    if im_path is None or not os.path.exists(im_path):
        return

    shutil.copy(im_path, os.path.join(getProjectContext() + Parameters.REPORTED_DATASET_PATH, new_image_name))


def getMasked(frame, camId):
    mask_path = os.path.join(getProjectContext() + "./Resources/mask", camId + ".jpg")

    assert os.path.exists(mask_path), 'the mask do not exist'

    mask = cv2.imread(mask_path)

    masked = cv2.bitwise_and(frame, frame, mask=mask[:, :, 0])

    return masked


def distance(v1, v2, d_type='d1'):
    assert v1.shape == v2.shape, "shape of two vectors need to be same!"

    if d_type == 'd1':
        return np.sum(np.absolute(v1 - v2))
    elif d_type == 'd2':
        return np.sum((v1 - v2) ** 2)
    elif d_type == 'd2-norm':
        return 2 - 2 * np.dot(v1, v2)
    elif d_type == 'd3':
        pass
    elif d_type == 'd4':
        pass
    elif d_type == 'd5':
        pass
    elif d_type == 'd6':
        pass
    elif d_type == 'd7':
        return 2 - 2 * np.dot(v1, v2)
    elif d_type == 'd8':
        return 2 - 2 * np.dot(v1, v2)
    elif d_type == 'cosine':
        return spatial.distance.cosine(v1, v2)
    elif d_type == 'square':
        return np.sum((v1 - v2) ** 2)


if __name__ == "__main__":
    # print(uploadImage("./test/camera_1.jpg"))
    # insertCamera()
    # print(getEventCode())
    # uploadImage(getProjectContext()+parameters.IMAGE_TEMPLATE+"camera_1.jpg")
    # WriteErrorLog("","","")
    print(getProjectContext())

    copyDetectImageToReportedDataset(getProjectContext() + "Mycopy1.py", getProjectContext() + "h.py")
