import cv2
from PIL import Image
from PyQt5.QtGui import QPixmap, QImage
import pyautogui
import io
import time
import zlib
import socket, threading

scroll = 0.2
	
class RemoteCore:
	def __init__(self):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)			#서버 생성
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind(('', 9900))
		server_socket.listen()

		try:
			while True:
				client_socket, addr = server_socket.accept()			#연결 기다리기
				th_send = threading.Thread(target=self.send, args = (client_socket,addr))
				th_receive = threading.Thread(target=self.receive, args = (client_socket,addr))
				th_send.start()			#send함수 실행
				th_receive.start()			#receive함수 실행
		except:
			server_socket.close()

	def send(self, client_socket, addr):		#전송함수
		print('connect: ', addr)
		try:
			while(True):
				image = pyautogui.screenshot()			#스크린샷 촬영
				image = image.resize((int(image.size[0]), int(image.size[1])))	#크기조정
				data = image.tobytes()				#바이트화
				data = zlib.compress(data)			#압축
				length = len(data)
				client_socket.sendall(length.to_bytes(4, byteorder="little"))		#데이터 크기 전송
				client_socket.sendall(data)				#데이터 전송
				time.sleep(0.005)		#딜레이
		except Exception as e:
			pass

	def receive(self, client_socket, addr):		#데이터 받기 함수
		length = 0
		a = 0
		while (True):
			start = time.process_time()		#시작시간 기록
			try:
				data = client_socket.recv(4)	#데이터 길이를 먼저 받음
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
				data = buf.decode('utf-8').split(":")
				if (data[0] == "mouse_move"): self.mouse_control(data[1], data[2], "move")
				elif (data[0] == "mouse_left_down"): self.mouse_control(data[1], data[2], "down", "left")
				elif (data[0] == "mouse_left_up"): self.mouse_control(data[1], data[2], "up", "left")
				elif (data[0] == "mouse_right_down"): self.mouse_control(data[1], data[2], "down", "right")
				elif (data[0] == "mouse_right_up"): self.mouse_control(data[1], data[2], "up", "right")
				elif (data[0] == "mouse_wheel"): self.mouse_control(data[1], data[2], "wheel")
				elif (data[0] == "key_press"): self.keyboard_control(data[1], data[2], "press")
				elif (data[0] == "key_release"): self.keyboard_control(data[1], data[2], "release")

			except Exception as ex:
				print(ex)

			finally:
				end = time.process_time()		#끝 시간 기록
				# print("receive -> " + str(length) + " : " + str(a) + " : " + str(end - start))		#소요시간 출력

	def mouse_control(self, first, second, control_type, button="none"):		#마우스 제어함수
		global scroll
		tx = int(first)
		ty = int(second)

		if (control_type == "move"): pyautogui.moveTo(int(tx), int(ty))
		elif (control_type == "down"): pyautogui.mouseDown(int(tx), int(ty), button)
		elif (control_type == "up"): pyautogui.mouseUp(int(tx), int(ty), button)
		elif (control_type == "wheel"): pyautogui.scroll(int(tx*scroll))

	def keyboard_control(self, first, second, control_type):				#키보드 제어함수
		btn1 = str(first)
		btn2 = str(second)

		if (control_type == "press"): pyautogui.keyDown(btn1)
		elif (control_type == "release"): pyautogui.keyUp(btn1)

# Remote Class
class Remote(RemoteCore):
	ESC_KEY = 27
	FRAME_RATE = 60
	SLEEP_TIME = 1 / FRAME_RATE
	
	def __init__(self):
		self.stopsig = 0
	
	def startRemote(self, remoteScreen):
		t = threading.Thread(target=self.threadedStart, args=(remoteScreen,))
		t.daemon = True
		t.start()

	def threadedStart(self, remoteScreen):
		remoteScreen.setScaledContents(True)
		while self.stopsig == 0:
			RemoteCore.__init__(self)
			remoteScreen.setText("원격 제어 중")
			cv2.waitKey(1)
	
	def closeEvent(self):
		self.stopsig = 1
		