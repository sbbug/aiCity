#ref:https://doc.qt.io/qt-5/qvboxlayout.html
import sys
from UI.TitleBar import *
from UI.funcs import LoadStyleFromQss
from UI.leftScroll import LeftScroll
from UI.cameraLabel import CamLabel,ShowDetectTitle,ShowStreamBackground,StartButton,StopButton,AbnormalLabel,ShowStream,AbnormalLabelTitle
import cv2
import Parameters
import Functions
import time
import numpy as np
from Interface2 import detectAbnormalForUI
from DeepDetect.FPN.FpnDetection import FpnDetection
from multiprocessing import Queue
from Parameters import WINDOW_QSS
#
CAM_NUM = 40

frame_dict = dict()

abnormals = list()

#target_camera = [5,6,8,26,27,28,29,30,11,24] # targetting cameras needed to detected
target_camera = [24,30] # targetting cameras needed to detected

class ShowAbnormalThread(QThread):

    slot = pyqtSignal(list)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)


    def run(self):
        while True:
            try:
                print("ShowAbnormalThread-------len(abnormals)",len(abnormals))
                emit_abnormals = []

                for i in range(len(abnormals)):

                    emit_abnormals.append(abnormals[i])

                self.slot.emit(emit_abnormals)
                time.sleep(5)
            except:
                pass


class DetectThread(QThread):
    # revised in 2019.11.21 by mjs: add time.clock()

    slot = pyqtSignal(bytes)

    def __init__(self, parent=None):

        from DB.SQL_save import createLogDir
        from Tool.logger.make_logger import make_logger


        QThread.__init__(self, parent=parent)
        self.detection = FpnDetection()
        self.logger = make_logger('project', createLogDir(), 'run_log')


    def run(self):


        i = 0
        while True:
            print(frame_dict.__contains__(target_camera[i]))
            if frame_dict.__contains__(target_camera[i]):

              encodeRgbImage = frame_dict[target_camera[i]]

              #delete it

              del frame_dict[target_camera[i]]

              image = np.frombuffer(encodeRgbImage, dtype=np.uint8).reshape((720,1280,3))

              start = time.perf_counter()
              image_detect_res,masked,reportingAbnormalSet = detectAbnormalForUI(self.detection,image,"camera_"+str(target_camera[i]), self.logger)
              end = time.perf_counter()
              line = 'detectAbnormalForUI: the runtime is: ' + str(end - start) + '\n'
              self.logger.info(line)

              for report in reportingAbnormalSet:
                  abnormal = dict()
                  for r in report.keys():
                      report[r] = cv2.resize(report[r],(80,130))
                      abnormal[r] = report[r].tostring()
                      abnormals.append(abnormal)

              #rgbImage = cv2.resize(image_detect_res, (628, 417))

              rgbImage = cv2.resize(masked, (628, 417))

              cv2.putText(rgbImage, str(target_camera[i]), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)


              encodeRgbImage = rgbImage.tostring()

              self.slot.emit(encodeRgbImage)
              time.sleep(2)

            i+=1
            i=i%len(target_camera)



