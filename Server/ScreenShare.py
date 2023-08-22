from threading import Thread
from socket import *
import pyautogui
import math
import pickle
import cv2
import numpy as np

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class ScreenShareServer:
    def __init__(self, clients: dict, port):
        self.isSharing: bool = False

        self.max_length = 65000

        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        self.clients = clients
        self.port = port

    def start(self):
        self.isSharing = True
        t = Thread(target=self.threadedSendScreen)
        t.daemon = True
        t.start()

    def threadedSendScreen(self):
        while True:
            clientsCopy = self.clients
            ips = clientsCopy.values()

            frame = cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
            retval, frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            frame = frame.tobytes()  # 이미지 바이트 배열로 변환

            buffer_size = len(frame)
            num_of_packs = math.ceil(buffer_size / self.max_length)
            frame_info = {"packs": num_of_packs, "isEnd": self.isSharing}

            for ip in ips:
                self.sock.sendto(pickle.dumps(frame_info), (ip, self.port))

            if not self.isSharing:
                break

            left = 0
            right = self.max_length

            for i in range(num_of_packs):
                data = frame[left:right]
                left = right
                right += self.max_length

                for ip in ips:
                    self.sock.sendto(data, (ip, self.port))

    def stop(self):
        self.isSharing = False


class ScreenShareClient:
    def __init__(self, port):
        self.isSharing: bool = False
        self.isSetImage: bool = True
        self.host = "0.0.0.0"
        self.port = port
        self.max_length = 65540

        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def start(self, screen):
        self.isSharing = True
        t = Thread(target=self.threadedRecvScreen, args=(screen,))
        t.daemon = True
        t.start()

    def threadedRecvScreen(self, screen):

        frame_info = None
        buffer = b""

        while True:
            if not self.isSharing:
                screen.clear()  # QLabel에 빈 QPixmap을 설정하여 화면을 지웁니다.
                break

            data, address = self.sock.recvfrom(self.max_length)

            if len(data) < 100:
                frame_info = pickle.loads(data)

                if frame_info:
                    # 서버에서 전송을 종려했을 경우
                    if not frame_info["isEnd"]:
                        screen.clear()
                        continue

                    nums_of_packs = frame_info["packs"]

                    for i in range(nums_of_packs):
                        data, address = self.sock.recvfrom(self.max_length)
                        buffer += data

                    data = np.frombuffer(buffer, dtype='uint8')
                    buffer = b""  # 버퍼 초기화
                    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)

                    if frame is not None and type(frame) == np.ndarray:
                        cv2.waitKey(1)

                pixmap = self.decodeCapture(frame)

                if self.isSetImage:
                    screen.setPixmap(pixmap)
                else:
                    pass

    def decodeCapture(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3, QImage.Format_RGB888)
        pixmap = QPixmap(image).scaled(image.width(), image.height(), Qt.IgnoreAspectRatio)

        return pixmap

    def stopRecv(self):
        self.isSharing = False

    def pauseRecv(self):
        self.isSetImage = False

    def resumeRecv(self):
        self.isSetImage = True

##  Use Example
# import time
# def sleepTime(second, server):
#     time.sleep(second)
#     server.stop()

# clients = {"test1" : "172.30.1.99"}
# server = ScreenShareServer(clients, 2000)

# t = Thread(target=sleepTime, args=(10, server, ))
# t.daemon = True
# t.start()

# server.start()