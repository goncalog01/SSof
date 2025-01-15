import requests
import re

link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22053"

s = requests.Session()

nums = re.findall(r'-?\d+', s.get(link + "/hello").text)
target = int(nums[0])
value = int(nums[1])

while value != target:
    value += int(re.findall(r'-?\d+', s.get(link + "/more").text)[0])

print(s.get(link + "/finish").text)