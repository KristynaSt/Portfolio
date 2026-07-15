# Try Hack Me - Injectics

**OWASP Category: A05:2025 - Injection**

The websites log-in form was vulnerable to SQL injection - we were able to log-in as authenticated user. The dashboard edit field was also prone to SQL injection, so I was able to delete a table from the database. Subsequently, I escalateed privileges by successfully authenticating to the website with admin credentials discovered in a public-facing web directory.

## Tools:
- **Nmap**
- **BurpSuite**

## Methodology:

1. **Enumerating target with Nmap**
    - Nmap scan:
    
    ```bash
    nmap -A 10.113.162.73
    ```

     <img src="\assets\Injectics_nmap.png" alt="nmap_reuslts" width="1000px">

    - The ports 80 and 22 are open.

2. **Exploring the website on port 80**
    - The target is running a website on port 80. It contains a leaderboard table - showing results of Injectics 2024.

     <img src="\assets\Injectics_website.png" alt="website" width="1000px">

    - In the top menu only 2 buttons are working - Home (directing us to the homepage) and Login (showing us login options as a normal user or as a admin).

    <img src="\assets\Injectics_login.png" alt="login" width="1000px">

3. **Reviewing the source-code**
    - After checking the source code of the homepage, we discover a comment indicating a file mail.log exists. Also revealing admins e-mail.

    <img src="\assets\Injectics_comment.png" alt="comment" width="1000px">

    - I visited the URL http://targetIP/mail.log. The content informs us that if the "users" table gets deleted, there are default credentials we can still use to authenticate.

    <img src="\assets\Injectics_maillog.png" alt="mail.log" width="1000px">

4. **Trying SQL Injection**
    - I tried to put an apostrophe in the username box of the login form and got the error message: "Invalid keywords detected".

    <img src="\assets\Injectics_sqltry.png" alt="sql_injection_try" width="1000px">

    - Looking at the log-in page source code I discovered the script.js file that confirms, that these characters are filtered in the log-in form: OR, AND, UNION, SELECT, ", '.
    
    <img src="\assets\Injectics_scriptjs.png" alt="script.js" width="1000px">

    - I intercepted the log-in request in BurpSuite, URL encoded the apostrophe and replaced OR with || - the authentication was successful.

    <img src="\assets\Injectics_request.png" alt="request" width="1000px">

    <img src="\assets\Injectics_response.png" alt="sresponse" width="1000px">

    - After successful log-in, we see a dashboard we can edit.

    <img src="\assets\Injectics_log.png" alt="log-in" width="1000px">

5. **Deleting the table "users"**
    - To escalate privileges, we want to log in with the credentials that work after the table "users" is deleted. After intercepting a request to edit the dashboard, I deleted the table using SQL injection.

    <img src="\assets\Injectics_delete.png" alt="delete_table" width="1000px">

    <img src="\assets\Injectics_deleted.png" alt="deleted_table" width="1000px">

6. **Logging-in as admin**
    - After deleting the table "users", I could successfully sign-in with the admin credentials present in mail.log file.

## Remediation
Replace dynamically constructed SQL queries with parameterized queries. Remove files containing sensitive information from publicly accessible web directories.