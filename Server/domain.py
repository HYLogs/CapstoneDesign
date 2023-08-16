import socket
from PyQt5.QtWidgets import *

class Student():
    def __init__(self, ip:str=None, name:str=None, memo:str=None, is_connected:bool=False):
        self.ip = ip
        self.name = name
        self.memo = memo
        self.is_connected = is_connected
    
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