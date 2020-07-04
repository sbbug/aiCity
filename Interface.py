'''
这里用来处理服务接口里的逻辑
'''
import cv2
import time
import Algorithm.algorithms as alg
import Functions
import Parameters
import json
from DeepDetect.FPN.FpnDetect import FpnDetection
import random
from multiprocessing import Process,Queue,Manager
from InterUtils import logWriter,filterReportedAbnormal,sendAbnormals,filterReportedAbnormalByFeature,filterYesterdayReportedAbnormalByFeature
import numpy as np

num = -1

# get some data in some time
def showGrid(key_imgs):
    print("key_imgs",len(key_imgs))
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
                row = np.hstack(temp)
                rows.append(row)
                break
            temp.append(np.zeros((100, 200, 3), np.uint8))


    show = np.vstack(rows)

    return show
def showSingleImage(manager,name,key):
    print(manager)
    print(key)
    print("show single image")
    cv2.imshow("single camera", manager[key])
    cv2.waitKey(-1)
    print("end show single image")


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):

    # global num
    img_names = param[0]
    img_big_datas = param[1]
    if event == cv2.EVENT_LBUTTONDOWN:

        # print(img_big_datas)
        # print(img_names)
        xy = "%d,%d" % (x, y)
        print("x:",x,"y:",y)
        i = x // 200
        j = y // 100
        num = j*6+i+1
        print("num",num)

        #cv2.namedWindow(img_names[num])
        #cv2.startWindowThread()
        cv2.imshow(img_names[num],img_big_datas[img_names[num]])
        #cv2.waitKey(-1)
        #cv2.destroyWindow(img_names[num])
        #print("destroy")

# 消费者
def consumer(q,name,camera_num):

    img_small_datas = {}
    img_big_datas = {}
    img_names = {}
    manager = Manager()
    manager = manager.dict()
    global num
    while True:
        # if full
        if q.full():
            print("queue clear")
            q.queue.clear()
        # update img
        if q.qsize()!=0:
            res = q.get()
            time.sleep(random.randint(1,3))
            manager[res['cam_id'].split(".")[0]] = cv2.resize(res['frame'], (800, 500))
            img_names[int(res['cam_id'].split("_")[1])] = res['cam_id']
            img_big_datas[res['cam_id']] = cv2.resize(res['frame'], (800, 500))
            img_small_datas[res['cam_id']] = cv2.resize(res['frame'], (200, 100))
        else:
            print("wait producer")
            time.sleep(10)

        # show
        print("num img_small_datas",len(img_small_datas))

        if len(img_small_datas) == camera_num:
            print("start show camera grid")
            show = showGrid(img_small_datas)
            cv2.namedWindow("display")
            cv2.setMouseCallback("display", on_EVENT_LBUTTONDOWN,[img_names,img_big_datas])
            # print(num)
            # if num!= -1:
            #     show_single_img_process = Process(target=showSingleImage,
            #                                       args=(manager,"show_single_image",img_names[num]))
            #
            #     show_single_img_process.start()
            #     show_single_img_process.join()
            #     num = -1
            #
            # print("quit")
            cv2.imshow("display", show)
            cv2.waitKey(10)

