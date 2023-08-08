from typing import List
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QStyleOptionViewItem, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, pyqtSlot

from domain import *
from service import *
from page import *
from customWidget import *

import os

import json
from utils.file import save_config

CONNECTED_ICON = "./images/Connected.png"

class SupervisionPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi("ui/command_center.ui", self)
        
        self.main = parent
        self.teacher_service = self.main.teacher_service
        
        self.right_click_pos = None
        
        self.students = []
    
    def setupUi(self):
        self.disables = self.main.disables
        self.table_size = self.main.table_size
        
        self.setting_table()
        self.build_table()
        
        self.screenShareBtn.pressed.connect(self.screen_share_btn_handler)
        self.changeBatchBtn.pressed.connect(self.change_batch_btn_handler)

    def setting_table(self):
        print("setting page")
        row, col = self.main.table_size
        
        # 테이블 행열 크기 설정
        self.studentTable.setRowCount(row)
        self.studentTable.setColumnCount(col)
        
        # 테이블 빈공간 없애기
        self.studentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.studentTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def get_students(self): # TODO 통신을 통해 학생의 데이터를 받아온다.
        '''
        학생 데이터를 받아온다.
        '''
        print("get students")
        
        for i in range(38):
            self.students.append(Student("192.168.10." + str(i + 1), "port", "312_" + "{:02d}".format(i + 1)))

    def build_table(self):
        '''
        학생 자리 테이블을 생성한다.
        '''
        print("start table building")
        index = 0
        row, col = self.table_size
        
        for i in range(row):
            for j in range(col):
                student = Student(f"192.168.1.{index}", f"8080", f"E303_COM{index}", f"{index}번 PC입니다.")
                
                index += 1
                
                if [i, j] not in self.disables:
                    item = TableItem(self.studentTable, student)
                    if index < len(self.students):
                        index += 1
                else:
                    item = TableItem(self.studentTable)
                    # TODO 자리가 비활성화인 경우
                    pass
                    # item.setDisabled(True)
                
                self.studentTable.setCellWidget(i, j, item)
                
        if index < len(self.students):
            # TODO 테이블 크기 에러 출력
            reply = QMessageBox.information(self, "경고", "학생PC의 수가 자리에 비해 더 많습니다. 배치를 변경하시겠습니까? \
                \n변경하지 않는다면 생략되는 학생PC가 존재할 수 있습니다!", \
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            
            if reply == QMessageBox.Yes:
                self.change_batch_btn_handler()
                
    def screen_share_btn_handler(self):
        if self.screen_share_btn.text() == "화면 공유 시작":
            self.teacher_service.start_screen_share()
            self.screen_share_btn.setText("화면 공유 중지")
        else:
            self.teacher_service.stop_screen_share()
            self.screen_share_btn.setText("화면 공유 시작")
        
    def change_batch_btn_handler(self):
        self.main.to_table_setting_page()
        
    def closeEvent(self, event):
        super().closeEvent(event)
        self.teacher_service.close()
        
    def dragEnterEvent(self, a0: QDragEnterEvent) -> None:
        print("drag")
        return super().dragEnterEvent(a0)
        
class RemoteControllPage(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        uic.loadUi("ui/remote_controll.ui", self)
        self.main = parent
        
        self.endRemoteControllBtn.clicked.connect(self.end_btn_handler)
                
    def end_btn_handler(self):
        # TODO 통신 종료
        self.main.teacher_service.stop_remote_controll()
        
        self.main.to_command_page()
        
    def close(self):
        pass
    
class TableSettingPage(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        uic.loadUi("ui/table_setting.ui", self)
        
        delegate = IconDelegate(self.table)
        self.table.setItemDelegate(delegate)
        self.table.setIconSize(QSize(45, 45))
        
        self.main = parent
        self.disable_pos = parent.disables
        self.table_size = parent.table_size

        self.build_table()
        
        self.addRowBtn.pressed.connect(self.add_row)
        self.rmRowBtn.pressed.connect(self.rm_row)
        self.addColBtn.pressed.connect(self.add_col)
        self.rmColBtn.pressed.connect(self.rm_col)
        
        self.toggleEnableBtn.pressed.connect(self.toggle_enable)
        
        self.resetBtn.pressed.connect(self.reset_btn_handler)
        self.saveBtn.pressed.connect(self.save_btn_handler)

    def build_table(self) -> None:
        row, col = self.table_size
        
        self.table.setRowCount(row)
        self.table.setColumnCount(col)
        
        self.resize_table()
        
        self.add_icon()
        
    def resize_table(self) -> None:
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def add_icon(self) -> None:
        row = self.table.rowCount()
        col = self.table.columnCount()
        
        for i in range(row):
            for j in range(col):
                cell = QTableWidgetItem()

                if [i, j] not in self.disable_pos:
                    icon = self.make_icon()
                    cell.setIcon(icon)
                self.table.setItem(i, j, cell)
                
    def make_icon(self) -> None:
        icon = QIcon()
        
        pixmap = QPixmap(CONNECTED_ICON)
        pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        icon.addPixmap(pixmap)
        
        return icon
        
    def add_row(self) -> None:
        self.table.setRowCount(self.table.rowCount() + 1)
        self.table_size[0] += 1
        self.build_table(self.table.rowCount(), self.table.columnCount())
        
    def rm_row(self) -> None:
        index = self.table.rowCount() - 1
        if index < 1:
            print("행이 최소 1 이상이어야 합니다.")
            return
        self.table.removeRow(index)
        self.table_size[0] -= 1
        self.resize_table()
        self.build_table(self.table.rowCount(), self.table.columnCount())
        
    def add_col(self) -> None:
        self.table.setColumnCount(self.table.columnCount() + 1)
        self.table_size[1] += 1
        self.build_table()
        
    def rm_col(self) -> None:
        index = self.table.columnCount() - 1
        if index < 1:
            print("행이 최소 1 이상이어야 합니다.")
            return
        self.table.removeColumn(index)
        self.table_size[1] -= 1
        self.resize_table()
        self.build_table()
        
    def reset_btn_handler(self) -> None:
        self.rm_setting_file()
        self.build_table()
        
    def rm_setting_file(self) -> None:
        if os.path.exists(self.main.setting_path):
            os.remove(self.main.setting_path)
        self.build_table()
        
    def save_btn_handler(self) -> None:
        dialog = SaveDialog(self)
        dialog.show()
        if dialog.exec_() == QDialog.Accepted:
            self.save_batch()
            self.main.load_setting(self.main.setting_path)
            self.main.to_command_page()
            
    def save_batch(self) -> None:
        # 테이블 row, col 불러오기
        row = self.table.rowCount()
        col = self.table.columnCount()
        
        disable_pos = []
        
        for i in range(row):
            for j in range(col):
                item = self.table.item(i, j)
                if item is None:
                    continue
                
                if not self.check_enable(item):
                    disable_pos.append((i, j))
        
        save_config(self.main.setting_path, table_size=(row, col), disables=disable_pos)

    def check_enable(self, item:QTableWidgetItem) -> bool:
        return not item.icon().isNull()
    
    def toggle_enable(self) -> None:      
        for item in self.table.selectedItems():
            i, j = item.row(), item.column()
            
            if self.check_enable(item):
                self.table.removeCellWidget(i, j)
                self.table.setItem(i, j, QTableWidgetItem())
                self.disable_pos.append((i, j))
            else:
                self.disable_pos.remove((i, j))
                item.setIcon(QIcon("./images/Connected.png"))
                
    def apply_setting(self, setting:Dict):
        self.disable_pos = setting['disables']
        self.table_size = setting['table_size']
                
                
class IconDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(IconDelegate, self).initStyleOption(option, index)
        if option.features & QStyleOptionViewItem.HasDecoration:
            s = option.decorationSize
            s.setWidth(option.rect.width())
            option.decorationSize = s
                
class SaveDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("./ui/save_dialog.ui", self)