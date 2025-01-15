from pwn import *
import re

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = 22055

s = remote(SERVER, PORT, timeout=9999)

nums = re.findall(r'-?\d+', s.recv(512).decode())
target = int(nums[0])
value = int(nums[1])

while value != target:
    s.sendline(b'MORE')
    value += int(re.findall(r'-?\d+', s.recv(512).decode())[0])

s.sendline(b'FINISH')
print(s.recv(512).decode())