class Thread(QThread):

    cameras = ["url"] # url placeholder

    slot_1 = pyqtSignal(bytes,int)
    slot_2 = pyqtSignal(bytes, int)
    slot_3 = pyqtSignal(bytes, int)
    slot_4 = pyqtSignal(bytes, int)
    slot_5 = pyqtSignal(bytes, int)
    slot_6 = pyqtSignal(bytes, int)
    slot_7 = pyqtSignal(bytes, int)
    slot_8 = pyqtSignal(bytes, int)
    slot_9 = pyqtSignal(bytes, int)
    slot_10 = pyqtSignal(bytes, int)
    slot_11 = pyqtSignal(bytes, int)
    slot_12 = pyqtSignal(bytes, int)
    slot_13 = pyqtSignal(bytes, int)
    slot_14 = pyqtSignal(bytes, int)
    slot_15 = pyqtSignal(bytes, int)
    slot_16 = pyqtSignal(bytes, int)
    slot_17 = pyqtSignal(bytes, int)
    slot_18 = pyqtSignal(bytes, int)
    slot_19 = pyqtSignal(bytes, int)
    slot_20 = pyqtSignal(bytes, int)
    slot_21 = pyqtSignal(bytes, int)
    slot_22= pyqtSignal(bytes, int)
    slot_23 = pyqtSignal(bytes, int)
    slot_24 = pyqtSignal(bytes, int)
    slot_25 = pyqtSignal(bytes, int)
    slot_26= pyqtSignal(bytes, int)
    slot_27= pyqtSignal(bytes, int)
    slot_28= pyqtSignal(bytes, int)
    slot_29= pyqtSignal(bytes, int)
    slot_30= pyqtSignal(bytes, int)
    slot_31= pyqtSignal(bytes, int)
    slot_32= pyqtSignal(bytes, int)
    slot_33= pyqtSignal(bytes, int)
    slot_34= pyqtSignal(bytes, int)
    slot_35= pyqtSignal(bytes, int)
    slot_36= pyqtSignal(bytes, int)
    slot_37= pyqtSignal(bytes, int)
    slot_38= pyqtSignal(bytes, int)
    slot_39= pyqtSignal(bytes, int)

    slot_40 = pyqtSignal(bytes, int)


    def __init__(self, parent=None,var=None):
        QThread.__init__(self, parent=parent)
        Thread.initCameras()
        self.var = var

    @classmethod
    def initCameras(self):
        ipConfig = Functions.loadIPConfig(Functions.getProjectContext() + Parameters.CAMERAS_CONFIG)
        for con in ipConfig:
            Thread.cameras.append(Functions.getCameraUrl(con))


    def run(self):


        cap = cv2.VideoCapture(Thread.cameras[self.var])
        while True:
            ret, frame = cap.read()

            if ret:
                try:
                    # https://stackoverflow.com/a/55468544/6622587
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    rgbImage = cv2.resize(rgbImage,(1280,720))

                    encodeRgbImage = rgbImage.tostring()

                    if self.var in target_camera:

                        frame_dict[self.var] = encodeRgbImage

                    rgbImage = cv2.resize(rgbImage,(206,114))

                    cv2.putText(rgbImage, str(self.var), (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (255, 255, 255), 2)

                    encodeRgbImage = rgbImage.tostring()

                    me = eval("self.slot_"+str(self.var))
                    me.emit(encodeRgbImage,self.var)
                    time.sleep(0.1)
                except:
                    pass




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.abnormals = dict()
        self.camera_labels = []
        self.abnormal_labels = []
        self.abnormal_label_titles = []
        self.InitializeWindow()

    def InitializeWindow(self): #初始化窗口
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT);
        self.InitializeViews() #初始化窗口中的组件
        self.setStyleSheet(str(LoadStyleFromQss(Functions.getProjectContext() + WINDOW_QSS)))#组件属性参数载入

    def InitializeViews(self):

        self.center = QWidget(self) # 定义显示区域
        self.setCentralWidget(self.center)#将center放在桌面上
        self.center_v_lay = QVBoxLayout(self)
        self.center.setLayout(self.center_v_lay)#在center窗口上定义水平布局

        #初始化导航栏
        self.InitializeTopViews()
        #初始化客户端区域
        self.client = QWidget(self)  # 定义窗口
        self.client_h_lay = QHBoxLayout(self)  # 定义水平布局
        self.client.setLayout(self.client_h_lay)
        self.center_v_lay.addWidget(self.client)#同时将client加入center
        self.center_v_lay.setStretch(1, 100)
        self.center_v_lay.setSpacing(0)
        self.center_v_lay.setContentsMargins(0, 0, 0, 0)#设置内边距

        self.InitializeLeftViews()
        self.InitializeCenterViews()
        self.InitializeRightViews()

        self.startShowLeftCameraThread()
        self.startDetectCameraThread()
        self.startUpdateRightAbnormals()

    #初始化顶部标题栏
    def InitializeTopViews(self):
        self.titleBar = TitleBar(self)  # 定义导航条对象
        self.titleBar.setObjectName("top")
        self.center_v_lay.addWidget(self.titleBar)  # 按照水平布局，将标题栏加入center
        self.titleBar.SetIcon(QPixmap(WINDOW_ICON));  # 设置图标
        self.titleBar.SetTitle(WINDOW_TITLE);  # 设置导航栏的标签与标题

    #初始化左侧检测窗口
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
        self.left_label_show_title.setPixmap(QPixmap(getProjectContext()+"UI/resources/images/show_camera_title.jpg"))

        for i in range(1,CAM_NUM+1):
            label = CamLabel(self.left_show_cameras, str(i))
            label.move(10, 10 + (i-1) * 124)
            self.camera_labels.append(label)

        self.scroll = QScrollArea()
        self.scroll.setObjectName("scroll")
        self.scroll.setWidget(self.left_show_cameras)
        self.scroll_bar = self.scroll.verticalScrollBar()  # 重要的一步，获取滚动范围的滚动条！！！
        self.scroll_bar.setObjectName("bar")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.left_label_show_title)
        self.vbox.addWidget(self.scroll)
        self.left_show.setLayout(self.vbox)


    def setLeftLabelCamera(self, image,which):

        try:
            image = np.frombuffer(image,dtype=np.uint8).reshape((114,206,3))

            h, w, ch = image.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)

            self.camera_labels[which].setPixmap(QPixmap.fromImage(convertToQtFormat))
        except:
            pass

    def setDetectCenterCamera(self,image):
        try:
            image = np.frombuffer(image, dtype=np.uint8).reshape((417,628,3))

            h, w, ch = image.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)

            self.show_stream.setPixmap(QPixmap.fromImage(convertToQtFormat))
        except:
            pass

    def startShowLeftCameraThread(self):

        for i in range(1,CAM_NUM+1):
            th = Thread(self,i)
            temp = eval("th.slot_"+str(i))
            temp.connect(self.setLeftLabelCamera)
            th.start()

    def startDetectCameraThread(self):

        th = DetectThread(self)
        th.slot.connect(self.setDetectCenterCamera)
        th.start()

    def updateRightAbnormals(self,abnormals):

        print("updateRightAbnormals(self,abnormals)",len(abnormals))

        for index,abnormal in enumerate(abnormals):
            for key in abnormal.keys():
                image = np.frombuffer(abnormal[key], dtype=np.uint8).reshape((130, 80, 3))

                h, w, ch = image.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)

                #show_abnormal = AbnormalLabel(self.right_show_abnormals, str(i))
                self.abnormal_labels[index].setPixmap(QPixmap.fromImage(convertToQtFormat))
                self.abnormal_label_titles[index].setText(key)
                #show_abnormal.setPixmap(QPixmap("./resources/camera_imgs/abnormal.png"))
                #show_abnormal.move(10, 10 + i * 135)

    def startUpdateRightAbnormals(self):

        th = ShowAbnormalThread(self)
        th.slot.connect(self.updateRightAbnormals)
        th.start()

    def createAbnormalLabels(self):
        for i in range(120):  # revised

            show_abnormal_title = AbnormalLabelTitle(self.right_show_abnormals)
            self.abnormal_label_titles.append(show_abnormal_title)
            show_abnormal_title.move(10, 10 + i * (30+130+10))

            show_abnormal = AbnormalLabel(self.right_show_abnormals, str(i))
            self.abnormal_labels.append(show_abnormal)
            show_abnormal.move(10, 40 + i * (130+10+30))


    #初始化右侧异常上报窗口
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
        self.right_label_show_title.setPixmap(QPixmap(getProjectContext()+"UI/resources/images/show_abnormal_title.png"))

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

    #初始化中心检测窗口
    def InitializeCenterViews(self):

        self.main_center = QWidget()
        self.main_center.setObjectName("main_center")
        self.client_h_lay.addWidget(self.main_center)
        self.client_h_lay.setStretchFactor(self.main_center, 14)

        self.show_detect_title = ShowDetectTitle(self.main_center)
        self.show_detect_title.setObjectName("show_detect_title")
        self.show_detect_title.move(160, 10)

        self.show_stream_background = ShowStreamBackground(self.main_center)
        self.show_stream_background.setObjectName("show_stream_background")
        self.show_stream_background.move(20, 100)

        self.show_stream = ShowStream(self.show_stream_background)
        self.show_stream.setObjectName("show_stream")
        self.show_stream.setPixmap(QPixmap(getProjectContext()+"UI/resources/images/camera_33.jpg"))
        self.show_stream.move(25, 25)

        self.button_start = StartButton(self.main_center)
        self.button_start.setObjectName("button_start")
        self.button_start.move(220, 580)
        self.button_stop = StopButton(self.main_center)
        self.button_stop.setObjectName("button_stop")
        self.button_stop.move(420, 580)

        #self.startDetectCenterCameraThread()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


