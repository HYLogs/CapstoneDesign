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
        
    def get_ip(self):
        return self.ip
    
    def get_name(self):
        return self.name
    
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
    
class Capture():
    def __init__(self, stream = []) -> None:
        self.stream = stream
        self.trigger = True
        
    def start_capture(self):
        t = Thread(target=self.capture)
        t.start()
            
    def capture(self):
        while self.trigger:
            self.stream.append(pyautogui.screenshot())
            
    def stop_capture(self):
        self.trigger = False
        
