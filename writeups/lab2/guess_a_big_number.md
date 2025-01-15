# Challenge `Guess a BIG Number` writeup

- Vulnerability: Endpoint is vulnerable to brute-force attack
- Where: `/number/guess` endpoint
- Impact: Allows to find the server's pick by enumeration

## Steps to reproduce

1. Send a GET request to the `/number/guess` endpoint with a random number
2. If the server responds with a "Lower!" message, repeat step 1 with a lower number; if it responds with a "Higher!" message, repeat step 1 with a higher number

__Note: In the POC below, binary search is used to optimize this process, making it possible to find the server's pick in O(log n) steps__

[(POC)](pocs/guess_a_big_number_poc.py)
