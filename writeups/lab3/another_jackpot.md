# Challenge `Another jackpot` writeup

- Vulnerability: Race condition
- Where: `/login` endpoint (between lines 167 and 176)
- Impact: Allows users to have admin privileges during the window of vulnerability

## Steps to reproduce

1. Send a POST request to the `/login` endpoint with the 'username' field as 'admin'
2. At the same time as step 1, send a GET request to the `/jackpot` endpoint

__Note: These steps need to be repeated until success, since step 2 has to happen after the username is set to 'admin' and before the username and password are checked__

[(POC)](pocs/another_jackpot_poc.py)
