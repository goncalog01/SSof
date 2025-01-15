# Challenge `Secure by Design` writeup

- Vulnerability: Endpoint is vulnerable to privilege escalation attack
- Where: `http://mustard.stt.rnl.tecnico.ulisboa.pt:22056` endpoint
- Impact: Allows non-admin users to access information that should only be available to admins
- NOTE: By looking at the cookies received in the response after trying to login with a random username, we can see there is a 'user' field with a value that is encoded in Base64. By decoding it, we see that the value corresponds to the username encoded in Base64. By sending a request with the field set to the value corresponding to the username 'admin' encoded in Base64 we get access to the information only available to admins

## Steps to reproduce

1. Set the 'user' cookies field to 'YWRtaW4=' (value corresponding to 'admin' encoded in Base64)
2. Send a GET request to the `http://mustard.stt.rnl.tecnico.ulisboa.pt:22056` endpoint

[(POC)](pocs/secure_by_design_poc.py)
