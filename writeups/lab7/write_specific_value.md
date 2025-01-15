# Challenge `Write Specific Value` writeup

- Vulnerability: Format Strings Vulnerability
- Where: line 13 of `03_match.c`
- Impact: Allows reading arbitrary memory content, write to arbitrary memory content, and hijack of the execution control flow

## Steps to reproduce

1. Using GDB to analyze the stack immediately before the `printf` call (line 13), you can see that the beginning of `buffer` is in the 7th register of the stack immediately after the format string of the `printf`, and you can also check the address where `target` is located (`0x804a040`)
2. Sending `\x40\xa0\x04\x08.%62x.%7$n` will put the address of `target` in the 7th register of the stack immediately after the format string of the `printf` (beginning of `buffer`) and then write the number of bytes printed so far (68 bytes: 4 from the address + 1 from the '.' + 62 from the first register below the format string + 1 from the '.') in that address, changing the value of `target` to 68 and printing the flag

[(POC)](pocs/write_specific_value_poc.py)
