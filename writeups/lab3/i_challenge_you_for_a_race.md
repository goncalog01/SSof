# Challenge `I challenge you for a race` writeup

- Vulnerability: Race condition
- Where: `/challenge/read_file.c` program (between lines 14 and 20)
- Impact: Allows users to read a file that they don't have access to

## Steps to reproduce

1. Create a file that you own
2. Create a symbolic link to that file
3. Run the `read_file.c` program with the link as argument
4. At the same time as step 3, create a new symbolic link with the same name as the one created in step 2, but pointing to the file that you want to read (in this case `/challenge/flag`)

__Note: These steps need to be repeated until success, since step 4 has to happen after the access to the file is checked and before the file is opened, so that when the program checks if you have access to read the file, the link is pointing to the file you own (and thus have access to), but when the program opens the file, the link is pointing to the file you want to read__

[(POC)](pocs/i_challenge_you_for_a_race_poc.sh)