# 生产者
def producer(q,name):

    FpnDetect = FpnDetection()
    ipConfig = Functions.loadIPConfig(Functions.getProjectContext() + Parameters.CAMERAS_CONFIG)
    now = -1
    camera_num = len(ipConfig)

    while now < camera_num:
        now += 1
        now = now % camera_num
        camID = ipConfig[now]["cam_id"]
        camUrl = Functions.getCameraUrl(ipConfig[now])
        cap = cv2.VideoCapture(camUrl)

        print("当前检测的摄像头", camID)
        if cap.isOpened() == False:
            print("%s is not opened!", camID)
            res = {"cam_id": camID, "frame": np.zeros((1280, 720, 3), np.uint8)}
            q.put(res)
            continue
        ret, frame = cap.read()
        cap.release()

        print("FPN detect ")
        abnormals = FpnDetect.detectAbnormalsByMutilScale(frame,camID)

        print("abnormals")
        print(abnormals)

        if len(abnormals) == 0 and (not Parameters.debug):
            print("当前摄像头无异常", camID)
            continue  # normal

        # 将假异常的图片以及bounding box写入日志
        logWriter(frame, camID, abnormals)

        # 判断是否之前都有问题？存在时间超过设定阈值为异常，否则可能是移动目标干扰,
        reportAbnormals = alg.findTrueAbnormals(camID, abnormals, frame)
        print("reportAbnormals")
        print(reportAbnormals)

        # 对于检测到的真异常再次进行过滤，筛选掉已经上报的异常
        print("重复上报判断")
        reportingAbnormals = filterReportedAbnormal(camID, reportAbnormals)

        # print("reportingAbnormals")
        # print(reportingAbnormals)

        # 通过异常的特征，时间错，类型进行重复上报判断
        # print("重复上报判断")
        # reportingAbnormals = filterReportedAbnormalByFeature(camID,reportAbnormals)

        # 对隔天重复上报的异常进行过滤
        print("隔天重复上报的异常进行过滤")
        reportingAbnormals = filterYesterdayReportedAbnormalByFeature(camID,reportingAbnormals)

        #reportingAbnormals = filterReportedAbnormal(camID, reportingAbnormals)

        # 将异常发送到对方系统
        # sendAbnormals(frame, reportingAbnormals, camID)

        # debug
        if Parameters.debug == True:

            # show_diff_frame = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
            # 绘制ROI
            #camConfigFile = open(functions.getProjectContext() + parameters.IMAGE_CONFIG + camID + ".json")
            #config = json.load(camConfigFile)
            # for points in config['ROI']:
            #     for i in range(len(points) - 1):
            #         cv2.circle(frame, (points[i][0], points[i][1]), 5, (255, 0, 0), thickness=-1)
            #         cv2.line(frame, (points[i][0], points[i][1]), (points[i + 1][0], points[i + 1][1]),
            #                  (255, 0, 0), 2)
            #         cv2.circle(frame, (points[i + 1][0], points[i + 1][1]), 5, (255, 0, 0), thickness=-1)
            # # 绘制所有异常,包括假异常
            # for abnormal in abnormals:
            #     topLeft = (abnormal['x'], abnormal['y'])
            #     bottomRight = (abnormal['x'] + abnormal['w'], abnormal['y'] + abnormal['h'])
            #     cv2.putText(frame, abnormal["type"], topLeft, cv2.FONT_HERSHEY_SIMPLEX, 1,
            #                 (0, 255, 0), 2)
            #     cv2.rectangle(frame, topLeft, bottomRight, (0, 255, 0), 2)
            #     # cv2.rectangle(show_diff_frame, topLeft, bottomRight, (0, 255, 0), 2)

            # find abnormals
            for abnormal in reportAbnormals:
                topLeft = (abnormal['x'], abnormal['y'])
                bottomRight = (abnormal['x'] + abnormal['w'], abnormal['y'] + abnormal['h'])
                cv2.putText(frame, abnormal["type"], topLeft, cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 255), 2)
                cv2.rectangle(frame, topLeft, bottomRight, (0, 255, 255), 2)
                # cv2.rectangle(show_diff_frame, topLeft, bottomRight, (0, 191, 255), 2)
            # find new abnormals
            s = 0
            for abnormal in reportingAbnormals:
                topLeft = (abnormal['x'], abnormal['y'])
                bottomRight = (abnormal['x'] + abnormal['w'], abnormal['y'] + abnormal['h'])
                cv2.putText(frame, abnormal["type"], topLeft, cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)
                cv2.rectangle(frame, topLeft, bottomRight, (0, 0, 255), 2)
                # cv2.rectangle(show_diff_frame, topLeft, bottomRight, (0, 0, 255), 2)
        res = {"cam_id":camID,"frame":frame}

        q.put(res)

        time.sleep(random.randint(1, 3))

def run():

    ipConfig = Functions.loadIPConfig(Functions.getProjectContext() + Parameters.CAMERAS_CONFIG)
    camera_num = len(ipConfig)
    # shared queue
    q = Queue()
    # detect process
    detect_process = Process(target=producer, args=(q, "producer"))
    # display frame procee
    display_process = Process(target=consumer, args=(q, 'consumer',camera_num))

    detect_process.start()
    display_process.start()

    detect_process.join()
    display_process.join()


if __name__ =="__main__":
    run()