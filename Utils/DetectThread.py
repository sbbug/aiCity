from PyQt5.QtCore import *
import time
from Interface2 import detectAbnormalForUI
from Functions import getProjectContext
# from DeepDetect.FPN.FpnDetection import FpnDetection
from DeepDetect.CascadeDetection import CascadeDetection
import cv2
import Parameters
# from newMainWindow import abnormals
from Utils.par import abnormals
from Camera.FtpServer import FtpServer
from Parameters import HTTP_CAMERAS
from Camera.HttpCamera import HttpCamera
from queue import Queue
import base64
import asyncio
import websockets
import threading
import requests
import json


class DetectThread(QThread):
    # revised in 2019.11.21 by mjs: add time.clock()

    slot = pyqtSignal(bytes)

    def __init__(self, parent, cameras_rtsp, cameras_image, logger):
        QThread.__init__(self, parent=parent)

        # self.detection = FpnDetection()
        self.detection = CascadeDetection()
        self.cameras_rtsp = cameras_rtsp
        self.cameras_image = cameras_image
        self.logger = logger
        # ftp server info
        self.ftp_server = FtpServer("121.43.182.244", 'ftpuser', 'Lawatlas2018')
        self.ftp_cameras = ["camera_51"]

        self.websocket_queue = Queue(50)

        self.send_thread = threading.Thread(target=self.run_send_detect_thread)
        self.send_thread.start()

    def run(self):

        while True:

            # get frame from video stream
            for camera in self.cameras_rtsp:
                img = camera.readDetectQ()
                # img = camera.img_detect
                cam_id = camera.cam_id

                if img is not None and cam_id in Parameters.DETECT_CAMERAS:
                    encodeRgbImage = self.detect_frame(img, cam_id)
                    self.slot.emit(encodeRgbImage)
                    time.sleep(0.1)

            # get frame from http server
            for key in self.cameras_image.keys():

                camera_info = self.cameras_image[key].readCameraInfo()

                if camera_info is None or camera_info['im_data'] is None:
                    continue

                new_cam_id = camera_info['camera_id'] + '_' + str(camera_info['angle_id'])
                # new_cam_id = camera_info['camera_id']
                encodeRgbImage = self.detect_frame(camera_info['im_data'], new_cam_id, camera_info['im_path'])
                self.slot.emit(encodeRgbImage)
                time.sleep(0.1)

    def detect_frame(self, img, cam_id, raw_image_path=None):
        '''
        :param img:
        :param cam_id:
        :return:
        '''
        start = time.perf_counter()
        image_detect_res, masked, reportingAbnormalSet = detectAbnormalForUI(self.detection, img, cam_id,
                                                                             logger=self.logger,
                                                                             frame_raw_image_path=raw_image_path)
        end = time.perf_counter()
        line = 'detectAbnormalForUI: the runtime is: ' + str(end - start) + '\n'
        # print(line)
        self.logger.info(line)
        print("---------------", len(reportingAbnormalSet))
        for report in reportingAbnormalSet:
            abnormal = dict()
            cls = ''
            for r in report.keys():
                if r == "score":
                    abnormal['score'] = report['score']
                    continue
                else:
                    cls = r
                    report[r] = cv2.resize(report[r], (80, 130))
                    abnormal[r] = report[r].tostring()

                abnormals.append(abnormal)
            cv2.imwrite(getProjectContext()+"/Utils/temp.jpg", report[cls])
            self.run_send_abnormal_thread(getProjectContext()+"/Utils/temp.jpg", abnormal['type'], abnormal['score'])

        # rgbImage = cv2.resize(masked, (628, 417))
        rgbImage = cv2.resize(image_detect_res, (628, 417))
        #
        cv2.putText(rgbImage, cam_id, (300, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                    2)

        encodeRgbImage = rgbImage.tostring()

        rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_RGB2BGR)
        img_str = cv2.imencode('.jpg', rgbImage)[1].tostring()
        self.websocket_queue.put(str(base64.b64encode(img_str), encoding="utf-8"))

        return encodeRgbImage

    async def send_msg(self):
        '''
        :return:
        '''
        url = "ws://221.226.81.54:30009"
        while True:
            try:
                async with websockets.connect(url) as websocket:
                    while True:
                        if self.websocket_queue.qsize() == 0:
                            time.sleep(2)
                        msg = self.websocket_queue.get()
                        await websocket.send(msg)
                        print(f'client send message to server {url} successfully')
                        # time.sleep(10)
            except Exception as e:
                print(e)
                time.sleep(2)

    def run_send_detect_thread(self):
        asyncio.run(self.send_msg())

    def run_send_abnormal_thread(self, img_path, cls, score):
        '''
        :param img_path:
        :param cls:
        :param score:
        :return:
        '''
        im_data = self.image_to_base64(img_path)
        abnormal_meta = dict()
        abnormal_meta['cls'] = str(cls)
        abnormal_meta['score'] = str(score)
        abnormal_meta['data'] = im_data
        n = 0
        while True:

            if n > 3:
                self.logger("the send-abnormal is timeout")
                break
            try:
                res = requests.post("http://221.226.81.54:30010/", data=json.dumps(abnormal_meta))
                if res.text == "yes":
                    self.logger("abnormal send is success")
                    break
            except:
                n += 1

    def image_to_base64(self, path):

        with open(path, 'rb') as f:
            image = f.read()
            image_base64 = str(base64.b64encode(image), encoding='utf-8')
        return image_base64


if __name__ == "__main__":
    def image_to_base64(path):

        with open(path, 'rb') as f:
            image = f.read()
            image_base64 = str(base64.b64encode(image), encoding='utf-8')
        return image_base64


    def run_send_abnormal_thread(img_path, cls, score):
        '''
        :param img_path:
        :param cls:
        :param score:
        :return:
        '''
        im_data = image_to_base64(img_path)
        abnormal_meta = dict()
        abnormal_meta['cls'] = cls
        abnormal_meta['score'] = score
        abnormal_meta['data'] = im_data
        n = 0
        while True:
            if n > 3:
                break
            try:
                res = requests.post("http://221.226.81.54:30010/", data=json.dumps(abnormal_meta))
                if res.text == "yes":
                    print("abnormal send is success")
                    break
            except:
                n += 1


    run_send_abnormal_thread(getProjectContext()+"/Utils/temp.jpg", "UoDOFacilities", "0.8")
