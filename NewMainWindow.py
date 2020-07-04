# ref:https://doc.qt.io/qt-5/qvboxlayout.html

from UI.TitleBar import *
from UI.funcs import LoadStyleFromQss
from UI.cameraLabel import CamLabel, ShowDetectTitle, ShowStreamBackground, StartButton, StopButton, AbnormalLabel, \
    ShowStream, AbnormalLabelTitle
import Parameters
import Functions
import time
import numpy as np

from Camera.Camera import Camera
from Parameters import WINDOW_QSS
from Functions import getCameraUrl
from Tool.logger.make_logger import make_logger
import datetime
import os
import threading

from Utils.DetectThread import DetectThread
from Utils.Func import monitor_show
from Utils.GrapDetectCamerasThread import GrapDetectCamerasThread
from Utils.GrapLeftCamerasThread import GrapLeftCamerasThread
from Utils.ShowAbnormalThread import ShowAbnormalThread
from Parameters import HTTP_CAMERAS
from Camera.HttpCamera import HttpCamera
from Camera.FtpServer import FtpServer

#
CAM_NUM = 40


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.abnormals = dict()
        self.camera_labels = dict()
        self.abnormal_labels = []
        self.abnormal_label_titles = []
        self.cameras_rtsp = []
        self.cameras_image = dict()
        self.ftp_cameras = []

        log_output_dir = os.path.join(getProjectContext(), Parameters.OUTPUT_LOG, str(datetime.date.today()))
        if not os.path.exists(log_output_dir):
            os.mkdir(log_output_dir)

        self.logger = make_logger("project", log_output_dir, 'log')

        self.logger.info("start initCameras")
        self.initCameras(self.logger)
        self.logger.info("start InitializeWindow")
        self.InitializeWindow()

    def InitializeWindow(self):  # 初始化窗口
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)
        self.InitializeViews()  # 初始化窗口中的组件
        self.setStyleSheet(str(LoadStyleFromQss(Functions.getProjectContext() + WINDOW_QSS)))  # 组件属性参数载入

    def InitializeViews(self):

        self.center = QWidget(self)  # 定义显示区域
        self.setCentralWidget(self.center)  # 将center放在桌面上
        self.center_v_lay = QVBoxLayout(self)
        self.center.setLayout(self.center_v_lay)  # 在center窗口上定义水平布局

        # 初始化导航栏
        self.InitializeTopViews()
        # 初始化客户端区域
        self.client = QWidget(self)  # 定义窗口
        self.client_h_lay = QHBoxLayout(self)  # 定义水平布局
        self.client.setLayout(self.client_h_lay)
        self.center_v_lay.addWidget(self.client)  # 同时将client加入center
        self.center_v_lay.setStretch(1, 100)
        self.center_v_lay.setSpacing(0)
        self.center_v_lay.setContentsMargins(0, 0, 0, 0)  # 设置内边距

        self.InitializeLeftViews()
        self.InitializeCenterViews()
        self.InitializeRightViews()

        # start grap video image
        self.startLeftGrapCamerasThread()
        self.startDetectGrapCamerasThread()
        # self.startMonitorQueueSize()
        # left show
        self.startShowLeftCameraThread()
        self.startDetectCameraThread()
        self.startUpdateRightAbnormals()

    def initCameras(self, logger, timeout=10):

        ipConfig = Functions.loadIPConfig(Functions.getProjectContext() + Parameters.DETECT_CAMERAS_CONFIG)

        for c in ipConfig:
            url = getCameraUrl(c)
            camera = Camera(url, c['cam_id'], 1280, 720)
            logger.info("opening {} ".format(url))
            camera.open()
            logger.info("opened {} ".format(url))

            if camera.is_opened is False:
                logger.info("failed to open {} ".format(url))
            else:
                self.cameras_rtsp.append(camera)

        for camera_id in HTTP_CAMERAS:
            self.cameras_image[camera_id] = HttpCamera(camera_id)
        # ftp_server = FtpServer("121.43.182.244", 'ftpuser', 'Lawatlas2018')
        # self.ftp_cameras.append(ftp_server)

    # 初始化顶部标题栏
    def InitializeTopViews(self):
        self.titleBar = TitleBar(self)  # 定义导航条对象
        self.titleBar.setObjectName("top")
        self.center_v_lay.addWidget(self.titleBar)  # 按照水平布局，将标题栏加入center
        self.titleBar.SetIcon(QPixmap(WINDOW_ICON));  # 设置图标
        self.titleBar.SetTitle(WINDOW_TITLE);  # 设置导航栏的标签与标题

    # 初始化左侧检测窗口
    def InitializeLeftViews(self):

        self.left_show = QWidget()
        self.left_show.setObjectName("left_show")
        self.client_h_lay.addWidget(self.left_show)
        self.client_h_lay.setStretchFactor(self.left_show, 4)

        self.left_show_cameras = QWidget()
        self.left_show_cameras.setObjectName("left_show_cameras")
        self.left_show_cameras.setMinimumSize(180, 4600)

        self.left_show_title = QWidget()
        self.left_show_title.setObjectName("left_show_title")
        self.left_label_show_title = QLabel(self.left_show_cameras)
        self.left_label_show_title.setObjectName("left_label_show_title")

        im = QPixmap(getProjectContext() + "UI/resources/images/show_camera_title.jpg")
        # im = im.scaled(280, 200)

        self.left_label_show_title.setPixmap(im)

        for i in range(1, CAM_NUM + 1):
            label = CamLabel(self.left_show_cameras, str(i))
            label.move(20, 10 + (i - 1) * 120)
            key = "camera_" + str(i)
            self.camera_labels[key] = label

        self.scroll = QScrollArea()
        self.scroll.setObjectName("scroll")
        self.scroll.setWidget(self.left_show_cameras)
        self.scroll_bar = self.scroll.verticalScrollBar()  # 重要的一步，获取滚动范围的滚动条！！！
        self.scroll_bar.setObjectName("bar")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.left_label_show_title)
        self.vbox.addWidget(self.scroll)
        self.left_show.setLayout(self.vbox)

    def setLeftLabelCamera(self):

        while True:
            for camera in self.cameras_rtsp:
                cam_id = camera.cam_id
                image = camera.readShowQ()
                if image is not None:
                    h, w, ch = image.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    self.camera_labels[cam_id].setPixmap(QPixmap.fromImage(convertToQtFormat))

            time.sleep(1)

    def setDetectCenterCamera(self, image):
        try:
            image = np.frombuffer(image, dtype=np.uint8).reshape((417, 628, 3))

            h, w, ch = image.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)

            self.show_stream.setPixmap(QPixmap.fromImage(convertToQtFormat))
        except:
            pass

    def startShowLeftCameraThread(self):

        show_left_camera = threading.Thread(target=self.setLeftLabelCamera, args=())
        show_left_camera.start()

    def startLeftGrapCamerasThread(self):

        th = GrapLeftCamerasThread(self, cameras=self.cameras_rtsp, logger=self.logger)
        th.start()

    def startDetectGrapCamerasThread(self):

        th = GrapDetectCamerasThread(self, cameras=self.cameras_rtsp, logger=self.logger)
        th.start()

    def startDetectCameraThread(self):

        th = DetectThread(self, self.cameras_rtsp, self.cameras_image, self.logger)
        th.slot.connect(self.setDetectCenterCamera)
        th.start()

    def startMonitorQueueSize(self):

        monitor_th = threading.Thread(target=monitor_show, args=(self.cameras,))
        monitor_th.start()

    def updateRightAbnormals(self, abnormals):

        self.logger.info("updateRightAbnormals(self,abnormals):{}".format(len(abnormals)))
        # print("===============",abnormals)
        for index, abnormal in enumerate(abnormals):
            for key in abnormal.keys():
                if key == "score": continue
                image = np.frombuffer(abnormal[key], dtype=np.uint8).reshape((130, 80, 3))

                h, w, ch = image.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)

                # show_abnormal = AbnormalLabel(self.right_show_abnormals, str(i))
                self.abnormal_labels[index].setPixmap(QPixmap.fromImage(convertToQtFormat))
                self.abnormal_label_titles[index].setText(key+" "+str(abnormal['score']))
                # show_abnormal.setPixmap(QPixmap("./resources/camera_imgs/abnormal.png"))
                # show_abnormal.move(10, 10 + i * 135)

    def startUpdateRightAbnormals(self):

        th = ShowAbnormalThread(self)
        th.slot.connect(self.updateRightAbnormals)
        th.start()

    def createAbnormalLabels(self):
        for i in range(120):  # revised

            show_abnormal_title = AbnormalLabelTitle(self.right_show_abnormals)
            self.abnormal_label_titles.append(show_abnormal_title)
            show_abnormal_title.move(10, 10 + i * (30 + 130 + 10))

            show_abnormal = AbnormalLabel(self.right_show_abnormals, str(i))
            self.abnormal_labels.append(show_abnormal)
            show_abnormal.move(10, 40 + i * (130 + 10 + 30))

    # 初始化右侧异常上报窗口
    def InitializeRightViews(self):
        # 右侧异常显示栏
        self.right_show = QWidget()
        self.right_show.setObjectName("right_show")
        self.client_h_lay.addWidget(self.right_show)
        self.client_h_lay.setStretchFactor(self.right_show, 3)

        self.right_show_abnormals = QWidget()
        self.right_show_abnormals.setObjectName("right_show_abnormals")
        self.right_show_abnormals.setMinimumSize(160, 4600)

        self.right_show_title = QWidget()
        self.right_show_title.setObjectName("right_show_title")
        self.right_label_show_title = QLabel(self.right_show_abnormals)
        self.right_label_show_title.setObjectName("right_label_show_title")
        self.right_label_show_title.setPixmap(
            QPixmap(getProjectContext() + "UI/resources/images/show_abnormal_title.png"))

        self.createAbnormalLabels()

        self.scroll = QScrollArea()
        self.scroll.setObjectName("scroll")
        self.scroll.setWidget(self.right_show_abnormals)
        self.scroll_bar = self.scroll.verticalScrollBar()  # 重要的一步，获取滚动范围的滚动条！！！
        self.scroll_bar.setObjectName("bar")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.right_label_show_title)
        self.vbox.addWidget(self.scroll)
        self.right_show.setLayout(self.vbox)

    # 初始化中心检测窗口
    def InitializeCenterViews(self):

        self.main_center = QWidget()
        self.main_center.setObjectName("main_center")
        self.client_h_lay.addWidget(self.main_center)
        self.client_h_lay.setStretchFactor(self.main_center, 14)

        self.show_detect_title = ShowDetectTitle(self.main_center)
        self.show_detect_title.setObjectName("show_detect_title")
        self.show_detect_title.move(220, 80)

        self.show_stream_background = ShowStreamBackground(self.main_center)
        self.show_stream_background.setObjectName("show_stream_background")
        self.show_stream_background.move(90, 180)

        self.show_stream = ShowStream(self.show_stream_background)
        self.show_stream.setObjectName("show_stream")
        self.show_stream.setPixmap(QPixmap(getProjectContext() + "UI/resources/images/camera_33.jpg"))
        self.show_stream.move(25, 25)  # compare show_stream_background

        # self.button_start = StartButton(self.main_center)
        # self.button_start.setObjectName("button_start")
        # self.button_start.move(280, 700)
        # self.button_stop = StopButton(self.main_center)
        # self.button_stop.setObjectName("button_stop")
        # self.button_stop.move(480, 700)

        # self.startDetectCenterCameraThread()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
