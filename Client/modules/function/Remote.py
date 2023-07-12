from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QSize

import numpy as np
import pyautogui

import cv2
import time

# Remote Class
class Remote:
    ESC_KEY = 27
    FRAME_RATE = 60
    SLEEP_TIME = 1 / FRAME_RATE

    def __init__(self):
        self.stopsig = 0

    def startRemote(self, remoteScreen):
        while self.stopsig == 0:
            start = time.time()

            frame = np.asarray(pyautogui.screenshot())

            h, w, c = frame.shape
            qImg = QtGui.QImage(frame.data, w, h, w * c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            ## 출력영상을 resize해주기
            width, height = pyautogui.size()
            p = pixmap.scaled(QSize(width-300, height-300), QtCore.Qt.KeepAspectRatioByExpanding)
            # remoteScreen.setPixmap(p)
            remoteScreen.setText("원격 제어 중")

            delta = time.time() - start

            if delta < self.SLEEP_TIME:
                time.sleep(self.SLEEP_TIME - delta)
            cv2.waitKey(1)

    def closeEvent(self):
        self.stopsig = 1