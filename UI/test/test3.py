import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from UI.default import *
from UI.cameraLabel import CamLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.InitializeWindow()

    def InitializeWindow(self):
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(300, 600)
        self.InitializeViews()
        self.setStyleSheet(str(self.LoadStyleFromQss("../resources/css/test.qss")))

    def InitializeViews(self):
        self.number = 0
        self.main = QWidget()
        self.main.setObjectName("main")
        self.setCentralWidget(self.main)

        self.left = QWidget()
        self.center = QWidget()

        self.left_camera = QWidget()
        self.left_camera.setMinimumSize(300, 8000)

        self.lay = QHBoxLayout()
        self.lay.addWidget(self.left)
        self.lay.addWidget(self.center)
        self.main.setLayout(self.lay)
        self.lay.setStretchFactor(self.left, 6)
        self.lay.setStretchFactor(self.center, 6)

        self.center_lay = QHBoxLayout()
        label = QLabel()
        label.setPixmap(QPixmap("../resources/camera_imgs/camera_2.jpg"))
        self.center_lay.addWidget(label)
        self.center.setLayout(self.center_lay)

        for i in range(40):
            #label = QLabel(self.left_camera)
            label = CamLabel(self.left_camera,str(i))
            label.move(10, 10 + i * 210)

        ##创建一个滚动条
        self.scroll = QScrollArea()
        self.scroll.setObjectName("scroll")
        self.scroll.setWidget(self.left_camera)
        self.scroll_bar = self.scroll.verticalScrollBar() # 重要的一步，获取滚动范围的滚动条！！！
        self.scroll_bar.setObjectName("bar")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.scroll)
        self.left.setLayout(self.vbox)

    def LoadStyleFromQss(self, f):
        file = open(f)
        lines = file.readlines()
        file.close()
        res = ''
        for line in lines:
            res += line

        return res

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())