# Challenge `I will take care of this site` writeup

- Vulnerability: SQL Injection
- Where: `/login` endpoint
- Impact: Allows a regular user to login as the admin

## Steps to reproduce

1. Go to the login page
2. Login with username `admin'--` and any password
3. You will login as the admin and be able to access his information

__Note: If you try to login with username `'` and any password, you will be redirected to an error page where you can see the structure of the query: `SELECT id, username, password, bio, age, jackpot_val FROM user WHERE username = '<username>' AND password = '<password>'`. By logging in with username `admin'--`, it will ignore the rest of the query, since the `--` symbol represents the start of a comment in SQLite, so the performed query will be `SELECT id, username, password, bio, age, jackpot_val FROM user WHERE username = 'admin'`, allowing you to login in as the admin, since it does not check the password__

[(POC)](pocs/i_will_take_care_of_this_site_poc.py)
