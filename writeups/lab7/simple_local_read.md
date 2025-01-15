# Challenge `Simple Local Read` writeup

- Vulnerability: Format Strings Vulnerability
- Where: line 11 of `00_local_read.c`
- Impact: Allows reading arbitrary memory content, write to arbitrary memory content, and hijack of the execution control flow

## Steps to reproduce

1. Using GDB to analyze the stack immediately before the `printf` call (line 11), you can see that the address where `secret_value` is located is in the 7th register of the stack immediately after the format string of the `printf`
2. Sending `%08x.%08x.%08x.%08x.%08x.%08x.%s` will print the content of the 6 registers immediately after the format string of the `printf` and read (`%s`) the value pointed by the address stored in the 7th register (address of `secret_value`), printing the flag

[(POC)](pocs/simple_local_read_poc.py)
