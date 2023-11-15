from typing import List
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QStyleOptionViewItem, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, pyqtSlot
from threading import Thread

from domain import *
from service import *
from page import *
from customWidget import *

from utils.ObserverPattern import Observer

class TableSettingPage(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        uic.loadUi("ui/table_setting.ui", self)
        
        delegate = IconDelegate(self.table)
        self.table.setItemDelegate(delegate)
        self.table.setIconSize(QSize(45, 45))
        
        self.icon_path = "./images/pc.png"
        self.parent = parent
        self.config = parent.config
        
        self.setupUi()
        
    def setupUi(self):
        self.build_table()
        
        self.addRowBtn.pressed.connect(self.add_row)
        self.rmRowBtn.pressed.connect(self.rm_row)
        self.addColBtn.pressed.connect(self.add_col)
        self.rmColBtn.pressed.connect(self.rm_col)
        
        self.toggleEnableBtn.pressed.connect(self.toggle_enable)
        
        self.resetBtn.pressed.connect(self.reset_btn_handler)
        self.saveBtn.pressed.connect(self.save_btn_handler)
        

    def build_table(self) -> None:
        self.apply_config()
        self.resize_table()
        self.add_icon()
        
    def resize_table(self):
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def apply_config(self):
        row, col = self.config.table_size
        
        self.table.setRowCount(row)
        self.table.setColumnCount(col)
        
    def add_icon(self) -> None:
        row = self.table.rowCount()
        col = self.table.columnCount()
        
        for i in range(row):
            for j in range(col):
                cell = QTableWidgetItem()

                if [i, j] not in self.config.disables_pos:
                    icon = self.make_icon()
                    cell.setIcon(icon)
                self.table.setItem(i, j, cell)
                
    def make_icon(self) -> None:
        icon = QIcon()
        
        pixmap = QPixmap(self.icon_path)
        pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        icon.addPixmap(pixmap)
        
        return icon
        
    def add_row(self) -> None:
        self.table.setRowCount(self.table.rowCount() + 1)
        self.config.table_size[0] += 1
        self.build_table()
        
    def rm_row(self) -> None:
        index = self.table.rowCount() - 1
        if index < 1:
            print("행이 최소 1 이상이어야 합니다.")
            return
        self.table.removeRow(index)
        self.config.table_size[0] -= 1
        self.resize_table()
        self.build_table()
        
    def add_col(self) -> None:
        self.table.setColumnCount(self.table.columnCount() + 1)
        self.config.table_size[1] += 1
        self.build_table()
        
    def rm_col(self) -> None:
        index = self.table.columnCount() - 1
        if index < 1:
            print("행이 최소 1 이상이어야 합니다.")
            return
        self.table.removeColumn(index)
        self.config.table_size[1] -= 1
        self.resize_table()
        self.build_table()
        
    def reset_btn_handler(self) -> None:
        self.config.clear_config()
        self.build_table()
        
    def save_btn_handler(self) -> None:
        dialog = SaveDialog(self)
        dialog.show()
        if dialog.exec_() == QDialog.Accepted:
            self.save_batch()
            self.config.save()
            self.parent.to_command_page()
            
    def save_batch(self) -> None:
        # 테이블 row, col 불러오기
        row = self.table.rowCount()
        col = self.table.columnCount()
        
        table_size = [row, col]
        
        disables_pos = []
        
        for i in range(row):
            for j in range(col):
                item = self.table.item(i, j)
                if item is None:
                    continue
                
                if not self.check_enable(item):
                    disables_pos.append([i, j])
        
        self.config.update(table_size, disables_pos)

    def check_enable(self, item:QTableWidgetItem) -> bool:
        return not item.icon().isNull()
    
    def toggle_enable(self) -> None:      
        for item in self.table.selectedItems():
            i, j = item.row(), item.column()
            
            if self.check_enable(item):
                self.table.removeCellWidget(i, j)
                self.table.setItem(i, j, QTableWidgetItem())
                self.config.add_disable_pos([i, j])
            else:
                self.config.remove_disable_pos([i, j])
                icon = self.make_icon()
                item.setIcon(icon)
                
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
        
class SupervisionPage(QWidget, Observer):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi("ui/command_center.ui", self)
        
        self.config = parent.config
        self.teacher_service = parent.teacher_service
        self.teacher_service.supervision_page = self
        self.parent = parent
        
        self.right_click_pos = None

    def setupUi(self):        
        self.build_table()

        self.screenShareBtn.pressed.connect(self.screen_share_btn_handler)
        self.changeBatchBtn.pressed.connect(self.change_batch_btn_handler)

    def get_students(self): # TODO 통신을 통해 학생의 데이터를 받아온다.
        '''
        학생 데이터를 받아온다.
        '''
        students = self.teacher_service.get_students()            

    def build_table(self):
        '''
        학생 자리 테이블을 생성한다.
        '''
        self.apply_config()
        self.resize_table()

        row, col = self.config.table_size

        index = 0

        for i in range(row):
            for j in range(col):
                if self.check_pos(i, j):
                    student = self.teacher_service.students[index]
                    item = TableItem(self.studentTable, student, config=self.config, service=self.teacher_service)
                    student.addObserver(item)
                    index += 1
                    self.studentTable.setCellWidget(i, j, item)
                
    def check_pos(self, i, j):
        for row, col in self.config.disables_pos:
            if row == i and col == j:
                return False
        return True
                
    def apply_config(self):
        row, col = self.config.table_size
        
        self.studentTable.setRowCount(row)
        self.studentTable.setColumnCount(col)            
    
    def resize_table(self):
        self.studentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.studentTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
                
    def screen_share_btn_handler(self):
        if self.screenShareBtn.text() == "화면 공유 시작":
            # t = Thread(self.teacher_service.start_screen_share())
            # t.daemon = True
            # t.start()
            self.teacher_service.start_screen_share()
            self.screenShareBtn.setText("화면 공유 중지")
        else:
            self.teacher_service.stop_screen_share()
            self.screenShareBtn.setText("화면 공유 시작")
        
    def change_batch_btn_handler(self):
        self.parent.to_table_setting_page()
        
    def closeEvent(self, event):
        super().closeEvent(event)
        
        row, col = self.config.table_size
        
        for i in range(row):
            for j in range(col):
                item = self.studentTable.cellWidget(i, j)
                if item is None:
                    continue
                student = item.student
                self.config.students[student.name] = student.memo
                
        self.config.save()
                
    def notify(self):
        self.studentTable.clear()
        self.build_table()
        
    # def update(self):
    #     students = self.teacher_service.students
    #     students.sort(key=lambda x:x.name)
        
    #     row, col = self.config.table_size
        
    #     index = 0
    #     for i in range(row):
    #         for j in range(col):
    #             if self.check_pos(i, j):
    #                 item = self.studentTable.cellWidget(i, j)
    #                 item.set_student(students[index])
    #                 index += 1
            

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