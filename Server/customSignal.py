from PyQt5.QtCore import QObject, pyqtSignal

class CustomSignal(QObject):
    changed = pyqtSignal()