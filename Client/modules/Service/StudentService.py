from modules.domain.Student import Student
from modules.domain.Teacher import Teacher
from modules.function.Remote import Remote
from modules.function.Sticker import Sticker
from modules.function.Socket import Client
import socket
from modules.function.Broadcast import BroadcastClient

from PyQt5.QtGui import QPixmap
import time

# Main
class StudentService:
    student: Student
    remoteObject: Remote

    def __init__(self):
        ip, name = self.findStudentInfo()
        self.student = Student(ip, name)
        self.remoteObject = Remote()
        self.scrshrObject = Client()
        self.sticker = Sticker('img/sendingImg.gif', xy=[0, 0], on_top=True)

    def excuteInputEvent(self):
        return 0

    def sendScr(self):
        return 0

    def sendRemote(self, remoteScreen):
        # 원격 제어 요청 처리

        # 원격 제어 실행
        self.sticker.show()
        self.remoteObject.startRemote(remoteScreen)

        return 0

    def closeRemote(self):
        self.remoteObject.closeEvent()
        self.sticker.hide()

    def screenShare(self, shareScreen):
        self.scrshrObject.recvScreen(shareScreen)

    def closeScreenShare(self):
        self.scrshrObject.closeEvent()

    def findStudentInfo(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        name = socket.gethostname()
        return ip, name

    def findTeacher(self, status):
        # 브로드캐스팅 수신
        bClient = BroadcastClient(1999)
        bClient.start()
        while True:
            if BroadcastClient.serverIP == "":
                pixmap = QPixmap('resource/FailState.png')
                pixmap = pixmap.scaled(48, 48)
                status.setPixmap(pixmap)
            else:
                pixmap = QPixmap('resource/SuccessState.png')
                status.setPixmap(pixmap)
            teacher = Teacher(BroadcastClient.serverIP)
            self.student.set_teacher(teacher)

            time.sleep(5)
