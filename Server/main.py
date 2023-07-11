import sys
from PyQt5 import QtGui, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from domain import *
from page import SupervisionPage

form_class = uic.loadUiType("./Server/ui/main.ui")[0]

class Main(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        # self.loadSetupFile()
        self.setupUi()
        self.show()
        
    def setupUi(self):
        super().setupUi(self)
        
        self.fir_page = SupervisionPage()
        
        self.stackedWidget.addWidget(self.fir_page)
        
    def closeEvent(self, event) -> None:
        super().closeEvent(event)
        self.fir_page.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Main()
    myWindow.show()
    app.exec_()