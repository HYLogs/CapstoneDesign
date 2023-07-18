import socket
import pyautogui
from PyQt5 import uic
from PyQt5.QtWidgets import *
from threading import Thread

class Student():
    def __init__(self, ip:str, port:str, name:str):
        self.ip = ip
        self.port = port
        self.name = name
        self.disable = False
        
    def get_ip(self):
        return self.ip
    
    def get_name(self):
        return self.name
    
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
    
    def get_ip(self) -> int:
        return self.ip