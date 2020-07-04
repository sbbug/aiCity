import time
import logging
import threading
import cv2
from multiprocessing import Queue


def open_cam_rtsp(uri, width, height, latency):
    """Open an RTSP URI (IP CAM)."""
    # gst_str = ('rtspsrc location={} latency={} ! '
    #            'rtph264depay ! h264parse ! omxh264dec ! '
    #            'nvvidconv ! '
    #            'video/x-raw, width=(int){}, height=(int){}, '
    #            'format=(string)BGRx ! videoconvert ! '
    #            'appsink').format(uri, latency, width, height)

    return cv2.VideoCapture(uri)


def grab_img(cam):
    """This 'grab_img' function is designed to be run in the sub-thread.
    Once started, this thread continues to grab a new image and put it
    into the global 'img_handle', until 'thread_running' is set to False.
    """
    while cam.thread_running:

        if cam.cap.isOpened():

            ret, cam.img_handle = cam.cap.read()

            if ret is False:
                break

            if cam.img_handle is None:
                break
            else:
                cam.img_handle = cv2.cvtColor(cam.img_handle, cv2.COLOR_BGR2RGB)
                cam.img_detect = cam.img_handle.copy()
        # time.sleep(0.01)

    cam.thread_running = False


class Camera():
    """Camera class which supports reading images from theses video sources:
     RTSP (IP CAM)

    """

    def __init__(self, url, cam_id, img_w, img_h):
        self.rtsp_uri = url
        self.image_width = img_w
        self.image_height = img_h
        self.rtsp_latency = 200
        self.is_opened = False
        self.thread_running = False
        self.img_handle = None
        self.img_detect = None
        self.img_width = 0
        self.img_height = 0
        self.cap = None
        self.thread = None
        self.detect_queue = Queue(1000)
        self.show_queue = Queue(1000)
        self.cam_id = cam_id

    def open(self):
        """Open camera based on command line arguments."""

        self.cap = open_cam_rtsp(
            self.rtsp_uri,
            self.image_width,
            self.image_height,
            self.rtsp_latency)

        if self.cap.isOpened():
            # Try to grab the 1st image and determine width and height
            _, img = self.cap.read()
            if img is not None:
                self.is_opened = True

    def start(self):
        assert not self.thread_running
        self.thread_running = True
        self.thread = threading.Thread(target=grab_img, args=(self,))
        self.thread.start()

    def stop(self):
        self.thread_running = False
        self.thread.join()

    def read(self):

        return self.img_handle

    def readDetectQ(self):
        img = None
        if self.detect_queue.qsize()>0:
            # 日志打印
            # print(self.cam_id, "DetectQ大小", self.detect_queue.qsize())
            img = self.detect_queue.get()
        return img

    def putDetectQ(self):
        if self.img_detect is not None:
            self.img_detect = cv2.resize(self.img_detect, (self.image_width, self.image_height))
            self.detect_queue.put(self.img_detect)

    def getDetectQSize(self):
        return self.detect_queue.qsize()

    def readShowQ(self):
        img = None
        if self.show_queue.qsize()>0:
            # 日志打印
            # print(self.cam_id, "ShowQ大小", self.show_queue.qsize())
            img = self.show_queue.get()
        return img

    def putShowQ(self):
        if self.img_handle is not None:
            im = cv2.resize(self.img_handle, (204, 116))
            im = cv2.putText(im, self.cam_id.split("_")[1], (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            self.show_queue.put(im)

    def getShowQSize(self):
        return self.show_queue.qsize()

    def release(self):
        assert not self.thread_running
        if self.cap != 'OK':
            self.cap.release()
