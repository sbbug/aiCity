'''
这里用来处理服务接口里的逻辑
'''
import cv2
import time
import Algorithm.algorithms as alg
import Functions
import Parameters
import json
# from DeepDetect.FPN.FpnDetection import FpnDetection
import random
from multiprocessing import Process, Queue, Manager
from InterUtils import logWriter, filterReportedAbnormal, sendAbnormals, filterReportedAbnormalByFeature, \
    filterYesterdayReportedAbnormalByFeature
from InterUtils import FinalfilterReportedAbnormal
import numpy as np
import datetime

num = -1


# get some data in some time
def showGrid(key_imgs):
    print("key_imgs", len(key_imgs))
    '''
    :param key_imgs: dict of camera key:cam_id value:img_data
    :return: grid
    '''
    i = 1
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


def showSingleImage(manager, name, key):
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
        print("x:", x, "y:", y)
        i = x // 200
        j = y // 100
        num = j * 6 + i + 1
        print("num", num)

        # cv2.namedWindow(img_names[num])
        # cv2.startWindowThread()
        cv2.imshow(img_names[num], img_big_datas[img_names[num]])
        # cv2.waitKey(-1)
        # cv2.destroyWindow(img_names[num])
        # print("destroy")


# 消费者
def consumer(q, name, camera_num):
    img_small_datas = {}
    img_big_datas = {}
    img_names = {}
    manager = Manager()
    manager = manager.dict()
    global num
    while True:
        print("now queue size", q.qsize())
        # if full
        if q.full():
            print("queue clear")
            q.queue.clear()
        # update img
        if q.qsize() != 0:
            res = q.get()
            time.sleep(random.randint(1, 3))
            manager[res['cam_id'].split(".")[0]] = cv2.resize(res['frame'], (800, 500))
            img_names[int(res['cam_id'].split("_")[1])] = res['cam_id']
            img_big_datas[res['cam_id']] = cv2.resize(res['frame'], (800, 500))
            img_small_datas[res['cam_id']] = cv2.resize(res['frame'], (200, 100))
        else:
            print("wait producer")
            time.sleep(10)

        # show
        print("num img_small_datas", len(img_small_datas))

        if len(img_small_datas) == camera_num:
            print("start show camera grid")
            show = showGrid(img_small_datas)
            cv2.namedWindow("display")
            cv2.setMouseCallback("display", on_EVENT_LBUTTONDOWN, [img_names, img_big_datas])
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




