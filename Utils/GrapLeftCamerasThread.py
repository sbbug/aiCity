
from PyQt5.QtCore import *
import time

class GrapLeftCamerasThread(QThread):

    def __init__(self, parent, cameras,logger):
        QThread.__init__(self, parent=parent)
        self.cameras = cameras
        self.logger = logger

    def run(self):

        for camera in self.cameras:
            self.logger.info("start thread {}".format(camera.cam_id))
            camera.start()

        while True:
            for camera in self.cameras:
                #print(camera.cam_id,"camera.putShowQ()")
                camera.putShowQ()

            time.sleep(1)