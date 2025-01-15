# Challenge `Calling Functions` writeup

- Vulnerability: Buffer Overflow
- Where: line 21 of `functions.c`
- Impact: Allows someone to write and/or to execute code in areas that one should not

## Steps to reproduce

1. Using GDB you can check where `buffer` and `fp` are stored in memory and see that they are 32 bytes apart, and you can also check the address where the `win` function is written in the memory
2. Send a string to the server with 32 random characters (for the space between the variables) followed by the address where the `win` function is written in the memory in little-endian order (e.g., if the address is `0x80486f1`, you should send `0xf1860408`)
3. The `fp` variable will be changed to the address where the `win` function is written in the memory, calling the function and printing the flag

[(POC)](pocs/calling_functions_poc.py)
