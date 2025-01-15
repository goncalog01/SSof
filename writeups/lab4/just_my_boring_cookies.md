# Challenge `Just my boring cookies` writeup

- Vulnerability: XSS
- Where: `http://mustard.stt.rnl.tecnico.ulisboa.pt:22251` search box
- Impact: Allows an attacker to inject malicious code in the webpage

## Steps to reproduce

1. Write the script `<script>document.write(document.cookie)</script>` in the search box and click `Search`
2. Your cookies will appear in the text below the search box

[(POC)](pocs/just_my_boring_cookies_poc.py)
