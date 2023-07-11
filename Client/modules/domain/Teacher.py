class Teacher:
    ip: str
    port: int
    name: str

    def __init__(self, ip: str, port: int, name: str):
        self.ip = ip
        self.port = port
        self.name = name
