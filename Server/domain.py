import socket
from PyQt5.QtWidgets import *

class Student():
    def __init__(self, ip:str, port:str, name:str, detail:str):
        self.ip = ip
        self.port = port
        self.name = name
        self.detail = detail
        self.disable = False
        
    def get_ip(self):
        return self.ip
    
    def get_name(self):
        return self.name
    
    def get_detail(self):
        return self.detail
    
    def set_disabled(self, a:bool):
        self.disable = a
    
class Teacher():
    def __init__(self) -> None:
        self.ip, self.name = self.find_ip_and_name()
    
    def find_ip_and_name(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        name = socket.gethostname()
        return ip, name