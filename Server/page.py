from typing import Tuple, List
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QStyleOptionViewItem, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QPoint, pyqtSlot

from domain import *
from service import *
from page import *

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
        self.set_table_context_menu()
        
        self.screenShareBtn.pressed.connect(self.screen_share_btn_handler)
        self.changeBatchBtn.pressed.connect(self.change_batch_btn_handler)

    def setting_table(self):
        row, col = self.main.table_size
        
        # 테이블 행열 크기 설정
        self.studentTable.setRowCount(row)
        self.studentTable.setColumnCount(col)
        
        # 테이블 빈공간 없애기
        self.studentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.studentTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def set_table_context_menu(self):
        self.studentTable.customContextMenuRequested.connect(self.context_menu)
        
        show_detail_action = QAction("상세정보", self.studentTable)
        
        self.studentTable.addAction(show_detail_action)
        
        show_detail_action.triggered.connect(self.show_detail)
        
    @pyqtSlot(QPoint)
    def context_menu(self, position):
        menu = QMenu()
        
        
    def show_detail(self, event):
        print(type(event))

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
                item = TableItem([i, j])
                
                if [i, j] not in self.disables:
                    if index < len(self.students):
                        index += 1
                else:
                    item.setDisabled(True)
                
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
        
    def table_mouse_press_handler(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.table_right_mouse_press_handler(event)
            
    def table_right_mouse_press_handler(self, event):
        '''
        테이블에서 우클릭 시 컨텍스트 메뉴를 표시한다.
        '''
        self.right_click_pos = event.pos()
        
        # 컨텍스트 메뉴 생성
        context_menu = QMenu(self)
        
        remote_controll_action = QAction("원격제어", self)

        remote_controll_action.triggered.connect(self.remote_controll_triggered_handler)
        
        context_menu.addAction(remote_controll_action)
        
        # 컨텍스트 메뉴 표시
        context_menu.exec_(self.mapToGlobal(event.pos()))
        
    def remote_controll_triggered_handler(self):
        table_item = self.get_event_target()
        self.main.teacher_service.remote_controll(table_item.ip)
        
        self.main.to_remote_page()
        
    def get_event_target(self):
        index = self.studentTable.indexAt(self.right_click_pos)
        row = index.row()
        col = index.column()
        table_item = self.studentTable.cellWidget(row, col)
        return table_item
        
    def remote_controll(self):
        print("원격제어 실행")
        
    def closeEvent(self, event):
        super().closeEvent(event)
        self.teacher_service.close()
            
class TableItem(QWidget):
    def __init__(self, pos:list, ip="", name=""):
        super().__init__()
        uic.loadUi("ui/table_item.ui", self)
        self.pos = pos
        self.ip = ip
        self.name = name
        self.disable = False
        
        self.setText()

    def clear(self):
        self.ip = ""
        self.name = ""
        self.setText()
        
    def setDisabled(self, a0: bool) -> None:
        super().setDisabled(a0)
        self.disable = a0
        
    def add_student_info(self, student:Student):
        self.ip = student.get_ip()
        self.name = student.get_name()
        
        self.setText()
        
    def setText(self):
        self.ip_label.setText(self.ip)
        self.name_label.setText(self.name)
    
    def get_pos(self):
        return self.pos
        
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

        self.build_table(*parent.table_size)
        
        self.addRowBtn.pressed.connect(self.add_row)
        self.rmRowBtn.pressed.connect(self.rm_row)
        self.addColBtn.pressed.connect(self.add_col)
        self.rmColBtn.pressed.connect(self.rm_col)
        
        self.toggleEnableBtn.pressed.connect(self.toggle_enable)
        
        self.resetBtn.pressed.connect(self.reset_btn_handler)
        self.saveBtn.pressed.connect(self.save_btn_handler)

    def build_table(self, row:int = 7, col:int = 6) -> None:
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

                if (i, j) not in self.disable_pos:
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
        self.build_table(self.table.rowCount(), self.table.columnCount())
        
    def rm_row(self) -> None:
        index = self.table.rowCount() - 1
        if index < 1:
            print("행이 최소 1 이상이어야 합니다.")
            return
        self.table.removeRow(index)
        self.resize_table()
        self.build_table(self.table.rowCount(), self.table.columnCount())
        
    def add_col(self) -> None:
        self.table.setColumnCount(self.table.columnCount() + 1)
        self.build_table(self.table.rowCount(), self.table.columnCount())
        
    def rm_col(self) -> None:
        index = self.table.columnCount() - 1
        if index < 1:
            print("행이 최소 1 이상이어야 합니다.")
            return
        self.table.removeColumn(index)
        self.resize_table()
        self.build_table(self.table.rowCount(), self.table.columnCount())
        
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