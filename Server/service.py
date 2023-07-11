from domain import *
import base64
from broadcast import *
from time import sleep
from io import BytesIO
import cv2
import numpy as np

class TeacherService():
    def __init__(self, teacher: Teacher) -> None:
        self.teacher = teacher
        self.capture = Capture()
        self.broadcaster = Broadcaster(teacher.get_ip(), 80)
        self.trigger = True
    
    def start_screen_share(self):
        print("start screen share")
        t = threading.Thread(target=self.back_tread_screen_share)
        t.start()
    
    def back_tread_screen_share(self):
        self.trigger = True
        self.capture.start_capture()
        
        image = None
        
        while self.trigger:
            sleep(1)
            print("broad casting")
            if len(self.capture.stream) > 0:
                image = self.capture.stream.pop(0)

            if image is None:
                continue

            encoded_image = self.encode_image(image)
            
                # TODO 이미지 브로드 캐스팅
            self.broadcaster.broadcast(encoded_image)
            
    def encode_image(self, image):
        buffer = BytesIO()
        image.save(buffer, format="GIF")
        encoded_image = buffer.getvalue()
        buffer.close()
        return encoded_image
            
    def stop_screen_share(self):
        self.capture.stop_capture()
        self.trigger = False
    
    def remote_controll(self, student):
        pass
    
    def close(self):
        self.capture.stop_capture()
    
    