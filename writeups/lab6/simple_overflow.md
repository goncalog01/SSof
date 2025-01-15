# Challenge `Simple Overflow` writeup

- Vulnerability: Buffer Overflow
- Where: line 15 of `simple.c`
- Impact: Allows someone to write and/or to execute code in areas that one should not

## Steps to reproduce

1. Using GDB you can check where `buffer` and `test` are stored in memory and see that they are 128 bytes apart
2. Send a string to the server with 129 random characters (128 for the space between the variables plus one to change the `test` variable)
3. The `test` variable will be changed and you will get the flag

[(POC)](pocs/simple_overflow_poc.py)
