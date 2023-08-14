from domain import *
from Broadcast import *
from time import sleep

class TeacherService():
    def __init__(self, teacher: Teacher) -> None:
        self.teacher = teacher
        self.broadcaster = BroadcastServer(teacher.ip, 1999)
        self.screen_share_continue = True
        
        self.find_students()
        
    def find_students(self):
        self.broadcaster.start()
    
    def remote_controll(self, student):
        print("remote_controll start")
        pass
    
    def stop_remote_controll(self):
        print("stop_remote controll")
    
    def close(self):
        self.stop_remote_controll()
    
    