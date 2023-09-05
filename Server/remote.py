import sys
import time
from PIL import Image
import socket
import zlib
import threading
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
import numpy as np
import pyautogui
from queue import Queue
import keyboard


# HOST = '127.0.0.1'				# test IP
HOST = '121.137.69.76'			#접속ip
PORT = 9900			#접속포트
screen_width = 1920			#스크린샷 가로길이
screen_height = 1080			#스크린샷 세로길이
send_queue = Queue()
img_data =  Image.open( '대기화면.png' )	#초기이미지 설정
rec_count = 0				#통신횟수

def key_name(key):			#qt 키 이벤트 이름 반환함수
	if(key == QtCore.Qt.Key_A): return("a")
	elif(key == QtCore.Qt.Key_B): return("b")
	elif(key == QtCore.Qt.Key_C): return("c")
	elif(key == QtCore.Qt.Key_D): return("d")
	elif(key == QtCore.Qt.Key_E): return("e")
	elif(key == QtCore.Qt.Key_F): return("f")
	elif(key == QtCore.Qt.Key_G): return("g")
	elif(key == QtCore.Qt.Key_H): return("h")
	elif(key == QtCore.Qt.Key_I): return("i")
	elif(key == QtCore.Qt.Key_J): return("j")
	elif(key == QtCore.Qt.Key_K): return("k")
	elif(key == QtCore.Qt.Key_L): return("l")
	elif(key == QtCore.Qt.Key_M): return("m")
	elif(key == QtCore.Qt.Key_N): return("n")
	elif(key == QtCore.Qt.Key_O): return("o")
	elif(key == QtCore.Qt.Key_P): return("p")
	elif(key == QtCore.Qt.Key_Q): return("q")
	elif(key == QtCore.Qt.Key_R): return("r")
	elif(key == QtCore.Qt.Key_S): return("s")
	elif(key == QtCore.Qt.Key_T): return("t")
	elif(key == QtCore.Qt.Key_U): return("u")
	elif(key == QtCore.Qt.Key_V): return("v")
	elif(key == QtCore.Qt.Key_W): return("w")
	elif(key == QtCore.Qt.Key_X): return("x")
	elif(key == QtCore.Qt.Key_Y): return("y")
	elif(key == QtCore.Qt.Key_Z): return("z")
	elif(key == QtCore.Qt.Key_0): return("0")
	elif(key == QtCore.Qt.Key_1): return("1")
	elif(key == QtCore.Qt.Key_2): return("2")
	elif(key == QtCore.Qt.Key_3): return("3")
	elif(key == QtCore.Qt.Key_4): return("4")
	elif(key == QtCore.Qt.Key_5): return("5")
	elif(key == QtCore.Qt.Key_6): return("6")
	elif(key == QtCore.Qt.Key_7): return("7")
	elif(key == QtCore.Qt.Key_8): return("8")
	elif(key == QtCore.Qt.Key_9): return("9")
	elif(key == QtCore.Qt.Key_Space): return("space")
	elif(key == QtCore.Qt.Key_Backspace): return("backspace")
	elif(key == QtCore.Qt.Key_Delete): return("delete")
	elif(key == QtCore.Qt.Key_Return): return("enter")
	elif(key == QtCore.Qt.Key_Shift): return("shift")
	elif(key == QtCore.Qt.Key_Control): return("ctrl")
	elif(key == QtCore.Qt.Key_Alt): return("alt")
	elif(key == QtCore.Qt.Key_Up): return("up")
	elif(key == QtCore.Qt.Key_Down): return("down")
	elif(key == QtCore.Qt.Key_Left): return("left")
	elif(key == QtCore.Qt.Key_Right): return("right")
	elif(key == QtCore.Qt.Key_Semicolon): return(";")
	elif(key == QtCore.Qt.Key_Greater): return(">")
	elif(key == QtCore.Qt.Key_Equal): return("=")
	elif(key == QtCore.Qt.Key_Plus): return("+")
	elif(key == QtCore.Qt.Key_Minus): return("-")
	elif(key == QtCore.Qt.Key_Question): return("?")
	elif(key == QtCore.Qt.Key_Tab): return("tab")


