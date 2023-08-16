from typing import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from service import *

class ComputerInfoDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("./ui/detail_dialog.ui", self)

    def set_ip(self, ip):
        self.ipLineEdit.setText(ip)

    def set_name(self, name):
        self.nameLineEdit.setText(name)

    def set_detail(self, detail):
        self.detailTextEdit.setText(detail)

class TableItem(QWidget):
    def __init__(self, parent:QTableWidget, student:Student = None) -> None:
        super().__init__()
        uic.loadUi("./ui/table_item.ui", self)

        self.table = parent

        if student.is_connected:
            self.img = "./images/Connected.png"
        else:
            self.img = "./images/Disconnected.png"
        self._ip = student.ip
        self._name = student.name
        self._detail = student.memo
        self.student = student
        self.setupUi()

    def setupUi(self) -> None:
        pixmap = QPixmap(self.img)
        self.image.setPixmap(pixmap)

        self.name.setText(self._name)
        self.ip.setText(self._ip)
        self.detail.setText(self._detail)

    def set_context_menu(self):
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        self.create_context_menu(pos)

    def create_context_menu(self, pos):
        context_menu = QMenu(self)

        show_detail_action = QAction("상세정보", context_menu)
        remote_controll_action = QAction("원격제어", context_menu)
        
        context_menu.addAction(show_detail_action)
        context_menu.addAction(remote_controll_action)
        
        show_detail_action.triggered.connect(self.show_detail)
        remote_controll_action.triggered.connect(self.remote_controll)

        # ContextMenu를 보여줍니다.
        context_menu.exec_(pos)
        
    def show_detail(self):
        dialog = ComputerInfoDialog()
        dialog.set_ip(self._ip)
        dialog.set_name(self._name)
        dialog.set_detail(self._detail)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            new_detail = dialog.detailTextEdit.toPlainText()
            
            self._detail = new_detail
            self.student.memo = new_detail
            self.detail.setText(new_detail)
        
    def remote_controll(self):
        teacher = Teacher()
        service = TeacherService(teacher)
        service.remote_controll(self.student)
    
    def set_ip(self, ip:str):
        self.ip = ip
    
    def set_name(self, name:str):
        self.name = name
        
    def set_detail(self, detail:str):
        self.detail = detail
        
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            pos = event.globalPos()
            self.show_context_menu(pos)