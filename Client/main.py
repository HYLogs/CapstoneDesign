import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import os
import threading

from modules.Service.StudentService import StudentService
from modules.CustomControls.Controls import MySizeGrip

def resource_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return base_path

BASE_DIR = resource_path()

path = os.path.join(BASE_DIR, "Main.ui")

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType(path)[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()

        self.offset = None
        self.SService = StudentService()

        self.setUi()
        self.setData()

    # Main
    def setUi(self):
        self.setupUi(self)

        # 테두리 설정
        self.setBorder()

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

        t = threading.Thread(target=self.SService.findTeacher, args=(BASE_DIR, self.first.stateImg, ))
        t.daemon = True
        t.start()

    # common
    def setBorder(self):
        # QSizeGrip 위젯 생성
        MySizeGrip(self.centralwidget, self.SService.pauseScreenShare, self.SService.resumeScreenShare)

        # 테두리 제거
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 테두리 제거
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_Max.clicked.connect(lambda: self.maximizeButton())
        self.pushButton_Min.clicked.connect(lambda: self.showMinimized())

    def backHome(self):
        self.stackedWidget.setCurrentIndex(0)

    # ScreenShare
    def scrShrBtnClick(self):
        self.stackedWidget.setCurrentIndex(2)
        self.third.screenShareQuitButton.clicked.connect(lambda: self.SService.closeScreenShare(self.third.screen))
        self.SService.screenShare(self.third.screen)

    # Remote
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

    def showRemoteScreen(self):
        self.stackedWidget.setCurrentIndex(1)
        self.second.remoteControlQuitButton.clicked.connect(self.SService.closeRemote)
        self.SService.sendRemote(self.second.screen)

    def closeEvent(self, QCloseEvent):
        self.SService.closeRemote()

    # Top bar
    def maximizeButton(self):
        if self.pushButton_Max.isChecked():
            self.showMaximized()
        else:
            self.showNormal()

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


# Pages
class First(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(BASE_DIR, "UI/home_Qwidget.ui"), self)


class Second(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(BASE_DIR, "UI/remote_control.ui"), self)


class Third(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(BASE_DIR, "UI/screen_share.ui"), self)


if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()