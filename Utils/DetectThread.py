from PyQt5.QtCore import *
import time
from Interface2 import detectAbnormalForUI
# from DeepDetect.FPN.FpnDetection import FpnDetection
from DeepDetect.CascadeDetection import CascadeDetection
import cv2
import Parameters
# from newMainWindow import abnormals
from Utils.par import abnormals
from Camera.FtpServer import FtpServer
from Parameters import HTTP_CAMERAS
from Camera.HttpCamera import HttpCamera


class DetectThread(QThread):
    # revised in 2019.11.21 by mjs: add time.clock()

    slot = pyqtSignal(bytes)

    def __init__(self, parent, cameras_rtsp,cameras_image,logger):
        QThread.__init__(self, parent=parent)

        # self.detection = FpnDetection()
        self.detection = CascadeDetection()
        self.cameras_rtsp = cameras_rtsp
        self.cameras_image = cameras_image
        self.logger = logger
        # ftp server info
        self.ftp_server = FtpServer("121.43.182.244", 'ftpuser', 'Lawatlas2018')
        self.ftp_cameras = ["camera_51"]
        # http server info
        # self.http_cameras = dict()

        # for camera_id in HTTP_CAMERAS:
        #     self.http_cameras[camera_id] = HttpCamera(camera_id)

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

            # get frame from ftp server
            # img = self.ftp_server.read()
            #
            # if img is not None:
            #     encodeRgbImage = self.detect_frame(img, self.ftp_cameras[0])
            #     self.slot.emit(encodeRgbImage)
            #     time.sleep(0.1)

            # get frame from http server
            for key in self.cameras_image.keys():

                camera_info = self.cameras_image[key].readCameraInfo()

                if camera_info is None or camera_info['im_data'] is None:
                    continue

                new_cam_id = camera_info['camera_id'] + '_' + str(camera_info['angle_id'])
                # new_cam_id = camera_info['camera_id']
                encodeRgbImage = self.detect_frame(camera_info['im_data'], new_cam_id,camera_info['im_path'])
                self.slot.emit(encodeRgbImage)
                time.sleep(0.1)

    def detect_frame(self, img, cam_id,raw_image_path = None):
        '''
        :param img:
        :param cam_id:
        :return:
        '''
        start = time.perf_counter()
        image_detect_res, masked, reportingAbnormalSet = detectAbnormalForUI(self.detection, img, cam_id,logger=self.logger,frame_raw_image_path=raw_image_path)
        end = time.perf_counter()
        line = 'detectAbnormalForUI: the runtime is: ' + str(end - start) + '\n'
        # print(line)
        self.logger.info(line)

        for report in reportingAbnormalSet:
            abnormal = dict()
            for r in report.keys():
                if r == "score":
                    abnormal['score'] = report['score']
                    continue
                else:
                    report[r] = cv2.resize(report[r], (80, 130))
                    abnormal[r] = report[r].tostring()

                abnormals.append(abnormal)

        # rgbImage = cv2.resize(masked, (628, 417))
        rgbImage = cv2.resize(image_detect_res, (628, 417))
        #
        cv2.putText(rgbImage, cam_id, (300, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                    2)

        encodeRgbImage = rgbImage.tostring()

        return encodeRgbImage
