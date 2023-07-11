from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
import numpy as np
import pyautogui

import win32gui
import win32con
import win32api
import win32ui
from PIL import Image

import cv2
import time

ESC_KEY = 27
FRAME_RATE = 60
SLEEP_TIME = 1 / FRAME_RATE


class Remote:
    def __init__(self, QuitButton):
        self.stopsig = 0
        self.QuitButton = QuitButton
        self.QuitButton.clicked.connect(self.closeEvent)

    def startRemote(self, qlabel):
        while True:
            start = time.time()

            frame = np.asarray(pyautogui.screenshot())

            h, w, c = frame.shape
            qImg = QtGui.QImage(frame.data, w, h, w * c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            ## 출력영상을 resize해주기
            width, height = pyautogui.size()
            p = pixmap.scaled(QSize(width-300, height-300), QtCore.Qt.KeepAspectRatioByExpanding)
            qlabel.setPixmap(p)

            delta = time.time() - start

            if delta < SLEEP_TIME:
                time.sleep(SLEEP_TIME - delta)
            cv2.waitKey(1)
            if self.stopsig == 1:
                break

    def closeEvent(self):
        self.stopsig = 1
