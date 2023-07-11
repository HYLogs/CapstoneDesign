class Student():
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name
        
    def get_ip(self):
        return self.ip