from modules.domain.Student import Student
from modules.domain.Teacher import Teacher

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
import numpy as np
import pyautogui

import cv2
import time
import socket


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
            remoteScreen.setPixmap(p)

            delta = time.time() - start

            if delta < self.SLEEP_TIME:
                time.sleep(self.SLEEP_TIME - delta)
            cv2.waitKey(1)

    def closeEvent(self):
        self.stopsig = 1

# Main
class StudentService:
    student: Student
    remoteObject: Remote

    def __init__(self):
        ip, name = self.findStudentInfo()
        self.student = Student(ip, name)
        self.remoteObject = Remote()

    def excuteInputEvent(self):
        return 0

    def sendScr(self):
        return 0

    def sendRemote(self, remoteScreen):
        # 원격 제어 요청 처리

        # 원격 제어 실행
        self.remoteObject.startRemote(remoteScreen)

        return 0

    def closeRemote(self):
        self.remoteObject.closeEvent()

    def findStudentInfo(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        name = socket.gethostname()
        return ip, name

    def findTeacher(self):
        # 브로드캐스팅 수신
        teacher = Teacher()
        self.student.set_teacher(teacher)
