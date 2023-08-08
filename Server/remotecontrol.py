import socket
import pyautogui
import zlib
import time
import numpy as np
import threading
import cv2
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QSize

class screenShareServer:
    def __init__(self) -> None:
        pass

    def connectServer(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', port))
        server_socket.listen()

        try:
            while True:
                clinet_socket, addr = server_socket.accept()
                th_send = threading.Thread(target=self.sendData, args=(clinet_socket, addr))
                th_send.start()
                
        except:
            server_socket.close()

    def sendData(self, client_socket, ip):
        print('connected : ', ip)
        time.sleep(0.5)
        try:
            while True:
                image = pyautogui.screenshot()
                data = image.tobytes()
                data = zlib.compress(data)
                length = len(data)
                client_socket.sendall(length.to_bytes(4, byteorder="little"))
                client_socket.sendall(data)
                time.sleep(0.01)

        except:
            print("except: ", ip)

        finally:
            client_socket.close()

class screenShareClinet:
    ESC_KEY = 27
    FRAME_RATE = 60
    SLEEP_TIME = 1 / FRAME_RATE

    def __init__(self):
        self.stopsig = 0

    def connectServer(self, host_ip, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host_ip, port))

        th_receive = threading.Thread(target=self.receiveData, args=(client_socket, host_ip))
        th_receive.start()
    
    def receiveData(self, remoteScreen):
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


        

class remoteControl:
    def __init__(self) -> None:
        pass

