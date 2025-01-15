# Challenge `Match an Exact Value` writeup

- Vulnerability: Buffer Overflow
- Where: line 16 of `match.c`
- Impact: Allows someone to write and/or to execute code in areas that one should not

## Steps to reproduce

1. Using GDB you can check where `buffer` and `test` are stored in memory and see that they are 64 bytes apart
2. Send a string to the server with 64 random characters (for the space between the variables) followed by `dcba`
3. The `test` variable will be changed to `0x61626364` and you will get the flag

__Note: `0x61626364` corresponds to the string `abcd`, but the value is stored in little-endian order, hence why we have to send `dcba` (`0x64636261`) instead__

[(POC)](pocs/match_an_exact_value_poc.py)
