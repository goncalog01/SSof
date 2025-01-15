# Challenge `Write Specific Byte` writeup

- Vulnerability: Format Strings Vulnerability
- Where: line 15 of `04_write_byte.c`
- Impact: Allows reading arbitrary memory content, write to arbitrary memory content, and hijack of the execution control flow

## Steps to reproduce

1. Using GDB to analyze the stack immediately before the `printf` call (line 15), you can see that the beginning of `buffer` is in the 7th register of the stack immediately after the format string of the `printf`, and you can also check the address where `target` is located (`0x804a044`)
2. Sending `\x47\xa0\x04\x08.%7$hhn` will put the address (`0x804a047`) of the most significant byte of `target` in the 7th register of the stack immediately after the format string of the `printf` (beginning of `buffer`) and then write the number of bytes printed so far (5 bytes: 4 from the address + 1 from the '.') in that address, changing the value of the most significant byte of `target` and printing the flag

[(POC)](pocs/write_specific_byte_poc.py)
