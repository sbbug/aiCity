# render right abnormal

from PyQt5.QtCore import *
import time
from Utils.par import abnormals

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