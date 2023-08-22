from PyQt5.QtWidgets import QApplication, QMainWindow, QSizeGrip
from PyQt5.QtCore import Qt


class MySizeGrip(QSizeGrip):
    def __init__(self, parent, pauseMethod, resumeMethod):
        super().__init__(parent)
        self.pauseMethod = pauseMethod
        self.resumeMethod = resumeMethod

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pauseMethod()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.resumeMethod()
        super().mouseReleaseEvent(event)