import cv2
import numpy as np

np.set_printoptions(threshold=np.inf)
import Parameters
from Functions import getProjectContext
import time
import Algorithm.algorithms as alg
import os
import uuid
from Net import network
from Algorithm.Model.VggFeature import VggFeature
from operator import itemgetter
from Net import network_2
import Functions

# 将发生的异常写入到日志文件
def WriteErrorLog(error_time, error_content, error_location):
    try:
        logFile = open(Parameters.ERROR_LOG, 'a')
    except:
        print("错误日志文件打开异常")

    line = str(error_time) + "\t" + str(error_location) + "\t" + str(error_content)
    logFile.write(line)
    logFile.close()


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
        center = (r['x'] + r['w'] // 2, r['y'] + r['h'] // 2)
        isInROI = False
        for ROIContour in ROIContours:
            if cv2.pointPolygonTest(ROIContour, center, False) >= 0:
                isInROI = True
                break
        if isInROI == True:
            res.append(r)

    return res


def filterReportedAbnormal(camID, abnormals):
    '''
    :param camId: 当前正在检测的摄像头
    :param abnormals: 当前检测到的真异常
    :return:
    '''
    print("检测是否有重复上报异常")
    # 将之前的异常载入内存
    import time
    import os

    # 获取当前日期
    nowDate = str(time.strftime("%Y-%m-%d", time.localtime()))
    # 获取存储已上报异常的目录
    nowDatePath = getProjectContext() + os.path.join(Parameters.CAMERA_REPORTED, nowDate)

    # 先判断目录是否存在
    print(os.path.exists(nowDatePath + "/" + camID + ".log"))
    if not os.path.exists(nowDatePath + "/" + camID + ".log"):
        return abnormals

    file = open(nowDatePath + "/" + camID + ".log", "r")

    reportedAbnormals = []
    for line in file.readlines():
        elements = line.strip().split(" ")
        time = elements[0]
        type = str(elements[1])
        x = int(elements[2])
        y = int(elements[3])
        w = int(elements[4])
        h = int(elements[5])
        reportedAbnormals.append([type, x, y, w, h])

    reportingAbnormals = []
    maxIOU = -1.0
    nowIOU = 0.0
    for abnormal in abnormals:
        for reportedAbnormal in reportedAbnormals:
            if reportedAbnormal[0] == abnormal["type"]:
                nowIOU = alg.calIOU(
                    (reportedAbnormal[1], reportedAbnormal[2], reportedAbnormal[3], reportedAbnormal[4]),
                    (abnormal["x"], abnormal["y"], abnormal["w"], abnormal["h"]))

                maxIOU = max(nowIOU, maxIOU)
        # 如果新检测到的真异常区域与已上报的异常区域最大重叠值小于某阈值，则上报
        if maxIOU < Parameters.REPORT_IOU_REPORTED_THRESHOLD:
            reportingAbnormals.append(abnormal)

    return reportingAbnormals


def filterReportedAbnormal(camID, abnormals):
    '''
    :param camId: 当前正在检测的摄像头
    :param abnormals: 当前检测到的真异常
    :return:
    '''
    print("检测是否有重复上报异常")
    # 将之前的异常载入内存
    import time
    import os

    # 获取当前日期
    nowDate = str(time.strftime("%Y-%m-%d", time.localtime()))
    # 获取存储已上报异常的目录
    nowDatePath = getProjectContext() + os.path.join(Parameters.CAMERA_REPORTED, nowDate)

    # 先判断目录是否存在
    print(os.path.exists(nowDatePath + "/" + camID + ".log"))
    if not os.path.exists(nowDatePath + "/" + camID + ".log"):
        return abnormals

    file = open(nowDatePath + "/" + camID + ".log", "r")

    reportedAbnormals = []
    for line in file.readlines():
        elements = line.strip().split(" ")
        time = elements[0]
        type = str(elements[1])
        x = int(elements[2])
        y = int(elements[3])
        w = int(elements[4])
        h = int(elements[5])
        reportedAbnormals.append([type, x, y, w, h])

    reportingAbnormals = []
    maxIOU = -1.0
    nowIOU = 0.0
    for abnormal in abnormals:
        for reportedAbnormal in reportedAbnormals:
            if reportedAbnormal[0] == abnormal["type"]:
                nowIOU = alg.calIOU(
                    (reportedAbnormal[1], reportedAbnormal[2], reportedAbnormal[3], reportedAbnormal[4]),
                    (abnormal["x"], abnormal["y"], abnormal["w"], abnormal["h"]))

                maxIOU = max(nowIOU, maxIOU)
        # 如果新检测到的真异常区域与已上报的异常区域最大重叠值小于某阈值，则上报
        if maxIOU < Parameters.REPORT_IOU_REPORTED_THRESHOLD:
            reportingAbnormals.append(abnormal)

    return reportingAbnormals


# writed in 2019.11.19 by mjs
def getEventclass():
    import requests
    import json
    from Parameters import EVENT_URL
    try:
        cate = dict()
        category = requests.get(EVENT_URL)
        res = json.loads(category.text)
        for index in res['data']:
            cate[index['id']] = index['event_name']
        if res['code'] != 10001:
            print("获取事件列表时出现异常")
        else:
            pass

        return cate
    except Exception as e:
        print("Get Data Erorr: ", e)


# writed in 2019.11.19 by mjs
def getDayNumber(date):
    '''
    :param date:like '2017-10-20'
    :return: int
    '''
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    date = date.split('-')
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    result = 0
    for i in range(month - 1):
        result += days[i]
    result += day

    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        result += 1

    return result


# writed in 2019.11.19 by mjs
def FinalfilterReportedAbnormal(camID, abnormals):
    '''
    :param camId: 当前正在检测的摄像头
    :param abnormals: 当前检测到的真异常
    :return:
    '''
    print("检测是否有重复上报异常-final")
    # 将之前的异常载入内存
    import time
    from DB.SQL_Init import SQLI
    from Functions import isType
    from Parameters import DATA
    # 获取当前日期
    nowDate = str(time.strftime("%Y-%m-%d", time.localtime()))
    # print(camID)
    # get category
    class_dict = DATA

    start = time.perf_counter()
    # create mysql object
    SQL_OB = SQLI('root', '123456Pa!', 'test')
    sql = 'select meta, exist_problem, event_cate_id, path from feedback where camId="{}"'.format(camID)
    res = list(SQL_OB.find(sql))
    SQL_OB.close()
    print('SQL search runtime is: {}'.format(time.perf_counter() - start))

    reportedAbnormals = []
    for meta, exist_problem, event, path in res:
        try:
            type = isType(str(class_dict[event]))

            meta = meta.split(',')
            # print(meta)

            # some meta[0] is started with '[', so we need to process
            if str(meta[0]).startswith('['):
                x = int(meta[0][1:])
            else:
                x = int(meta[0])

            y = int(meta[1])
            w = int(meta[2])

            # some meta[3] is ended with ']', so too
            if str(meta[3]).endswith(']'):
                h = int(meta[3][:-1])
            else:
                h = int(meta[3])
            path = path[0:path.rfind('/')]
            time = path[path.rfind('/') + 1:]

            T1 = getDayNumber(time)
            T2 = getDayNumber(nowDate)
            # revised by shw on 28th Nov
            # revised by mjs on 26th Dec
            if 0 <= T2 - T1 <= 15 and ~int(exist_problem):
                reportedAbnormals.append([type, x, y, w, h])
        except:
            print(exist_problem)
            # pass
            # print(event)
            # print(event, class_dict[event])

    reportingAbnormals = []
    maxIOU = -1.0
    nowIOU = 0.0
    for abnormal in abnormals:
        for reportedAbnormal in reportedAbnormals:
            if reportedAbnormal[0] == abnormal["type"]:
                nowIOU = alg.calIOU(
                    (reportedAbnormal[1], reportedAbnormal[2], reportedAbnormal[3], reportedAbnormal[4]),
                    (abnormal["x"], abnormal["y"], abnormal["w"], abnormal["h"]))

                maxIOU = max(nowIOU, maxIOU)
        # 如果新检测到的真异常区域与已上报的异常区域最大重叠值小于某阈值，则上报
        if maxIOU < Parameters.REPORT_IOU_REPORTED_THRESHOLD:
            reportingAbnormals.append(abnormal)
    print("filter-ed:The number of reportingAbnormals=%d" % len(reportingAbnormals))
    return reportingAbnormals


def calSimilarity(a, b):
    return np.sqrt(np.sum(np.square(a - b)))


def filterYesterdayReportedAbnormalByBoxes(camID, reportingAbnormals):
    if len(reportingAbnormals) == 0:
        return []

    false_path = os.path.join(getProjectContext(), Parameters.FALSE_ABNORMAL_PATH)
    camera_path = os.path.join(false_path, camID)
    print(camera_path)
    if not os.path.exists(camera_path):
        return reportingAbnormals

    file_path = os.path.join(camera_path, "falseFeature.log")
    false_yesterday_file_handler = open(file_path, "r")

    false_abnormals = []
    line = false_yesterday_file_handler.readline()

    while line:
        note = eval(line.replace("\n", ""))
        false_abnormals.append(note)
        line = false_yesterday_file_handler.readline()

    false_yesterday_file_handler.close()

    # report these abnormal
    report_these_abnormal = []
    vgg = VggFeature()
    nowDate = str(time.strftime("%Y-%m-%d", time.localtime()))
    nowDatePath = getProjectContext() + os.path.join(Parameters.CAMERA_LOG, nowDate)
    nowImgPath = os.path.join(nowDatePath, camID)

    for abnormal in reportingAbnormals:

        img_path = os.path.join(nowImgPath, str(abnormal['imgId']) + ".jpg")
        img_data = cv2.imread(img_path)

        detect_object = img_data[
                        abnormal['y']:abnormal['y'] + abnormal['h'],
                        abnormal['x']:abnormal['x'] + abnormal['w']
                        ]
        now_feature = vgg.getFeature(detect_object).detach().cpu().numpy()[0]
        # if sift
        flag = False
        for false_abnormal in false_abnormals:
            similarity = calSimilarity(now_feature, false_abnormal['feature'])
            print("similarity", similarity)
            if similarity < 9:
                flag = True
                break

        if flag == False:
            report_these_abnormal.append(abnormal)

    return report_these_abnormal


def filterYesterdayReportedAbnormalByFeature(camID, reportingAbnormals):
    if len(reportingAbnormals) == 0:
        return []

    false_path = os.path.join(getProjectContext(), Parameters.FALSE_ABNORMAL_PATH)
    camera_path = os.path.join(false_path, camID)
    print(camera_path)
    if not os.path.exists(camera_path):
        return reportingAbnormals

    file_path = os.path.join(camera_path, "falseFeature.log")
    false_yesterday_file_handler = open(file_path, "r")

    false_abnormals = []
    line = false_yesterday_file_handler.readline()

    while line:
        note = eval(line.replace("\n", ""))
        false_abnormals.append(note)
        line = false_yesterday_file_handler.readline()

    false_yesterday_file_handler.close()

    # report these abnormal
    report_these_abnormal = []
    vgg = VggFeature()
    nowDate = str(time.strftime("%Y-%m-%d", time.localtime()))
    nowDatePath = getProjectContext() + os.path.join(Parameters.CAMERA_LOG, nowDate)
    nowImgPath = os.path.join(nowDatePath, camID)

    for abnormal in reportingAbnormals:

        img_path = os.path.join(nowImgPath, str(abnormal['imgId']) + ".jpg")
        img_data = cv2.imread(img_path)

        detect_object = img_data[
                        abnormal['y']:abnormal['y'] + abnormal['h'],
                        abnormal['x']:abnormal['x'] + abnormal['w']
                        ]
        now_feature = vgg.getFeature(detect_object).detach().cpu().numpy()[0]
        # if sift
        flag = False
        for false_abnormal in false_abnormals:
            similarity = calSimilarity(now_feature, false_abnormal['feature'])
            print("similarity", similarity)
            if similarity < 9:
                flag = True
                break

        if flag == False:
            report_these_abnormal.append(abnormal)

    return report_these_abnormal


def filterReportedAbnormalByFeature(camID, report_abnormals):
    '''
    :param camID:
    :param report_abnormals:
    :return:
    '''
    if len(report_abnormals) == 0:
        return []
    print("=================================", len(report_abnormals))
    # 将异常重新封装到指定的数据格式，然后传输到对方系统
    nowDate = str(time.strftime("%Y-%m-%d", time.localtime()))
    nowDatePath = getProjectContext() + os.path.join(Parameters.CAMERA_LOG, nowDate)
    nowImgPath = os.path.join(nowDatePath, camID)

    # abnormal store log
    vgg = VggFeature()
    old_abnormals = []
    new_abnormals = []
    need_write_log_abnormals = []

    # read old abnormals to list
    '''
   
    '''
    if os.path.isfile(nowDatePath + "/" + camID + ".txt"):
        file = open(nowDatePath + "/" + camID + ".txt", "r")
        line = file.readline()
        while line:
            line = line.replace("\n", "")
            note = eval(line)
            old_abnormals.append(note)
            line = file.readline()
        file.close()

    if len(old_abnormals) != 0:

        for abnormal in report_abnormals:
            flag = False
            img_path = os.path.join(nowImgPath, str(abnormal['imgId']) + ".jpg")
            img_data = cv2.imread(img_path)

            detect_object = img_data[
                            abnormal['y']:abnormal['y'] + abnormal['h'],
                            abnormal['x']:abnormal['x'] + abnormal['w']
                            ]
            now_feature = vgg.getFeature(detect_object).detach().cpu().numpy()[0]

            for old_abnormal in old_abnormals:

                # np.sqrt(np.sum(np.square(f1[0] - f2[0])))
                similarity = calSimilarity(now_feature, old_abnormal['feature'])
                print("similarity", similarity)
                if similarity < 5 \
                        and abnormal['type'] == old_abnormal['type']:
                    flag = True
                    break

            if flag == False:
                new_abnormals.append(abnormal)
                need_write_log_abnormal = {}
                need_write_log_abnormal['time'] = abnormal['time']
                need_write_log_abnormal['type'] = abnormal['type']
                need_write_log_abnormal['feature'] = now_feature.tolist()
                need_write_log_abnormals.append(need_write_log_abnormal)


    else:
        for abnormal in report_abnormals:
            img_path = os.path.join(nowImgPath, str(abnormal['imgId']) + ".jpg")

            img_data = cv2.imread(img_path)
            detect_object = img_data[abnormal['y']:abnormal['y'] + abnormal['h'],
                            abnormal['x']:abnormal['x'] + abnormal['w']]
            now_feature = vgg.getFeature(detect_object).detach().cpu().numpy()[0]

            new_abnormals.append(abnormal)
            need_write_log_abnormal = {}
            need_write_log_abnormal['time'] = abnormal['time']
            need_write_log_abnormal['type'] = abnormal['type']
            need_write_log_abnormal['feature'] = now_feature.tolist()
            need_write_log_abnormals.append(need_write_log_abnormal)

    # write log to disk
    write_abnormals_to_disk = old_abnormals + need_write_log_abnormals

    # sort by time
    write_abnormals_to_disk = sorted(write_abnormals_to_disk, key=itemgetter('time'), reverse=True)
    # write_abnormals_to_disk = sorted(write_abnormals_to_disk.items(), key=lambda x: x[1], reverse=True)

    #
    file = open(nowDatePath + "/" + camID + ".txt", "w")
    for write_abnormal_to_disk in write_abnormals_to_disk:
        file.write(str(write_abnormal_to_disk) + "\n")
    file.close()

    return new_abnormals


def logRepoterAbnormalWrite(camID, abnormals):
    '''
    :param camID: 摄像头编号
    :param abnormals: 异常区域
    :return:
    '''
    nowDate = str(time.strftime("%Y-%m-%d", time.localtime()))
    nowDatePath = getProjectContext() + os.path.join(Parameters.CAMERA_REPORTED, nowDate)

    if not os.path.exists(nowDatePath):
        os.makedirs(nowDatePath)

    # 将已经上报的异常保存到当前日志中
    logPath = nowDatePath + "/" + camID + ".log"
    print("++++++++++++++++++++++++++++")
    print(abnormals)
    logFile = open(logPath, 'a')
    content = []
    for abnormal in abnormals:
        detectAbnormalTime = str(abnormal['time'])
        x = str(abnormal["x"])
        y = str(abnormal["y"])
        w = str(abnormal["w"])
        h = str(abnormal["h"])
        logFile.write(
            str(detectAbnormalTime) + " " + abnormal["type"] + " " + x + " " + y + " " + w + " " + h + " " + abnormal[
                'imgId'] + "\n")
    for line in content:
        logFile.write(line)

    logFile.close()


# 对于上报过的异常我们需要进行存档，防止重复上报异常
def sendAbnormals(frame, abnormals, camID,logger,frame_raw_image_path):
    '''
    :param frame: 当前帧数据
    :param abnormals: 异常集合
    :param camID: 摄像头id
    :return:
    '''
    logger.info("================================={}".format(len(abnormals)))

    # 将异常重新封装到指定的数据格式，然后传输到对方系统
    nowDate = str(time.strftime("%Y-%m-%d", time.localtime()))
    nowDatePath = getProjectContext() + os.path.join(Parameters.CAMERA_LOG, nowDate)
    nowImgPath = os.path.join(nowDatePath, camID)
    # j = 0
    flag = False
    for abnormal in abnormals:
        # 获取当前帧的图片路径
        img_path = os.path.join(nowImgPath, str(abnormal['imgId']) + ".jpg")

        if flag is False:
            # save image detected abnormal
            Functions.copyDetectImageToReportedDataset(im_path=frame_raw_image_path,new_image_name=str(abnormal['imgId'])+".jpg")
            flag = True
        # img_path = "./f17da2da-163e-3158-b41b-34d50e9341d1.jpg"
        # img = cv2.imread(img_path)
        # cv2.imshow("{}".format(j),img)
        # j += 1
        if Parameters.NETWORK:
            #
            try:
                network.sendAbormalsToIt(abnormal, img_path,logger)
            except:
                pass
            # city manager web server
            try:
                network_2.sendAbormalsToIt(abnormal, img_path,logger)
            except:
                pass

    # 将已经上报的异常存储起来，用于过滤
    if len(abnormals) != 0:
        print("将已经上报的异常存档")
        logRepoterAbnormalWrite(camID, abnormals)


def logWriter(frame, camID, abnormals):
    """
    异常日志记录
    :param frame:
    :param camID:
    :param abnormals:
    :return:
    """

    # color space transform
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    nowDate = str(time.strftime("%Y-%m-%d", time.localtime()))
    nowDatePath = getProjectContext() + os.path.join(Parameters.CAMERA_LOG, nowDate)

    # 如果当前目录不存在创建一个新的目录
    if not os.path.exists(nowDatePath):
        os.makedirs(nowDatePath)

    # 获取uuid,使其具有唯一标识
    namespace = uuid.NAMESPACE_OID
    imgId = uuid.uuid3(namespace, str(time.time()))

    # 存图
    nowImgPath = os.path.join(nowDatePath, camID)
    if not os.path.exists(nowImgPath):
        os.makedirs(nowImgPath)
    # imageNum = len([name for name in os.listdir(nowImgPath) if os.path.isfile(os.path.join(nowImgPath, name))])
    cv2.imwrite(os.path.join(nowImgPath, str(imgId) + ".jpg"), frame)

    # 存日志
    logPath = nowDatePath + "/" + camID + ".log"
    content = []
    # 只保存最近的几条纪录，提升查询效率
    # 将最近时间段内的记录保存到content里
    if os.path.exists(logPath):
        logFile = open(logPath, 'r')
        lines = logFile.readlines()
        # 获取当前时间
        imgTime = int(time.time())
        for line in lines:
            if imgTime - int(line.split(" ")[1]) < Parameters.LOG_REFRESH_FRE:  # 30min
                content.append(line)
        logFile.close()

    logFile = open(logPath, 'w')
    for abnormal in abnormals:
        x = str(abnormal["x"])
        y = str(abnormal["y"])
        w = str(abnormal["w"])
        h = str(abnormal["h"])
        logFile.write(str(imgId) + " " + str(abnormal["time"]) + " " + abnormal[
            "type"] + " " + x + " " + y + " " + w + " " + h + "\n")
    for line in content:
        logFile.write(line)

    logFile.close()
