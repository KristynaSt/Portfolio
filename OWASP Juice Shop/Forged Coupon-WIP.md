# OWASP Juice Shop - Forged Coupon

**OWASP Category: A08:2025 Software or Data Integrity Failures**

popisek 

## Tools:
- **Burp Suite**

## Methodology:

1. **Finding the vulnerable endpoint**
    - Through exploring the main navigator menu manually I created a new user on http://127.0.0.1:3000/#/register. Then I logged-in as the newly created user on http://127.0.0.1:3000/#/login.
    -In the users details page (http://127.0.0.1:3000/profile), users have the option of changing their username. I changed the username to "test123" and intercepted the POST request through BurpSuite Proxy.

    <img src="\assets\BrokenAccess_CSRF.png" alt="CSRF_request" width="1000px">

    - The POST request contains parameter *username="newusername"* and referer URL: http://127.0.0.1:3000/profile. The POST request does not use CSRF token nor controls the server origin and uses cookie token -> request is prone to CSRF.
2. **Creating CSRF Payload**
    - I created a HTML page with a hidden input field inside "form", thats supposed to change the username to "HackedbyKristyna". The form is automatically submitted as the page loads due to JavaScript auto-submit script.

    ```html
    <html>
    <body>
        <form action="http:/127.0.0.1:3000/profile" method="POST">
                <input type="hidden" name="username" value="HackedbyKristyna" />
        </form>
        <script>document.forms[0].submit();</script>
    </body>
    </html>
    ```
3. **Attack execution**
    -In real-attack scenario the HTML has to be uploaded to a publicly accessible domain so it can be accessed by the targetted user. The user have an active session on the targetted platfom. To solve this CTF, I opened the HTML file from terminal with xdf-open filename.html. After refreshing the users profile page, the username has been changed to "HackedbyKristyna".

    <img src="\assets\BrokenAccess_CSRF_result.png" alt="CSRF_result" width="1000px">