# Challenge `Return Address` writeup

- Vulnerability: Buffer Overflow
- Where: line 15 of `return.c`
- Impact: Allows someone to write and/or to execute code in areas that one should not

## Steps to reproduce

1. Using GDB you can check where `buffer` and the return address of the `challenge` function are stored in memory and see that they are 22 bytes apart, and you can also check the address where the `win` function is written in the memory
2. Send a string to the server with 22 random characters (for the space between `buffer` and the return address) followed by the address where the `win` function is written in the memory in little-endian order (e.g., if the address is `0x80486f1`, you should send `0xf1860408`)
3. The return address of the `challenge` function will be changed to the address where the `win` function is written in the memory, so, instead of returning to `main`, it will call the `win` function, printing the flag

[(POC)](pocs/return_address_poc.py)
