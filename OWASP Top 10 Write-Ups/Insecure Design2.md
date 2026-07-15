# Try Hack Me - OWASP Top 10 2025: Insecure Design

**OWASP Category: A06:2025 Insecure Design**

Exploring the APIs for a mobile app, I discovered a insecure design vulnerability - unauthenticated users are able to access messages belonging to other users..

## Tools:
- **GoBuster**

## Methodology:

1. **Exploring the target in a web browser**
    - The lab instructions told us to navigate to 10.113.161.232:5005. There is a website directing the user to download the app SecureChat. The button does not redirect us anywhere, its just an empty button.

    <img src="\assets\InsecureDesign_website.png" alt="website" width="1000px">

2. **Enumerating API URL paths**
    - Using GoBuster I enumerated URL paths including /api.

    ```bash
    gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.113.161.232:5005/api/
    ```

    - We found a path /api/users:

    <img src="\assets\InsecureDesign_gobuster.png" alt="gobuster" width="1000px">

    <img src="\assets\InsecureDesign_API.png" alt="api_path" width="1000px">

3. **Finding API path for messages**
    - After trying a few logical combinations of URL paths, that could lead to revealing the apps registered users messages, I discovered the path /api/messages/*json_key* (json_key is admin, user1 or user2). This path reveals the users messages.

    <img src="\assets\InsecureDesign_message.png" alt="admin_messages" width="1000px">

    <img src="\assets\InsecureDesign_messages2.png" alt="user1_messages" width="1000px">

## Remediation
Implement server-side authorization to ensure that users can access only their own messages.