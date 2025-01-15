# Challenge `Write Given Number` writeup

- Vulnerability: Format Strings Vulnerability
- Where: line 19 of `06_write_random.c`
- Impact: Allows reading arbitrary memory content, write to arbitrary memory content, and hijack of the execution control flow

## Steps to reproduce

1. Using GDB to analyze the stack immediately before the `printf` call (line 19), you can see that the beginning of `buffer` is in the 7th register of the stack immediately after the format string of the `printf`, and you can also check the addresses where `target` (`0x804a070`) and `r` (`0x804a078`) are located
2. Sending `\x70\xa0\x04\x08\x78\xa0\x04\x08.%7$n%8$n` will put the address of `target` in the 7th register of the stack immediately after the format string of the `printf` (beginning of `buffer`) and the address of `r` in the 8th register and then write the number of bytes printed so far in both addresses (9 bytes: 8 bytes from the addresses + 1 from the '.'), changing both `target` and `r` to the same value and printing the flag

[(POC)](pocs/write_given_number_poc.py)
