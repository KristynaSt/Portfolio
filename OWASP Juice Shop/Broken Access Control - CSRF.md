# OWASP Juice Shop - CSRF

**OWASP Category:** A01:2025 Broken Access Control\

Through finding and utilizing a CSRF vulnerability I was able to change username of a user registered on the OWASP Juice Shop.

## Tools:

## Methodology:

1. **Finding the vulnerable endpoint**
    - Through exploring the main navigator menu manually I created a new user on http://127.0.0.1:3000/#/register. Then I logged-in as the newly created user on http://127.0.0.1:3000/#/login.
    -In the users details page (http://127.0.0.1:3000/profile), users have the option of changing their username. I changed the username to "test123" and intercepted the POST request through BurpSuite Proxy.

    <img src="C:\Users\tyna4\OneDrive\Pictures\Screenshots\Screenshot 2026-05-25 104732.png" alt="CSRF_request" width="500px">