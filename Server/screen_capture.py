from pyautogui import screenshot

class CaptureStream():
    def __init__(self):
        self.list = []
    
    def put(self, image):
        self.list.append(image)

    def pop(self):
        return self.list.pop(0)


class Capture():
    def __init__(self, stream=CaptureStream()):
        self.stream = stream
        self.exit_flag = True

    def doScreenCapture(self):
        image = screenshot()
        self.stream.put(image)

    def getStream(self):
        return self.stream.pop()

