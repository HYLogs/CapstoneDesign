import json
import os

def save_config(path:str, **kwargs):
    with open(path, 'w') as file:
        json.dump(kwargs, file)
        
def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            setting = json.load(file)
            return setting
    else:
        raise ValueError("저장된 파일이 없습니다.")