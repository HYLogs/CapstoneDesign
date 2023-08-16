import os
import json
from typing import Dict, Tuple, List, Any
from utils.file import *
from utils.ObserverPattern import Observer, Subject

class Configuration(Subject):
    def __init__(self):
        self.path = "./setting.json"
        self.observers = []
        self.table_size = [7, 6]
        self.disables_pos = []
        self.students = {}
        
        if self.exist_save():
            save = self.load_save()
            self.table_size = save['table_size']
            self.disables_pos = save['disables_pos']
            self.students = save['students']
        
    def addObserver(self, observer: Observer) -> None:
        self.observers.append(observer)
        
    def removeObserver(self, observer: Observer) -> None:
        self.observers.remove(observer)
    
    def notifyObservers(self) -> None:
        for observer in self.observers:
            observer.notify()
            
    def add_disable_pos(self, pos:List[int]) -> None:
        self.disables_pos.append(pos)
        
    def remove_disable_pos(self, pos:List[int]) -> None:
        self.disables_pos.remove(pos)
            
    def update(self, table_size:List[int] = [7, 6], disables_pos:List[List[int]] = []):
        self.table_size = table_size
        self.disables_pos = disables_pos
                
    def exist_save(self):
        return os.path.exists(self.path)
        
    def load_save(self):
        return load_json(self.path)
    
    def clear_config(self):
        if os.path.exists(self.path):
            self.update()
            self.save()
            
    def save(self):
        config = {"table_size": self.table_size,
                  "disables_pos": self.disables_pos,
                  "students": self.students}
        
        save_json(self.path, config)
        self.notifyObservers()