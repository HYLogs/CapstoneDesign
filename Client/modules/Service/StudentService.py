from modules.domain.Student import Student
from modules.domain.Teacher import Teacher
import socket


class StudentService:
    student: Student

    def __init__(self):
        ip, name = self.findStudentInfo()
        self.student = Student(ip, name)

    def excuteInputEvent(self):
        return 0

    def sendScr(self):
        return 0

    def sendRemote(self):
        return 0

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
