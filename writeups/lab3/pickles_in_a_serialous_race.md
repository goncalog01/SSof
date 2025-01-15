# Challenge `Pickles in a seri(al)ous race` writeup

- Vulnerability: Remote Code Execution
- Where: `mustard.stt.rnl.tecnico.ulisboa.pt:22653`
- Impact: Allows an attacker to execute arbitrary code remotely

## Steps to reproduce

1. Open two connections with the server, in one of them choose a classy note and in the other choose a free note
2. Wait until both connections are on the read/write choice
3. In the free note connection, use the `pickle.dumps()` method to serialize the class that contains the code to execute (in this case we use the `find` and `cat` commands to read the content of all the files in the `/home` directory) in the `__reduce__()` method and send it to the server, which will write it to a note
4. In the classy note connection, read that note, causing the server to run the `pickle.loads()` method on the content of the note, executing the code we sent, which will print the content of all the files in `/home` directory where we just need to search for the flag we are looking for

__Note: Step 2 is needed because when we switch from one mode to the other, the directory and all its files are deleted, so if we ran the free note connection first and the classy note connection after, the note would be deleted and the second connection wouldn't be able to read it. By 'synchronizing' both connections at the read/write choice, we guarantee that the note isn't deleted, since the other connection has already chosen its mode__

[(POC)](pocs/pickles_in_a_serialous_race_poc.py)
