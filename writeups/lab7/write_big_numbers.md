# Challenge `Write Big Numbers` writeup

- Vulnerability: Format Strings Vulnerability
- Where: line 15 of `05_write_big.c`
- Impact: Allows reading arbitrary memory content, write to arbitrary memory content, and hijack of the execution control flow

## Steps to reproduce

1. Using GDB to analyze the stack immediately before the `printf` call (line 15), you can see that the beginning of `buffer` is in the 7th register of the stack immediately after the format string of the `printf`, and you can also check the address where `target` is located (`0x804a044`)
2. Sending `\x46\xa0\x04\x08\x44\xa0\x04\x08.%3925x.%7$hn.%2888x.%8$hn` will put the address (`0x804a046`) of the 2nd most significant byte of `target` in the 7th register of the stack immediately after the format string of the `printf` (beginning of `buffer`) and the address (`0x804a044`) of the least significant byte in the 8th register and then write the number of bytes printed so far in those addresses (it writes 2 bytes: one in the address stored in the register and another one in the address after that), so the 2 most significant bytes of `target` will be changed to `0x0f5f` (3935 bytes: 8 from the addresses + 1 from the '.' + 3925 from the first register below the format string + 1 from the '.') and the 2 least significant bytes to `0x1aa9` (6825 bytes: 3935 from the previous byte + 1 from the '.' + 2888 from the second register below the format string + 1 from the '.'), changing the value of `target` to `0x0f5f1aa9` and printing the flag

[(POC)](pocs/write_big_numbers_poc.py)
