import sys
from PyQt5 import QtGui, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from domain import *
from page import *

form_class = uic.loadUiType("ui/main.ui")[0]

class Main(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        # self.loadSetupFile()

        self.teacher_service = TeacherService(Teacher())
        
        self.setupUi()
        self.show()
        
    def setupUi(self):
        super().setupUi(self)
        
        self.fir_page = SupervisionPage(self)
        self.sec_page = RemoteControllPage(self)
        
        self.stackedWidget.addWidget(self.fir_page)
        self.stackedWidget.addWidget(self.sec_page)
        
    def next_page(self):
        new_index = self.stackedWidget.currentIndex() + 1
        if new_index < len(self.stackedWidget):
            self.stackedWidget.setCurrentIndex(new_index)

    def prev_page(self):
        new_index = self.stackedWidget.currentIndex() - 1
        if new_index >= 0:
            self.stackedWidget.setCurrentIndex(new_index)    
    
    def closeEvent(self, event) -> None:
        super().closeEvent(event)
        self.fir_page.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Main()
    myWindow.show()
    app.exec_()