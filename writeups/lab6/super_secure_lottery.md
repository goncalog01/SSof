# Challenge `Super Secure Lottery` writeup

- Vulnerability: Buffer Overflow
- Where: line 18 of `lottery.c`
- Impact: Allows someone to write in areas that one should not

## Steps to reproduce

1. Using GDB you can check where `guess` and `lottery` are stored in memory and see that they are 48 bytes apart
2. Send a string to the server with the same character repeated 56 times (48 for the space between the variables plus 8 to change the value of the `lottery` variable)
3. Since the first 8 bytes of `guess` and `lottery` are the same, the `memcmp` function will return 0, printing the flag

__Note: The canaries are only checked before a function return, but since the `run_lottery` function gets stuck in an infinite loop without ever returning to `main`, the canaries are never checked and therefore the buffer overflow is not detected__

[(POC)](pocs/super_secure_lottery_poc.py)
