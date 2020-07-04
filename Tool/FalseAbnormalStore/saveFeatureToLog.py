import requests
import Parameters
import json
import Functions
import cv2
import time
import re
import os
from Algorithm.Model.VggFeature import VggFeature
from Tool.FalseAbnormalStore.getFalseAbnormalToLog import findImagePath,getCameraNo
import numpy as np
np.set_printoptions(threshold=np.inf)
falseAbnormalPath = "../../Resources/ReportLog/FalseAbnormal"

if __name__ =="__main__":

    false_file = open("FalseAbnormalsRecord.log","r")
    False_abnormal_set = []

    record = false_file.readline()
    while record:
        ele = record.replace("\n","").split(" ")
        abnormal = {}
        abnormal['id'] = int(ele[0])
        abnormal['picture_no'] =ele[1]
        abnormal['x'] = int(ele[2])
        abnormal['y'] = int(ele[3])
        abnormal['w'] = int(ele[4])
        abnormal['h'] = int(ele[5])
        False_abnormal_set.append(abnormal)
        record = false_file.readline()

    print("finish read")

    print("start calculate feature")
    vgg = VggFeature()

    will_write_to_log = {}
    for abnormal in False_abnormal_set:

        print(abnormal['picture_no'])
        img_path = findImagePath(abnormal['picture_no'])

        if img_path != "":
            print(img_path)
            record_abnormal = {}
            object_data = cv2.imread(img_path)[abnormal['y']:abnormal['y'] + abnormal['h'], abnormal['x']:abnormal['x']+ abnormal['w']]
            feature = vgg.getFeature(object_data).detach().cpu().numpy()[0]
            feature = feature.tolist()
            record_abnormal['time'] = str(int(time.time()))
            record_abnormal['feature'] = feature

            camera_no = getCameraNo(img_path)

            if not will_write_to_log.__contains__(camera_no):
                will_write_to_log[camera_no] = [record_abnormal]
            else:
                will_write_to_log[camera_no].append(record_abnormal)

    print(will_write_to_log)

    for cam_id in will_write_to_log.keys():

        # write to file
        now_date_path = os.path.join(falseAbnormalPath, cam_id)
        if not os.path.exists(now_date_path):
            os.makedirs(now_date_path)

        false_file = os.path.join(now_date_path, "falseFeature.log")

        false_file_handler = None
        if os.path.exists(false_file):
            false_file_handler = open(false_file, "a")
        else:
            false_file_handler = open(false_file, "w")

        for feature_record in will_write_to_log[cam_id]:

            false_file_handler.write(str(feature_record) + "\n")

        false_file_handler.close()