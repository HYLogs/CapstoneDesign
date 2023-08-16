import json
from typing import Dict, Any

def save_json(path:str, data:Dict[Any, Any]):
    with open(path, 'w') as file:
        json.dump(data, file)
        
def load_json(path):
    with open(path, 'r') as file:
        setting = json.load(file)
        return setting