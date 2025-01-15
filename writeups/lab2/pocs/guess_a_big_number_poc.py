import requests

def binary_search(l, r):
    mid = l + (r - l) // 2

    response = s.get(link + "/number/" + str(mid))

    if ("SSof" in response.text):
        return response.text
    elif ("Lower" in response.text):
        return binary_search(l, mid - 1)
    elif ("Higher" in response.text):
        return binary_search(mid + 1, r)

link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22052"

s = requests.Session()

s.get(link)

print(binary_search(0, 100000))