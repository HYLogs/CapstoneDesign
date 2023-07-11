from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore

from domain import *
from service import *
from page import *

import json
import os

CONFIG_PATH = "./Server/setting.json"

class SupervisionPage(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("./Server/ui/command_center.ui", self)
        
        if os.path.exists(CONFIG_PATH):
            setting = self.load_setting()
            row, col = setting['row'], setting['col']
        else:
            row, col = self.get_table_setting_input()
        
        self.row = row
        self.col = col
        
        self.save_config()
        
        self.teacher = Teacher()
        self.teacher_service = TeacherService(self.teacher)
        
        self.right_click_pos = None
        
        self.students = [0 for _ in range(self.row * self.col)]
        
        self.setupUi()
        
    def load_setting(self):
        with open(CONFIG_PATH, 'r') as file:
            setting = json.load(file)
            return setting
    
    def get_table_setting_input(self):
        dialog = TableSettingDialog()
        if dialog.exec_() == QDialog.Accepted:
            row = int(dialog.row_text_edit.toPlainText())
            col = int(dialog.col_text_edit.toPlainText())
        
        return row, col
    
    def setupUi(self):
        self.setting_table()
        self.get_students()
        self.build_table()
        
        self.screen_share_btn.clicked.connect(self.screen_share_btn_handler)
        self.setting_btn.clicked.connect(self.setting_btn_handler)
        self.student_table.mousePressEvent = self.table_mouse_press_handler
        
    def setting_table(self):            
        # 테이블 행열 크기 설정
        self.student_table.setRowCount(self.row)
        self.student_table.setColumnCount(self.col)
        
        # 테이블 행열 헤더 제거
        self.student_table.horizontalHeader().setVisible(False)
        self.student_table.verticalHeader().setVisible(False)
        
        # 테이블 빈공간 없애기
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.student_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def get_students(self): # TODO 통신을 통해 학생의 데이터를 받아온다.
        '''
        학생 데이터를 받아온다.
        '''
        print("get students")
        
        for i in range(10):
            self.students[0] = Student("ip", "port", "name")

    def build_table(self):
        '''
        학생 자리 테이블을 생성한다.
        '''
        print("start table building")
        index = 0
        
        for i in range(self.row):
            for j in range(self.col):
                item = TableItem((i, j))
                if self.students[index]:
                    student = self.students[index]
                    item.add_student_info(student)
                
                self.student_table.setCellWidget(i, j, item)
                
    def screen_share_btn_handler(self):
        if self.screen_share_btn.text() == "화면 공유 시작":
            self.teacher_service.start_screen_share()
            self.screen_share_btn.setText("화면 공유 중지")
        else:
            self.teacher_service.stop_screen_share()
            self.screen_share_btn.setText("화면 공유 시작")
                
    def start_screen_share(self):  # TODO 화면 공유 시작 작성
        print("화면 공유 시작")

    def stop_screen_share(self):  # TODO 화면 공유 중지 작성
        print("화면 공유 중지")
        
    def setting_btn_handler(self):
        print("setting btn clicked")
        dialog = TableSettingDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.row = int(dialog.row_text_edit.toPlainText())
            self.col = int(dialog.col_text_edit.toPlainText())
            self.save_config()
            self.clear_and_build_table()

    def clear_and_build_table(self):
        self.student_table.clear()
        self.student_table.setRowCount(self.row)
        self.student_table.setColumnCount(self.col)
        self.build_table()
        
    def table_mouse_press_handler(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.table_right_mouse_press_handler(event)
            
    def table_right_mouse_press_handler(self, event):
        '''
        테이블에서 우클릭 시 컨텍스트 메뉴를 표시한다.
        '''
        self.right_click_pos = event.pos()
        
        index = self.student_table.indexAt(self.right_click_pos)
        row = index.row()
        col = index.column()
        
        table_item = self.student_table.cellWidget(row, col)
        
        # 컨텍스트 메뉴 생성
        context_menu = QMenu(self)
        
        # 컨텍스트 메뉴 동작 생성
        disable_action = QAction("비활성화", self)
        enable_action = QAction("활성화", self)
        remote_controll_action = QAction("원격제어", self)
        
        # 동작을 수행하는 함수 연결 (여기서는 예시로 메시지 박스 출력)
        disable_action.triggered.connect(self.disable_triggered_handler(table_item))
        enable_action.triggered.connect(self.enable_triggered_handler(table_item))
        remote_controll_action.triggered.connect(self.remote_controll_triggered_handler(table_item))
        
        # 동작을 컨텍스트 메뉴에 추가
        context_menu.addAction(disable_action)
        context_menu.addAction(enable_action)
        context_menu.addAction(remote_controll_action)
        
        # 컨텍스트 메뉴 표시
        context_menu.exec_(self.mapToGlobal(event.pos()))
            
    def disable_triggered_handler(self, table_item):
        table_item.hide()
        row, col = table_item.getPos()
        self.cells[row][col] = False
                    
        self.right_click_pos = None
        
    def enable_triggered_handler(self, table_item):      
        table_item.show()
        row, col = table_item.getPos()
        self.cells[row][col] = True
                    
        self.right_click_pos = None
        
    def remote_controll_triggered_handler(self, student_ip):
        self.teacher.remote_controll(student_ip)
        
    def remote_controll(self):
        print("원격제어 실행")
        
    def save_config(self):
        setting = {
            'row': self.row,
            'col': self.col,
        }
        
        with open(CONFIG_PATH, 'w') as file:
            json.dump(setting, file)
            
    def closeEvent(self, event):
        super().closeEvent(event)
        self.teacher_service.close()
            
class TableItem(QWidget):
    def __init__(self, pos:tuple, ip="", name=""):
        super().__init__()
        uic.loadUi("./Server/ui/table_item.ui", self)
        self.pos = pos
        self.ip = ip
        self.name = name
        
        self.setText()

    def clear(self):
        self.ip = ""
        self.name = ""
        self.setText()
        
    def add_student_info(self, student:Student):
        self.ip = student.get_ip()
        self.name = student.get_name()
        
    def setText(self):
        self.ip_label.setText(self.ip)
        self.name_label.setText(self.name)
    
    def getPos(self):
        return self.pos
    
class TableSettingDialog(QDialog):
    def __init__(self, parent:QWidget=None):
        super().__init__(parent)
        uic.loadUi("./Server/ui/setConfig.ui", self)
        self.setWindowTitle("Table Setting")
        self.buttonBox.accepted.connect(super().accept)
        self.buttonBox.rejected.connect(super().reject)