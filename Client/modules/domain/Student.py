from modules.domain.Teacher import Teacher


class Student:
    ip: str
    name: str
    teacher: Teacher

    def __init__(self, ip: str, name: str):
        self.ip = ip
        self.name = name

    def __str__(self):
        return self.ip + " " + self.name

    def set_teacher(self, teacher: Teacher):
        self.teacher = teacher
