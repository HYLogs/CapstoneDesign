import os

class Configuration:
    def __init__(self, path:str):
        if not os.path.exists(path):
            raise ValueError("올바른 경로가 아닙니다.")
        
        self.config_path = path
        
    def load_config(self, path):
        pass
    
    def save_config(self):
        pass