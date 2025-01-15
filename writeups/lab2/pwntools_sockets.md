# Challenge `PwnTools Sockets` writeup

- Vulnerability: Connection is vulnerable to brute-force attack
- Where: `mustard.stt.rnl.tecnico.ulisboa.pt:22055`
- Impact: Allows multiple chances to reach the `target` value

## Steps to reproduce

1. Connect to the server and get the `target` number
2. Send 'MORE' messages to the server to get more numbers until the sum of all numbers received adds up to `target`
3. Once the `target` value is reached, send a 'FINISH' message to the server

[(POC)](pocs/pwntools_sockets_poc.py)
