import json

def save_config(path:str, **kwargs):
    with open(path, 'w') as file:
            json.dump(kwargs, file)