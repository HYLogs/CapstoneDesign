import typing
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget

from domain import *
from service import *
from page import *

import json
import os

CONFIG_PATH = "setting.json"

class SupervisionPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi("ui/command_center.ui", self)
        
        self.disable_list = []
        
        if os.path.exists(CONFIG_PATH):
            setting = self.load_setting()
            row, col = setting['row'], setting['col']
            self.disable_list = setting['disable_list']
        else:
            row, col = self.get_table_setting_input()
        
        self.main = parent
        self.teacher_service = self.main.teacher_service
        
        self.row = row
        self.col = col
        
        self.right_click_pos = None
        
        self.students = []
        
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
        
        for i in range(38):
            self.students.append(Student("192.168.10." + str(i + 1), "port", "312_" + "{:02d}".format(i + 1)))

    def build_table(self):
        '''
        학생 자리 테이블을 생성한다.
        '''
        print("start table building")
        index = 0
        
        for i in range(self.row):
            for j in range(self.col):
                item = TableItem([i, j])
                
                if [i, j] not in self.disable_list:
                    if index < len(self.students):
                        student = self.students[index]
                        item.add_student_info(student)
                        index += 1
                else:
                    item.setDisabled(True)
                
                self.student_table.setCellWidget(i, j, item)
                
        if index < len(self.students):
            # TODO 테이블 크기 에러 출력
            reply = QMessageBox.information(self, "경고", "학생PC의 수가 자리에 비해 더 많습니다. 배치를 변경하시겠습니까? \
                \n변경하지 않는다면 생략되는 학생PC가 존재할 수 있습니다!", \
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            
            if reply == QMessageBox.Yes:
                self.setting_btn_handler()
                
    def screen_share_btn_handler(self):
        if self.screen_share_btn.text() == "화면 공유 시작":
            self.teacher_service.start_screen_share()
            self.screen_share_btn.setText("화면 공유 중지")
        else:
            self.teacher_service.stop_screen_share()
            self.screen_share_btn.setText("화면 공유 시작")
        
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
        table_item = self.get_event_target()
        if table_item.disable:
            return
        table_item.setDisabled(True)
        table_item.clear()
        self.disable_list.append(table_item.get_pos())
                    
        self.right_click_pos = None
        self.clear_and_build_table()
        
    def enable_triggered_handler(self):      
        table_item = self.get_event_target()
        if not table_item.disable:
            return
        table_item.setDisabled(False)
        self.disable_list.remove(table_item.get_pos())
                    
        self.right_click_pos = None
        self.clear_and_build_table()
        
    def remote_controll_triggered_handler(self):
        table_item = self.get_event_target()
        self.main.teacher_service.remote_controll(table_item.ip)
        
        self.main.next_page()
        
    def get_event_target(self):
        index = self.student_table.indexAt(self.right_click_pos)
        row = index.row()
        col = index.column()
        table_item = self.student_table.cellWidget(row, col)
        return table_item
        
    def remote_controll(self):
        print("원격제어 실행")
        
    def save_config(self):      
        setting = {
            'row': self.row,
            'col': self.col,
            'disable_list': self.disable_list
        }
        
        with open(CONFIG_PATH, 'w') as file:
            json.dump(setting, file)
            
    def closeEvent(self, event):
        super().closeEvent(event)
        self.teacher_service.close()
        self.save_config()
            
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
    
class TableSettingDialog(QDialog):
    def __init__(self, parent:QWidget=None):
        super().__init__(parent)
        uic.loadUi("ui/setConfig.ui", self)
        self.setWindowTitle("Table Setting")
        self.buttonBox.accepted.connect(super().accept)
        self.buttonBox.rejected.connect(super().reject)
        
class RemoteControllPage(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        uic.loadUi("ui/remote_controll.ui", self)
        self.main = parent
        
        self.endRemoteControllBtn.clicked.connect(self.end_btn_handler)
                
    def end_btn_handler(self):
        # TODO 통신 종료
        self.main.teacher_service.stop_remote_controll()
        
        self.main.prev_page()
        
    def close(self):
        pass