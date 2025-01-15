# Challenge `Super Secure System` writeup

- Vulnerability: Buffer Overflow
- Where: line 10 of `check.c`
- Impact: Allows someone to write and/or to execute code in areas that one should not

## Steps to reproduce

1. Using GDB you can check where `buffer` and the return address of the `check_password` function are stored in memory and see that they are 44 bytes apart, and you can also check the address of the instruction that prints the flag (line 26 of `check.c`)
2. Send a string to the server with 36 random characters (for the space between `buffer` and `ebx`), followed by the value of `ebx` in little-endian order (e.g., if the value is `0x804a000`, you should send `0x00a00408`), followed by 4 random characters (for the space between `ebx` and the return address), followed by the address of the instruction that prints the flag in little-endian order (e.g., if the address is `0x80487d9`, you should send `0xd9870408`)
3. The return address of the `check_password` function will be changed to the address of the instruction that prints the flag, so, instead of returning to line 25 of `check.c`, it will go to line 26, printing the flag

__Note: In this case, the last byte of ebx's value is `0x00`, that corresponds to `\0`, which would represent the end of the string, messing with the input sent, so instead it is replaced by `0x01` in the POC__

[(POC)](pocs/super_secure_system_poc.py)