class send_type():
	def __init__(self, type, a, b, time):
		super().__init__()
		self.type = type
		self.first_data = a
		self.sec_data = b
		self.time = time

class Window(QtWidgets.QWidget):
	def __init__(self, size=1.0):
		super().__init__()
		self.size = size							#크기
		self.run_watch = 0							#실행타이머
		self.rel_cursur_xy = [0,0]					#커서 좌표
		self.rel_cusur_ratio = [0,0]				#커서 상대위치%
		self.is_left_clicked = False
		self.mouse_movetime = 0
		self.setupUi()

	def setupUi(self):
		global screen_width, screen_height
		self.centralWidget = QtWidgets.QWidget(self)
		self.label = QtWidgets.QLabel(self.centralWidget)
		self.width = int(screen_width)
		self.height = int(screen_height)
		self.setGeometry(0, 0, self.width, self.height)
		self.imagemanager_pil()

	def imagemanager_pil(self):			#이미지 변경
		self.frame = np.asarray(img_data)

		h, w, c = self.frame.shape

		self.qImg = QtGui.QImage(self.frame.data, w, h, w * c, QtGui.QImage.Format_RGB888)
		self.pixmap = QtGui.QPixmap.fromImage(self.qImg)	#pixmap 생성
		width, height = pyautogui.size()
		self.pixmap = self.pixmap.scaled(QSize(width, height), QtCore.Qt.KeepAspectRatioByExpanding)	#사이즈 변경
		self.label.setPixmap(self.pixmap)	#적용

	def mousePressEvent(self, event):
		global send_queue, screen_width, screen_height
		self.rel_cursur_xy = [event.x(), event.y()]		#커서 위치 저장
		self.rel_cusur_ratio = [(event.x()-self.label.x())/self.label.width(), (event.y()-self.label.y())/self.label.height()]	#커서 상대위치% 저장
		if (keyboard.is_pressed('ctrl')):
			if (event.button() == QtCore.Qt.LeftButton):
				self.is_left_clicked = True
		else:
			mouse_x = int((event.x()-self.label.x())/self.label.width()*screen_width)	#마우스 좌표 계산
			mouse_y = int((event.y()-self.label.y())/self.label.height()*screen_height)
			if (event.button() == QtCore.Qt.LeftButton):
				send_queue.put(send_type("mouse_left_down", mouse_x, mouse_y, self.run_watch))	#큐 추가
			elif (event.button() == QtCore.Qt.RightButton):
				send_queue.put(send_type("mouse_right_down", mouse_x, mouse_y, self.run_watch))	#큐 추가

	def mouseReleaseEvent(self, event):
		global send_queue, screen_width, screen_height
		if (keyboard.is_pressed('ctrl')):
			if (event.button() == QtCore.Qt.LeftButton):
				self.is_left_clicked = False
		else:
			mouse_x = int((event.x()-self.label.x())/self.label.width()*screen_width)	#마우스 좌표 계산
			mouse_y = int((event.y()-self.label.y())/self.label.height()*screen_height)
			if (event.button() == QtCore.Qt.LeftButton):
				send_queue.put(send_type("mouse_left_up", mouse_x, mouse_y, self.run_watch))	#큐 추가
			elif (event.button() == QtCore.Qt.RightButton):
				send_queue.put(send_type("mouse_right_up", mouse_x, mouse_y, self.run_watch))	#큐 추가

	def mouseMoveEvent(self, event):
		global send_queue, screen_width, screen_height
		if (keyboard.is_pressed('ctrl') and self.is_left_clicked):
			self.label.move(self.label.x() + (event.x() - self.rel_cursur_xy[0]), self.label.y() + (event.y() - self.rel_cursur_xy[1]))
			self.rel_cursur_xy = [event.x(), event.y()]		#커서 위치 저장
			self.rel_cusur_ratio = [(event.x()-self.label.x())/self.label.width(), (event.y()-self.label.y())/self.label.height()]	#커서 상대위치% 저장
		elif (not keyboard.is_pressed('ctrl')):
			if (self.label.x() < event.x() < self.label.x()+self.label.width() and self.label.y() < event.y() < self.label.y()+self.label.height()):
				mouse_x = int((event.x()-self.label.x())/self.label.width()*screen_width)	#마우스 좌표 계산
				mouse_y = int((event.y()-self.label.y())/self.label.height()*screen_height)
				send_queue.put(send_type("mouse_move", mouse_x, mouse_y, self.run_watch))	#큐 추가

	def wheelEvent(self, event):			#마우스휠 확대
		if (keyboard.is_pressed('ctrl')):			#컨트롤을 누를경우 크기조정
			self.rel_cursur_xy = [event.x(), event.y()]		#커서 위치 저장
			self.rel_cusur_ratio = [(event.x()-self.label.x())/self.label.width(), (event.y()-self.label.y())/self.label.height()]	#커서 상대위치% 저장
			print (self.rel_cusur_ratio)
			if (event.angleDelta().y() < 0 and not self.size-0.15 <= 0.15):			#크기변수 수정
				print(self.size)
				self.size -= 0.15
			elif (event.angleDelta().y() > 0 and not self.size+0.15 >= 5):
				self.size += 0.15
		else:
			send_queue.put(send_type("mouse_wheel", event.angleDelta().y(), 0, self.run_watch))	#큐 추가

	def keyPressEvent(self, event):
		send_queue.put(send_type("key_press", key_name(event.key()), 0, self.run_watch))	#큐 추가

	def keyReleaseEvent(self, event):
		send_queue.put(send_type("key_release", key_name(event.key()), 0, self.run_watch))

	def run(self):				#행동함수
		self.run_timer = QtCore.QTimer(self)
		self.run_timer.timeout.connect(self.__runCore)				#0.01초마다 self.__runCore 호출
		self.run_timer.start(10)

	def __runCore(self):
		self.imagemanager_pil()
		self.run_watch += 0.1
		self.run_watch = round(self.run_watch, 2)

