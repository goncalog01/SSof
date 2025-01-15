import requests
import re

link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22056"

s = requests.Session()

s.cookies.set('user', 'YWRtaW4=')
print(s.get(link).text)