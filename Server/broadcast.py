from socket import *
import time
import threading

class BroadcastServer:
    students = dict()
    
    def __init__(self, service, ip, port):
        self.service = service
        self.ip = ip
        self.port = port
        self.broadcastAddr = self.setBoroadcastAddr()
        
    def setBoroadcastAddr(self):
        host = self.ip.split(".")
        host[3] = "255"
        host = ".".join(host)
        return host
        
    def start(self):  
        t = threading.Thread(target=self.sendIP)
        t.daemon = True
        t.start()
        
        t = threading.Thread(target=self.recvIP)
        t.daemon = True
        t.start()
        
    def stop(self):
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        
        sock.sendto("end".encode('utf-8'), (self.broadcastAddr, self.port))
    
    def sendIP(self):
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        while True:
            BroadcastServer.students = dict()
            sock.sendto(self.ip.encode('utf-8'), (self.broadcastAddr, self.port))
            time.sleep(2)
            self.service.update()
            time.sleep(5)
            
    def recvIP(self):
        host = "0.0.0.0"
        
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind((host, self.port))
        while True:
            data, address = sock.recvfrom(1024)
            if (address[0] == self.ip): continue
            
            # TODO DHCP? 일정시간동안 아무 통신이 없으면 연결 끊겼다고 판단
            BroadcastServer.students[data.decode('utf-8')] = address[0]
            print(BroadcastServer.students)

class BroadcastClient:
    serverIP = ""
    
    def __init__(self, port):
        self.host = "0.0.0.0"
        self.port = port

    def start(self):
        t = threading.Thread(target=self.recvReturnInfo)
        t.start()
    
    def recvReturnInfo(self):
        sock = socket(AF_INET, SOCK_DGRAM)
        name = gethostname()
        sock.bind((self.host, self.port))

        while True:
            data, address = sock.recvfrom(1024)
            BroadcastClient.serverIP = data.decode('utf-8')

            sock.sendto(name.encode('utf-8'), (BroadcastClient.serverIP, self.port))
            print(name)
            
            
# How to using

# Server
# bServer = BroadcastServer("172.30.1.56", 2000) # serverPC IP, PORT
# bServer.start()
# BroadcastServer.students # get connected Client PCs Ip

# Client
# bClient = BroadcastClient(2000) # serverPC PORT
# bClient.start() 