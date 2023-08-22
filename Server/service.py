from domain import *
from Broadcast import *
from time import sleep
from utils.ObserverPattern import Observer

from ScreenShare import ScreenShareServer
from threading import Thread

class TeacherService(Observer):
    def __init__(self, config=None) -> None:
        self.config = config
        
        self.teacher = Teacher()
        self.broadcaster = BroadcastServer(self, self.teacher.ip, 1999)
        self.screenshare_server = None
        self.supervision_page = None
        self.students = []

        self.make_students()
        self.apply_config()
        self.broadcaster.start()

    def make_students(self):
        row, col = self.config.table_size
        disables_cnt = len(self.config.disables_pos)
        n = row * col - disables_cnt
        
        for _ in range(n):
            self.students.append(Student())
        
    def apply_config(self):
        # for items, student in zip(self.config.students.items(), self.students):
        #     name, memo = items
        #     student.name = name
        #     student.memo = memo
        
        for name, memo in self.config.students.items():
            idx = int(name[-2:])
            self.students[idx].name = name
            self.students[idx].memo = memo
        
    def update(self):
        students = self.broadcaster.students
        
        for idx, student in enumerate(self.students):
            ip = self.find_ip_by_name(students, student.name)
            name = self.find_name_by_idx(students, idx)
             
            memo = ""
            if student.name in self.config.students.keys():
                memo = self.config.students[student.name]
            
            student.update(ip=ip, name=name, memo=memo)

    def find_ip_by_name(self, students, name):
        for k_name, ip in students.items():
            if k_name == name:
                return ip
        return ""
    
    def find_name_by_idx(self, students, idx):
        for name, ip in students.items():
            try:
                if int(name[-2:]) == idx:
                    return name
            except:
                pass    
            
        return ""
    
    def find_empty_student(self):
        for student in self.students:
            if student.name == "":
                return student
        return None
    
    def find_student_by_index(self, index):
        for student in self.students:
            if student.name == "":
                continue
            elif int(student.name[-2:]) == index:
                return student
        return None
    
    def start_screen_share(self):
        # t = Thread(self.start_screen_share_thread())
        # t.daemon = True
        # t.start()
        
        students = self.broadcaster.students
        self.screenshare_server = ScreenShareServer(students, 2000)
        
        self.screenshare_server.start()
        
    def start_screen_share_thread(self):
        students = self.broadcaster.students
        self.screenshare_server = ScreenShareServer(students, 2000)
        
        self.screenshare_server.start()
    
    def stop_screen_share(self):
        if self.screenshare_server is None:
            return
        self.screenshare_server.stop()
        

    def remote_controll(self, student):
        print("remote_controll start")
        pass

    def stop_remote_controll(self):
        print("stop_remote controll")

    def close(self):
        self.stop_remote_controll()
        self.stop_screen_share()
        self.broadcaster.stop()
        
    def notify(self):
        pass
            
class StudentService():
    def __init__(self):
        pass