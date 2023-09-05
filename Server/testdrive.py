from remote import *
from customWidget import *

f = open('config.txt', 'r')
IP = f.readline()
print(IP)
f.close()
RemoteCore(IP)