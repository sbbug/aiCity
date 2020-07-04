import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from UI.default import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.InitializeWindow()

    def InitializeWindow(self):
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(300, 600);
        self.InitializeViews()
        self.setStyleSheet(str(self.LoadStyleFromQss("../resources/css/test.qss")))

    def InitializeViews(self):
        self.number = 0
        w = QWidget()
        w.setObjectName("main")
        self.setCentralWidget(w)

        self.topFiller = QWidget()

        self.topFiller.setMinimumSize(600, 900)  #######设置滚动条的尺寸
        for filename in range(20):
            self.MapButton = QPushButton(self.topFiller)
            self.MapButton.setText(str(filename))
            self.MapButton.move(10, filename * 40)
        ##创建一个滚动条
        self.scroll = QScrollArea()
        self.scroll.setObjectName("scroll")
        self.scroll.setWidget(self.topFiller)
        self.scroll_bar = self.scroll.verticalScrollBar() # 重要的一步，获取滚动范围的滚动条！！！
        self.scroll_bar.setObjectName("bar")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.scroll)
        w.setLayout(self.vbox)


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