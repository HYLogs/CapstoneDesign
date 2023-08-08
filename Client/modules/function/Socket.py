from socket import *
from threading import Thread

from PIL import Image
from PyQt5.QtGui import QPixmap, QImage
import pyautogui


class Server:
    def __init__(self):
        self.isSharing: bool = False
        self.broadcastIp: str

    def startBroadCast(self, broadcastIp):
        self.broadcastIp = broadcastIp
        t = Thread(self.threadedBroadCasting(broadcastIp))
        t.start()

    def threadedBroadCasting(self, broadcastIp):
        soc = socket(AF_INET, SOCK_DGRAM)
        soc.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        while True:
            print("Sending..")
            soc.sendto("ip".encode("utf-8"), (broadcastIp, 1999))
            if self.isSharing:
                # 캡쳐 로직
                bytes = capture()
                soc.sendto(bytes, (broadcastIp, 1999))


class Client:
    def __init__(self):
        self.isSharing: bool = False

    def recvScreen(self, screen):
        self.isSharing = True
        t = Thread(self.threadedRecvScreen(screen))
        t.start()

    def threadedRecvScreen(self, screen):
        self.soc = socket(AF_INET, SOCK_DGRAM)
        self.soc.bind(('', 1999))
        while True:
            # msg, addr = self.soc.recvfrom(1024)
            # ip 설정 이벤트 처리

            if self.isSharing:
                print('--- before ---')
                data = self.soc.recv(4)
                # 최초 4바이트는 전송할 데이터의 크기이다. 그 크기는 little big 엔디언으로 byte에서 int형식으로 변환한다.
                # C#의 BitConverter는 big엔디언으로 처리된다.
                length = int.from_bytes(data, "little")
                # 다시 데이터를 수신한다.
                if length > 1024:
                    data = self.soc.recv(1024)
                    while (length - len(data)) > 0:
                        data += self.soc.recv(length - len(data))
                else:
                    data = self.soc.recv(length)

                pixmap = decodeCapture(data)
                screen.setPixmap(pixmap)
                print('--- after ---')

    def closeEvent(self):
        self.isSharing = False

def capture():
    screenshot = pyautogui.screenshot()
    screenshot_bytes = screenshot.tobytes()
    return screenshot_bytes

def decodeCapture(image):
    screenshot_pil = Image.frombytes("RGB", pyautogui.size, image)
    screenshot_qimage = QImage(screenshot_pil.tobytes(), screenshot_pil.size[0], screenshot_pil.size[1], QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(screenshot_qimage)
    return pixmap