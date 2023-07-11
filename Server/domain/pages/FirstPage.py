from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore

from ..cell import Cell
from ..student import Student
from ..dialog import TableDialog

import json
import os

CONFIG_PATH = "./setting.json"

class Page(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("./ui/command_center.ui", self)
        setting = {
            'row': 7,
            'col': 6
        }
        
        if os.path.exists(CONFIG_PATH):
            setting = self.load_setting()
        
        self.row = setting['row']
        self.col = setting['col']
        
        self.right_click_pos = None
        
        self.students = [[0 for i in range(self.col)] for j in range(self.row)] 
        self.cells = [[0 for i in range(self.col)] for j in range(self.row)] 
        self.disabled_cells = [[0 for i in range(self.col)] for j in range(self.row)] 
        
        self.setupUi()
        
    def load_setting(self):
        with open(CONFIG_PATH, 'r') as file:
            setting = json.load(file)
            return setting
        
    def setupUi(self):
        self.setting_table()
        self.get_students()
        self.check_cells_little_students()
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
        
        for i in range(30):
            self.students.append(Student(str(i), i, i))    
    
    def check_cells_little_students(self):
        return self.row * self.col < len(self.students)       

    def build_table(self):
        '''
        학생 자리 테이블을 생성한다.
        '''
        print("start table building")
        
        for i in range(self.row):
            for j in range(self.col):
                cell = Cell(str(i), str(j))
                self.student_table.setCellWidget(i, j, cell)
                
    def screen_share_btn_handler(self):
        self.build_screen_share_page()
        if self.screen_share_btn.text() == "화면 공유 시작":
            self.start_screen_share()
            self.screen_share_btn.setText("화면 공유 중지")
        else:
            self.stop_screen_share()
            self.screen_share_btn.setText("화면 공유 시작")

    def start_screen_share(self):  # TODO 화면 공유 시작 작성
        print("화면 공유 시작")

    def stop_screen_share(self):  # TODO 화면 공유 중지 작성
        print("화면 공유 중지")
        
    def setting_btn_handler(self):
        print("setting btn clicked")
        dialog = TableDialog()
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
        
        # 컨텍스트 메뉴 생성
        context_menu = QMenu(self)
        
        # 컨텍스트 메뉴 동작 생성
        disable_action = QAction("비활성화", self)
        enable_action = QAction("활성화", self)
        remote_controll_action = QAction("원격제어", self)
        
        # 동작을 수행하는 함수 연결 (여기서는 예시로 메시지 박스 출력)
        disable_action.triggered.connect(self.disable_triggered_handler)
        enable_action.triggered.connect(self.enable_triggered_handler)
        remote_controll_action.triggered.connect(self.remote_controll_triggered_handler)
        
        # 동작을 컨텍스트 메뉴에 추가
        context_menu.addAction(disable_action)
        context_menu.addAction(enable_action)
        context_menu.addAction(remote_controll_action)
        
        # 컨텍스트 메뉴 표시
        context_menu.exec_(self.mapToGlobal(event.pos()))
            
    def disable_triggered_handler(self):
        index = self.student_table.indexAt(self.right_click_pos)
        row = index.row()
        col = index.column()
        
        cell = self.student_table.cellWidget(row, col)
        
        cell.hide()
        self.cells[row][col] = False
                    
        self.right_click_pos = None
        
    def enable_triggered_handler(self):
        index = self.student_table.indexAt(self.right_click_pos)
        row = index.row()
        col = index.column()
        
        cell = self.student_table.cellWidget(row, col)
        
        cell.show()
        self.cells[row][col] = True
                    
        self.right_click_pos = None
        
    def remote_controll_triggered_handler(self):
        
        self.remote_controll()
        
    def remote_controll(self):
        print("원격제어 실행")
        
    def save_config(self):
        setting = {
            'row': self.row,
            'col': self.col,
        }
        
        with open(CONFIG_PATH, 'w') as file:
            json.dump(setting, file)