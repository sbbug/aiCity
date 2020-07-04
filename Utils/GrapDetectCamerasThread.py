from PyQt5.QtCore import *
import time


class GrapDetectCamerasThread(QThread):

    def __init__(self, parent, cameras, logger):
        QThread.__init__(self, parent=parent)
        self.cameras = cameras
        self.logger = logger

    def run(self):

        while True:
            for camera in self.cameras:
                camera.putDetectQ()
            time.sleep(60)  # sample frequence  1 / one min
