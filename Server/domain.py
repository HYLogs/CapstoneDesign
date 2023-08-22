import socket
from PyQt5.QtWidgets import *
from utils.ObserverPattern import *
from utils.ObserverPattern import Observer
from customSignal import *

class Student(Subject):
    def __init__(self, ip:str="", name:str="", memo:str="", is_connected:bool=False):
        self.observers = []
        self.ip = ip
        self.name = name
        self.memo = memo
        self.is_connected = is_connected
        self.signal = CustomSignal()
        self.signal.changed.connect(self.notifyObservers)
        
    def addObserver(self, observer: Observer) -> None:
        self.observers.append(observer)
        
    def removeObserver(self, observer: Observer) -> None:
        self.observers(observer)
    
    def notifyObservers(self) -> None:
        for observer in self.observers:
            observer.notify()
            
    def update(self, ip="", name="", memo=""):
        self.ip=ip
        self.name=name
        self.memo=memo
        
        self.signal.changed.emit()
    
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