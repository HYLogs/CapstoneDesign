from domain import *
import base64
from broadcast import *
from time import sleep
from io import BytesIO
import cv2
import numpy as np
import remotecontrol

class TeacherService():
    def __init__(self, teacher: Teacher) -> None:
        self.teacher = teacher
        self.broadcaster = Broadcaster(teacher.get_ip(), 80)
        self.screen_share_continue = True
    
    def start_screen_share(self):
        print("start screen share")
        t = threading.Thread(target=self.back_thread_screen_share)
        t.start()
    
    def back_thread_screen_share(self):
        self.screen_share_continue = True
        
        # TODO 화면 캡쳐
        
        while self.screen_share_continue:
            image = pyautogui.screenshot()
            print(type(image))
        
        # TODO 캡쳐 이미지 브로드캐스팅
            
    def encode_image(self, image):
        '''
        Encoding image for broadcasting
        Args: 
            image: Image to be encoded
        Returns:
            encoded_image: Encoded Image
        '''
        buffer = BytesIO()
        image.save(buffer, format="GIF")
        encoded_image = buffer.getvalue()
        buffer.close()
        return encoded_image
            
    def stop_screen_share(self):
        self.screen_share_continue = False
    
    def remote_controll(self, ip):
        print("remote_controll start")
        remotecontrol.screenShareServer.connectServer(8800)
        pass
    
    def stop_remote_controll(self):
        print("stop_remote controll")
    
    def close(self):
        self.stop_screen_share()
        self.stop_remote_controll()
    
    