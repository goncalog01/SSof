# Challenge `Python requests Again` writeup

- Vulnerability: Endpoint is vulnerable to brute-force attack
- Where: `/more` endpoint
- Impact: Allows multiple chances to reach the `target` value
- NOTE: By looking at the cookies received in the first response, we can see there is a 'remaning_tries' field with the value of 1 that is decreased after the first request to `/more` in order to allow only one chance. By changing this field to 1 before each request, we are allowed mutiple chances

## Steps to reproduce

1. Send a GET request to the `/hello` endpoint to get the `target` number
2. Set the 'remaining_tries' cookies field to 1 and send GET requests to the `/more` endpoint to get more numbers until the sum of all numbers received adds up to `target`
3. Once the `target` value is reached, send a GET request to the `/finish` endpoint

[(POC)](pocs/python_requests_again_poc.py)
