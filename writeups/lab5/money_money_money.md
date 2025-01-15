# Challenge `Money, money, money!` writeup

- Vulnerability: SQL Injection
- Where: `/update_profile` endpoint
- Impact: Allows an attacker to perform queries and change values in the database

## Steps to reproduce

1. Register a new user, login and go to your profile
2. In the 'Bio' box, write `', tokens = <your_jackpot_val>, bio = '` and click `Update profile`
3. Your amount of tokens will be updated and you will see the flag

__Note: If you try to update your bio to `'`, you will be redirected to an error page where you can see the structure of the query: `UPDATE user SET bio = '<updated_bio>' WHERE username = '<your_username>'`. By updating your bio to `', tokens = <your_jackpot_val>, bio = '`, the performed query will be `UPDATE user SET bio = '', tokens = <your_jackpot_val>, bio = '' WHERE username = '<your_username>'`, allowing you to update your amount of tokens__

[(POC)](pocs/money_money_money_poc.py)
