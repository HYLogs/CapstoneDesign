import cv2
from PIL import Image
from PyQt5.QtGui import QPixmap, QImage
import pyautogui
import io


# Remote Class
class Remote:
    ESC_KEY = 27
    FRAME_RATE = 60
    SLEEP_TIME = 1 / FRAME_RATE

    def __init__(self):
        self.stopsig = 0

    def startRemote(self, remoteScreen):
        remoteScreen.setScaledContents(True)
        while self.stopsig == 0:
            # pixmap = self.capture()
            # remoteScreen.setPixmap(pixmap)

            remoteScreen.setText("원격 제어 중")
            cv2.waitKey(1)

    def closeEvent(self):
        self.stopsig = 1