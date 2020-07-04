
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from UI.default import *
from UI.funcs import LoadStyleFromQss
class LeftScroll(QWidget):
    def __init__(self,parent):
        super(LeftScroll, self).__init__()
        self.win = parent
        self.InitializeWindow()
        print("----------")
    def InitializeWindow(self):
        self.isPressed = False
        self.setMinimumSize(300, 600);
        self.InitializeViews()
        self.setStyleSheet(str(LoadStyleFromQss("./resources/css/test.qss")))

    def InitializeViews(self):
        self.number = 0
        self.topFiller = QWidget()

        self.topFiller.setMinimumSize(250, 900)  #######设置滚动条的尺寸
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
        self.resize(300, 500)

    def ShowMininizedWindow(self):
        self.win.showMinimized()

    def ShowMaximizedWindow(self):
        self.win.showMaximized()

    def ShowRestoreWindow(self):
        if self.win.isMaximized():
            self.win.showNormal()
        else:
            self.win.showMaximized()

    def CloseWindow(self):
        self.win.close()

    def SetTitle(self, str):
        self.titleLabel.setText(str)

    def SetIcon(self, pix):
        self.iconLabel.setPixmap(pix.scaled(self.iconLabel.size() - QSize(TITLE_ICON_MAG, TITLE_ICON_MAG)))

    def mouseDoubleClickEvent(self, event):
        self.ShowRestoreWindow()
        return QWidget().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        self.isPressed = True
        self.startPos = event.globalPos()
        return QWidget().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.isPressed = False
        return QWidget().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.isPressed:
            if self.win.isMaximized:
                self.win.showNormal()

            movePos = event.globalPos() - self.startPos
            self.startPos = event.globalPos()
            self.win.move(self.win.pos() + movePos)

        return QWidget().mouseMoveEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LeftScroll(None)
    win.show()
    sys.exit(app.exec_())

