# Challenge `Python requests` writeup

- Vulnerability: Endpoint is vulnerable to brute-force attack
- Where: `/more` endpoint
- Impact: Allows multiple chances to reach the `target` value

## Steps to reproduce

1. Send a GET request to the `/hello` endpoint to get the `target` number
2. Send GET requests to the `/more` endpoint to get more numbers until the sum of all numbers received adds up to `target`
3. Once the `target` value is reached, send a GET request to the `/finish` endpoint

[(POC)](pocs/python_requests_poc.py)
