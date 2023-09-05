import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from domain import *
from page import *
from broadcast import *
from utils.file import *
from configuration import Configuration
from remote import *

form_class = uic.loadUiType("ui/main.ui")[0]

class Main(QMainWindow, form_class):
    def __init__(self):
        super().__init__()

        self.config = Configuration()

        self.SETTING_PAGE = 0
        self.COMMAND_PAGE = 1
        self.REMOTE_PAGE = 2
        
        self.teacher_service = TeacherService(self.config)

        self.page1 = TableSettingPage(self)
        self.page2 = SupervisionPage(self)
        self.page3 = RemoteControllPage(self)

        self.config.addObserver(self.page2)
        self.config.addObserver(self.teacher_service)

        self.setupUi()
        self.show()

    def setupUi(self):
        super().setupUi(self)

        start_page_index = self.SETTING_PAGE

        if self.config.exist_save():
            start_page_index = self.COMMAND_PAGE
            self.page2.setupUi()

        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)
        self.stackedWidget.addWidget(self.page3)
        
        self.stackedWidget.setCurrentIndex(start_page_index)

    def to_table_setting_page(self):
        self.stackedWidget.setCurrentIndex(self.SETTING_PAGE)

    def to_command_page(self):
        self.stackedWidget.setCurrentIndex(self.COMMAND_PAGE)

    def to_remote_page(self):
        self.stackedWidget.setCureentIndex(self.REMOTE_PAGE)

    def closeEvent(self, event) -> None:
        super().closeEvent(event)
        self.page2.close()
        self.teacher_service.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Main()
    myWindow.show()
    app.exec_()