def receiveScreen(client_socket, addr):		#데이터 받기 함수
	global img_data, rec_count, screen_width, screen_height
	while (True):
		start = time.process_time()		#시작시간 기록
		try:
			data = client_socket.recv(4)	#데이터 길이를 먼저 받음
			print(data)	
			length = int.from_bytes(data, "little")
			buf = b''
			step = length
			a=0
			while True:				#데이터가 전부 받아질 때까지 반복
				a += 1
				data = client_socket.recv(step)
				buf += data
				if len(buf) == length:
					break
				elif len(buf) < length:
					step = length - len(buf)
			data = zlib.decompress(buf)			#압축풀기
			img_data = Image.frombytes('RGB', (screen_width, screen_height), data)	#이미지 저장
			rec_count += 1
		except Exception as ex:
			print(ex)
		finally:
			end = time.process_time()		#끝 시간 기록
			print(str(length) + " : " + str(a) + " : " + str(end - start))		#소요시간 출력

def sendEvent(client_socket, addr):
	global send_queue
	length = 0
	last_time = 0
	while (True):
		start = time.process_time()		#시작시간 기록
		try:
			if (send_queue.qsize() != 0):
				send_data = send_queue.get()		#큐에서 꺼내옴
				if ((send_data.type == "mouse_move" and (last_time + 0.3 > send_data.time or send_queue.qsize() == 0))): continue	#드래그라면 0.3초마다 전송
				last_time = send_data.time
				data = str(send_data.type) + ":" + str(send_data.first_data) + ":" + str(send_data.sec_data)
				data = data.encode()
				length = len(data)
				client_socket.sendall(length.to_bytes(4, byteorder="little"))		#데이터 크기 전송
				client_socket.sendall(data)				#데이터 전송
		except Exception as ex:
			print(ex)
		finally:
			end = time.process_time()		#끝 시간 기록
			print("send -> " + str(length) + " : " + str(end - start))		#소요시간 출력
		time.sleep(0.01)

class RemoteCore(send_type, Window):
	def __init__(self, HOST):
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((HOST, PORT))			#접속
		th_send = threading.Thread(target=sendEvent, args = (client_socket, HOST))		#전송함수 쓰레드
		th_send.start()
		th_receive_screen = threading.Thread(target=receiveScreen, args = (client_socket, HOST))		#받기함수 쓰레드
		th_receive_screen.start()
		app = QApplication(sys.argv)
		window = Window()
		window.show()
		app.exec()
