from domain import *
from Broadcast import *
from time import sleep
from utils.ObserverPattern import Observer

class TeacherService(Observer):
    def __init__(self, config) -> None:
        self.config = config
        
        self.teacher = Teacher()
        self.broadcaster = BroadcastServer(self, self.teacher.ip, 1999)
        self.students = []

        self.make_students()
        self.apply_config()

    def make_students(self):
        row, col = self.config.table_size
        disables_cnt = len(self.config.disables_pos)
        n = row * col - disables_cnt
        
        for i in range(n):
            self.students.append(Student())
        
    def apply_config(self):
        for items, student in zip(self.config.students.items(), self.students):
            name, memo = items
            student.name = name
            student.memo = memo
        
    def update(self):
        students = self.broadcaster.students
        new_students = []
        
        for name, ip in students.items():
            student = self.find_student_by_name(self, name)
            if student is not None:
                self.students.remove(student)
                student.ip = ip
                new_students.append(student)
            else:
                new_students.append(Student(ip, name))
        
    def find_student_by_name(self, name):
        for student in self.students:
            if student.name == name:
                return student
        return None
    
    def find_student_by_index(self, index):
        for student in self.students:
            if student.name[-2:] == index:
                return student
        return None

    def remote_controll(self, student):
        print("remote_controll start")
        pass

    def stop_remote_controll(self):
        print("stop_remote controll")

    def close(self):
        self.stop_remote_controll()
        self.broadcaster.stop()
        
    def notify(self):
        pass
        
    def update(self):
        self.config.table_size()
            
class StudentService():
    def __init__(self):
        pass