# detect abnormal for UI show
def detectAbnormalForUI(fpnDetection, frame, camID, logger=None, frame_raw_image_path=None):
    # revised in 2019.11.21 by mjs: add time.clock()
    # revised in 2019.11.27 by mjs: add logger

    lines = []
    # get frame masked
    masked = frame

    if camID in Parameters.NEED_MASKED:
        masked = Functions.getMasked(frame, camID)
    else:
        masked = frame

    logger.info("FPN detect")
    start = time.perf_counter()
    abnormals = fpnDetection.detectAbnormalsByMutilScale(masked, camID)
    end = time.perf_counter()
    line = 'fpnDetection.detectAbnormalsByMutilScale: the runtime is: ' + str(end - start) + '\n'
    lines.append(line)
    # print(line)

    # print("abnormals")
    logger.info("abnormals:{}".format(abnormals))

    # print(abnormals)

    if len(abnormals) == 0 and (not Parameters.debug):
        logger.info("当前摄像头{}无异常".format(camID))

    else:

        # 将假异常的图片以及bounding box写入日志
        logWriter(frame, camID, abnormals)

        start = time.perf_counter()
        # 判断是否之前都有问题？存在时间超过设定阈值为异常，否则可能是移动目标干扰,
        reportAbnormals = alg.findTrueAbnormals(camID, abnormals, frame)
        end = time.perf_counter()
        line = 'alg.findTrueAbnormals: the runtime is: ' + str(end - start) + '\n'
        # lines.append(line)
        if logger is not None:
            logger.info(line)
        # print(line)

        logger.info("reportAbnormals:{}".format(reportAbnormals))

        # 对于检测到的真异常再次进行过滤，筛选掉已经上报的异常
        logger.info("重复上报判断")

        start = time.perf_counter()
        reportingAbnormals = filterReportedAbnormal(camID, reportAbnormals)
        end = time.perf_counter()
        line = 'filterReportedAbnormal: the runtime is: ' + str(end - start) + '\n'
        # lines.append(line)
        if logger is not None:
            logger.info(line)
        # print(line)

        logger.info("reportingAbnormals{}".format(reportingAbnormals))

        # 通过异常的特征，时间错，类型进行重复上报判断
        # print("重复上报判断")
        # reportingAbnormals = filterReportedAbnormalByFeature(camID,reportAbnormals)
        print('prefilter:the number of abnormals=%d' % len(reportingAbnormals))
        #
        start = time.perf_counter()
        # 对0-10天重复上报的异常进行过滤
        # reportingAbnormals = FinalfilterReportedAbnormal(camID, reportingAbnormals)
        end = time.perf_counter()
        line = 'FinalfilterReportedAbnormal: the runtime is: ' + str(end - start) + '\n'
        # lines.append(line)
        if logger is not None:
            logger.info(line)
        # #print(line)

        # 对隔天重复上报的异常进行过滤
        logger.info("隔天重复上报的异常进行过滤")
        start = time.perf_counter()
        reportingAbnormals = filterYesterdayReportedAbnormalByFeature(camID, reportingAbnormals)
        end = time.perf_counter()
        line = 'filterYesterdayReportedAbnormalByFeature: the runtime is: ' + str(end - start) + '\n'
        # lines.append(line)
        if logger is not None:
            logger.info(line)
        # print(line)

        # reportingAbnormals = filterReportedAbnormal(camID, reportingAbnormals)
        # if len(reportingAbnormals) != 0:
        #     # save image detected abnormal
        #     Functions.copyDetectImageToReportedDataset(im_path=raw_image_path)
        start = time.perf_counter()
        # 将异常发送到对方系统
        sendAbnormals(frame, reportingAbnormals, camID, logger,frame_raw_image_path)
        end = time.perf_counter()
        line = 'sendAbnormals: the runtime is: ' + str(end - start) + '\n'
        # lines.append(line)
        if logger is not None:
            logger.info(line)
        # print(line)

        reportingAbnormalSet = []
        # debug
        if Parameters.debug == True:

            if Parameters.SHOW_REPORTED_ABNORMAL:
                # find abnormals that had been reported
                for abnormal in reportAbnormals:
                    topLeft = (abnormal['x'], abnormal['y'])
                    bottomRight = (abnormal['x'] + abnormal['w'], abnormal['y'] + abnormal['h'])
                    cv2.putText(frame, abnormal["type"], topLeft, cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 255), 2)
                    cv2.rectangle(frame, topLeft, bottomRight, (0, 255, 255), 2)

                    cv2.putText(masked, abnormal["type"], topLeft, cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 255), 2)
                    cv2.rectangle(masked, topLeft, bottomRight, (0, 255, 255), 2)
                    # cv2.rectangle(show_diff_frame, topLeft, bottomRight, (0, 191, 255), 2)
            # find new abnormals
            for abnormal in reportingAbnormals:
                topLeft = (abnormal['x'], abnormal['y'])
                bottomRight = (abnormal['x'] + abnormal['w'], abnormal['y'] + abnormal['h'])
                cv2.putText(frame, abnormal["type"], topLeft, cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 0, 0), 1)
                # cv2.rectangle(frame, topLeft, bottomRight, (255, 0, 0), 2)
                # topLeft = (abnormal['x']+5, abnormal['y']+5)
                cv2.putText(frame, str(abnormal['score']), topLeft, cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 1)
                # cv2.rectangle(masked, topLeft, bottomRight, (255, 0, 0), 2)

                reportingAbnormalSet.append(
                    {abnormal["type"]: frame[
                                       abnormal['y']:abnormal['y'] + abnormal['h'],
                                       abnormal['x']:abnormal['x'] + abnormal['w']
                                       ],
                     "score": abnormal['score']
                     }
                )

                # cv2.rectangle(show_diff_frame, topLeft, bottomRight, (0, 0, 255), 2)

    return frame, masked, reportingAbnormalSet





