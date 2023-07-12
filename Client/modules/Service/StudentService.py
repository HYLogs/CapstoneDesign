from modules.domain.Student import Student
from modules.domain.Teacher import Teacher
from modules.function.Remote import Remote
from modules.function.Sticker import Sticker
import socket

# Main
class StudentService:
    student: Student
    remoteObject: Remote

    def __init__(self):
        ip, name = self.findStudentInfo()
        self.student = Student(ip, name)
        self.remoteObject = Remote()
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
