import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from domain import *
from domain.pages import FirstPage

form_class = uic.loadUiType("./ui/main.ui")[0]

class Main(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        # self.loadSetupFile()
        self.setupUi()
        self.show()
        
    def setupUi(self):
        super().setupUi(self)
        
        self.fir_page = FirstPage.Page()
        
        self.stackedWidget.addWidget(self.fir_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Main()
    myWindow.show()
    app.exec_()