import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import os
import threading

from modules.Service.StudentService import StudentService

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType(BASE_DIR + r"\Main.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.SService = StudentService()

        self.setUi()
        self.setData()

    def setUi(self):
        self.setupUi(self)

        # QSizeGrip 위젯 생성
        size_grip = QSizeGrip(self.centralwidget)

        # 상단 바 제거
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 테두리 제거
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_Max.clicked.connect(lambda: self.maximizeButton())
        self.pushButton_Min.clicked.connect(lambda: self.showMinimized())

        # 페이지 불러오기
        self.first = First()
        self.stackedWidget.addWidget(self.first)
        self.second = Second()
        self.stackedWidget.addWidget(self.second)
        self.third = Third()
        self.stackedWidget.addWidget(self.third)

        # Home 버튼 이번트
        self.first.remoteButton.clicked.connect(self.remoteBtnClick)
        self.first.scrshrButton.clicked.connect(self.scrShrBtnClick)

        # Home으로 돌아가기 버튼 이벤트
        self.second.remoteControlQuitButton.clicked.connect(self.backHome)
        self.third.screenShareQuitButton.clicked.connect(self.backHome)

    def setData(self):
        self.connect_label.setText(str(self.SService.student))

        t = threading.Thread(target=self.SService.findTeacher, args=(self.first.stateImg, ))
        t.daemon = True
        t.start()

    def remoteBtnClick(self):
        msgbox = QMessageBox(self.centralwidget)
        msgbox.setWindowTitle("원격제어 요청")
        msgbox.setText('강사에게 원격제어를 요쳥하겠습니까?')
        msgbox.addButton(QPushButton('요청'), QMessageBox.YesRole)
        msgbox.addButton(QPushButton('취소'), QMessageBox.NoRole)
        msgbox.setStyleSheet("QLabel{min-width:400 px; min-height:50 px;}");
        result = msgbox.exec_()

        if result == 0:
            self.showMinimized()
            self.showRemoteScreen()

    def backHome(self):
        self.stackedWidget.setCurrentIndex(0)

    def scrShrBtnClick(self):
        self.stackedWidget.setCurrentIndex(2)
        self.third.screenShareQuitButton.clicked.connect(self.SService.closeScreenShare)
        self.SService.screenShare(self.third.screen)

    def showRemoteScreen(self):
        self.stackedWidget.setCurrentIndex(1)
        self.second.remoteControlQuitButton.clicked.connect(self.SService.closeRemote)
        self.SService.sendRemote(self.second.screen)

    def maximizeButton(self):
        if self.pushButton_Max.isChecked():
            self.showMaximized()
        else:
            self.showNormal()

    def closeEvent(self, QCloseEvent):
        self.SService.closeRemote()

    # MOUSE Click drag EVENT function
    def mousePressEvent(self, event):
        if self.HeaderLayout.underMouse():
            if event.button() == QtCore.Qt.LeftButton:
                self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        num = 100
        if self.HeaderLayout.underMouse():
            if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
                if -num < event.pos().x() - self.offset.x() < num and -num < event.pos().y() - self.offset.y() < num:
                    self.move(self.pos() + event.pos() - self.offset)

        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

class First(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(BASE_DIR + r"\UI\home_Qwidget.ui", self)



class Second(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(BASE_DIR + r"\UI\remote_control.ui", self)


class Third(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(BASE_DIR + r"\UI\screen_share.ui", self)


if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()