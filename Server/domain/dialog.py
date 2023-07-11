from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class TableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/setConfig.ui", self)
        self.setWindowTitle("Table Setting")
        self.buttonBox.accepted.connect(super().accept)
        self.buttonBox.rejected.connect(super().reject)