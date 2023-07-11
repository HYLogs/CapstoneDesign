import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os

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

        self.first = First()
        self.stackedWidget.addWidget(self.first)
        self.second = Second()
        self.stackedWidget.addWidget(self.second)
        self.third = Third()
        self.stackedWidget.addWidget(self.third)

        self.first.remoteButton.clicked.connect(self.remoteBtnClick)
        self.first.scrshrButton.clicked.connect(self.scrshrBtnClick)

        self.second.remoteControlQuitButton.clicked.connect(self.backHome)
        self.third.screenShareQuitButton.clicked.connect(self.backHome)

    def setData(self):
        self.connect_label.setText(str(self.SService.student))


    def remoteBtnClick(self):
        msgbox = QMessageBox(self.centralwidget)
        msgbox.setWindowTitle("원격제어 요청")
        msgbox.setText('강사에게 원격제어를 요쳥하겠습니까?')
        msgbox.addButton(QPushButton('요청'), QMessageBox.YesRole)
        msgbox.addButton(QPushButton('취소'), QMessageBox.NoRole)
        msgbox.setStyleSheet("QLabel{min-width:400 px; min-height:50 px;}");
        result = msgbox.exec_()

        if result == 0:
            self.showRemoteScreen()

    def backHome(self):
        self.stackedWidget.setCurrentIndex(0)

    def scrshrBtnClick(self):
        self.stackedWidget.setCurrentIndex(2)

    def showRemoteScreen(self):
        self.stackedWidget.setCurrentIndex(1)
        self.second.remoteControlQuitButton.clicked.connect(self.SService.closeRemote)
        remoteScreen = self.second.screen
        self.SService.sendRemote(remoteScreen)

    def closeEvent(self, QCloseEvent):
        self.SService.closeEvent()


class First(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(BASE_DIR + r"\uis\home_Qwidget.ui", self)


class Second(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(BASE_DIR + r"\uis\remote_control.ui", self)


class Third(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(BASE_DIR + r"\uis\screen_share.ui", self)


if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()