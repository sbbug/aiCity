
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from UI.default import *
from Functions import getProjectContext

class CamLabel(QLabel):
    def __init__(self,parent,cam_id):

        super(CamLabel, self).__init__(parent)

        self.setText(str(cam_id))
        self.setFixedSize(210,114)
        self.setObjectName("cam_label")
        im = QPixmap(getProjectContext()+"UI/resources/camera_imgs/camera_2.jpg")
        # im = im.scaled(400, 200)
        self.setPixmap(im)

class ShowDetectTitle(QLabel):
    def __init__(self,parent):

        super(ShowDetectTitle, self).__init__(parent)
        self.setFixedSize(402,66)
        self.setPixmap(QPixmap(getProjectContext()+"UI/resources/images/show_detect_title.jpg"))

class ShowStreamBackground(QLabel):
    def __init__(self,parent):

        super(ShowStreamBackground, self).__init__(parent)
        self.setFixedSize(670,460)
        self.setPixmap(QPixmap(getProjectContext()+"UI/resources/images/show_stream_3.png"))


class ShowStream(QLabel):
    def __init__(self,parent):

        super(ShowStream, self).__init__(parent)
        self.setFixedSize(628,417)

class StartButton(QLabel):
    def __init__(self,parent):

        super(StartButton, self).__init__(parent)
        self.setFixedSize(50,50)
        self.setPixmap(QPixmap(getProjectContext()+"UI/resources/images/start.png"))

class StopButton(QLabel):
    def __init__(self, parent):
        super(StopButton, self).__init__(parent)
        self.setFixedSize(50, 50)
        self.setPixmap(QPixmap(getProjectContext()+"UI/resources/images/stop.png"))

class AbnormalLabel(QLabel):
    def __init__(self,parent,cam_id):

        super(AbnormalLabel, self).__init__(parent)

        self.setText(str(cam_id))
        self.setFixedSize(130,130)
        self.setObjectName("abnormal_label")
        #self.setPixmap(QPixmap("./resources/camera_imgs/abnormal.png"))

class AbnormalLabelTitle(QLabel):
    def __init__(self, parent):
        super(AbnormalLabelTitle, self).__init__(parent)

        self.setFixedSize(130, 30)
        self.setObjectName("abnormal_label_title")
        # self.setPixmap(QPixmap("./resources/camera_imgs/abnormal.png"))