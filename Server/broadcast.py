import socket
import threading
import time

# event 형식으로 변경

class Broadcaster:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.listeners = set()
        self.lock = threading.Lock()
        self.event = threading.Event()

    def add_listener(self, listener):
        with self.lock:
            self.listeners.add(listener)

    def remove_listener(self, listener):
        with self.lock:
            self.listeners.remove(listener)

    def broadcast(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.sendto(message, (self.ip, self.port))
                print('successfully send message!')
            
            except socket.error:
                print('error: ', socket.error)
                sock.close()


    def start(self, duration, message):
        self.event.clear()
        end_time = time.time() + duration

        while not self.event.is_set() and time.time() < end_time:
            self.broadcast(message)
            time.sleep(1)

        self.event.set()

class Listener(threading.Thread):
    def __init__(self, name, ip, port):
        super().__init__()
        self.name = name
        self.ip = ip
        self.port = port
        self.event = threading.Event()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((self.ip, self.port))
            sock.settimeout(1)

            while not self.event.is_set():
                try:
                    data, _ = sock.recvfrom(1024)
                    message = data.decode('utf-8')
                    print(f"{self.name} received message: {message}")
                except socket.timeout:
                    continue

    def stop(self):
        self.event.set()

# # IP 주소와 포트를 설정합니다.
# SERVER_ADDRESS = '221.147.245.107' # 전송측
# CLIENT_ADDRESS = '221.147.245.211' # 수신측
# PORT = 100
# message = 'Hello World!'

# # Broadcaster 객체를 생성합니다.
# broadcaster = Broadcaster(CLIENT_ADDRESS, PORT)

# # Listener 객체를 생성하고 Broadcaster에 추가합니다.
# listener1 = Listener("Listener 1", SERVER_ADDRESS, PORT)
# listener1.start()
# broadcaster.add_listener(listener1)

# # 브로드캐스트를 시작합니다.
# duration = 5
# broadcaster.start(duration, message)

# # 일정 시간이 지나면 통신을 종료합니다.
# time.sleep(duration)
# broadcaster.event.set()

# # 리스너를 종료합니다.
# listener1.stop()
# listener1.join()

