# Challenge `Calling Functions` writeup

- Vulnerability: Format Strings Vulnerability
- Where: line 16 of `07_functions.c`
- Impact: Allows reading arbitrary memory content, write to arbitrary memory content, and hijack of the execution control flow

## Steps to reproduce

1. Use the command `objdump -R bin` to know the address of `exit@GOT` (`0x804a018`)
2. Using GDB to analyze the stack immediately before the `printf` call (line 16), you can see that the beginning of `buffer` is in the 7th register of the stack immediately after the format string of the `printf`, and you can also check the address where the `win` function is written in the memory (`0x804849b`)
3. Sending `\x20\xa0\x04\x08\x18\xa0\x04\x08.%2042x.%7$hn.%31893x.%8$hn` will put the address (`0x804a020`) of the 2nd most significant byte of `exit@GOT` in the 7th register of the stack immediately after the format string of the `printf` (beginning of `buffer`) and the address (`0x804a018`) of the least significant byte in the 8th register and then write the number of bytes printed so far in those addresses (it writes 2 bytes: one in the address stored in the register and another one in the address after that), so the 2 most significant bytes of `exit@GOT` will be changed to `0x0804` (2052 bytes: 8 from the addresses + 1 from the '.' + 2042 from the first register below the format string + 1 from the '.') and the 2 least significant bytes to `0x849b` (33947 bytes: 2052 from the previous byte + 1 from the '.' + 31893 from the second register below the format string + 1 from the '.'), changing the value of `exit@GOT` to `0x804849b` (address where the `win` function is written in the memory), so when the `vuln` function calls `exit`, it will instead call `win` and print the flag

[(POC)](pocs/calling_functions_poc.py)
