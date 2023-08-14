import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from domain import *
from page import *
from Broadcast import *
import json

form_class = uic.loadUiType("ui/main.ui")[0]

CONFIG_PATH = "./setting.json"

class Main(QMainWindow, form_class):
    def __init__(self, setting_path):
        super().__init__()
        self.config = Configuration(CONFIG_PATH)
        
        self.SETTING_PAGE = 0
        self.COMMAND_PAGE = 1
        self.REMOTE_PAGE = 2
        
        self.setting_path = setting_path
        self.setting = None
        self.teacher = Teacher()
        
        self.teacher_service = TeacherService(self.teacher)
        self.broadcaster = BroadcastServer(self.teacher.ip, 1919)
        self.broadcaster.start()
        self.setupUi()
        self.show()
        
    def setupUi(self):
        super().setupUi(self)
        
        start_page_index = self.SETTING_PAGE
        
        self.table_size = (7, 6)
        self.disables = []
        
        self.page1 = TableSettingPage(self)
        self.page2 = SupervisionPage(self)
        self.page3 = RemoteControllPage(self)
        
        if self.load_setting(self.setting_path):
            start_page_index = self.COMMAND_PAGE
            self.page2.setupUi()
        
        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)
        self.stackedWidget.addWidget(self.page3)
        self.stackedWidget.currentChanged.connect(self.page_change_handler)
        
        self.stackedWidget.setCurrentIndex(start_page_index)
    
    def load_setting(self, path):
        if os.path.exists(path):
            with open(path, 'r') as file:
                setting = json.load(file)
            self.setting = setting
            self.table_size = setting["table_size"]
            self.disables = setting["disables"]
            return True
        return False

    def page_change_handler(self):
        if self.stackedWidget.currentIndex() == self.COMMAND_PAGE:
            self.page2.studentTable.clear()
            self.page2.setupUi()
            
    def to_table_setting_page(self):   
        if self.setting is not None:
            self.page1.apply_setting(self.setting)
            self.page1.build_table()  
        self.stackedWidget.setCurrentIndex(self.SETTING_PAGE)
        
    def to_command_page(self):
        self.stackedWidget.setCurrentIndex(self.COMMAND_PAGE)
        
    def to_remote_page(self):
        self.stackedWidget.setCureentIndex(self.REMOTE_PAGE)
    
    def closeEvent(self, event) -> None:
        super().closeEvent(event)
        self.page2.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Main(CONFIG_PATH)
    myWindow.show()
    app.exec_()