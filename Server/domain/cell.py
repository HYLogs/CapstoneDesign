from PyQt5.QtWidgets import *
from PyQt5 import QtGui, uic, QtCore, Qt
from PyQt5.QtGui import QContextMenuEvent

class Cell(QWidget):
    def __init__(self, number="", ip=""):
        super().__init__()
        uic.loadUi("./ui/cell.ui", self)
        self.disabled = False
        self.setupUi(number, ip)

    def setupUi(self, number, ip):
        self.setData(number, ip)

    def clear(self):
        self.number.setText("")
        self.ip.setText("")
        
    def setData(self, number, ip):
        self.number.setText(number)
        self.ip.setText("")
        
    def setDisabled(self):
        self.disabled = True
        
    def setEnabled(self):
        self.disabled = False
        
    def isDisabled(self):
        return self.disabled == True