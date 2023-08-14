import os
import json
from typing import Dict
from utils.file import *

class Configuration(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, path:str=None):
        cls = type(self)
        if not hasattr(cls, "_init"):
            config = {}
            
            if os.path.exists(path):
                self.path = path
                config = self.load_config()
                
            self.config = config
            cls._init = True
        
    def load_config(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as file:
                config = json.load(file)
                return config
        else:
            raise ValueError("저장된 설정 파일이 없습니다.")
    
    def save_config(self):
        with open(self.path, 'w') as file:
            json.dump(self.config, file)

    def set_config(self, **kwargs):
        self.config.update(kwargs)