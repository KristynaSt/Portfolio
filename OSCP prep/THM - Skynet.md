# Try Hack Me - Skynet

**OWASP Category:** 

popis

## Tools:
- **Burp Suite**
- **Nmap**
- **SMBclient**
- **GoBuster**

## Methodology:

1. **Enumerating open ports with Nmap**
    - Interesting open ports: 80, 445.

    ```bash
    nmap -A -Pn 10.114.168.251
    ```

2. **Enumerating directories for port 80**
    - The target is running on port 80 - I enumerated the directories using GoBuster.

    ```bash
    gobuster dir -u http://10.114.168.251 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
     ```

     We found a few directories that are being redirected (code 301).

    <img src="\assets\Skynet_gobuster.png" alt="gobuster" width="1000px">

    I explored the redirects with command:

     ```bash
    curl -I targetIP/directory
     ```

    Only accessible directory after redirect was **/squirrelmail/**.

    <img src="\assets\Skynet_mail.png" alt="gobuster" width="1000px">

3. **Exploring SMB**
    - I tired to connect to SMB with anonymous access and I was successful.

     <img src="\assets\Skynet_SMB.png" alt="smbt" width="1000px">

    - The share "anonymous" is accessible via anonymous access. Inside was a text file with potential passwords list - logs1.txt.

     ```bash
    smbclient //10.114.168.251/anonymous
    get log1.txt
    ```

    - There was also a share called "milesdyson" -> potential username.

4. **Brute-forcing squirrelmail**
    - With the list of potential passwords log1.txt and a potential username milesdyson, I tried to brute-force the Squirrelmail log-in page via BurpSuite Intruder.

    <img src="\assets\Skynet_intruder.png" alt="intruder" width="1000px">

    - The password "cyborg007haloterminator" gave us a status code 302 (resource has been temporarily moved to a different location), all the other passwords code 200. It is because after successful authentication, we are redirected to /webmail.php.

5. **Browsing through e-mails**
    - After successfully authenticating to the mailclient as user milesdyson, we found an e-mail "Samba password reset". Inside was a text including a password:

    We have changed your smb password after system malfunction.
    Password: )s{A&2Z=F^n_E.B`

6. **Connecting to SMB with credentials**
    - I tried the new password for user milesdyson to access the SMB share /milesdyson. The authentication was successful.

     <img src="\assets\Skynet_milessmb.png" alt="milessmb" width="1000px">

    - I found file /milesdyson/notes/important.txt that included the following text:

        1. Add features to beta CMS /45kra24zxs28v3yd
        2. Work on T-800 Model 101 blueprints
        3. Spend more time with my wife

    - Navigating to http://10.114.168.251/45kra24zxs28v3yd/, I found the following page:

     <img src="\assets\Skynet_page.png" alt="homepage" width="1000px">

7. **Another directory enumeration**
    - Again doing directory enumeration with the newly discovered path.

    - We found path /45kra24zxs28v3yd/administrator/, which is Cuppa CMS administrative interface.

     ```bash
    gobuster dir -u http://10.114.168.251/45kra24zxs28v3yd/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt 
     ```
     
     <img src="\assets\Skynet_admin.png" alt="homepage" width="1000px">

8. **Exploiting Cuppa CMS**
    - I found this exploit on the Exploit Database: https://www.exploit-db.com/exploits/25971 . It is a remote file inclusion exploit. The CMS code includes this part: 

    ```php
    <?php include($_REQUEST["urlConfig"]); ?>
    ```

    - We are going to try to make the urlConfig be a php file that creates a reverse shell. Utilizing a php reverse shell script located here: /usr/share/wordlists/SecLists/Web-Shells/laudanum-0.8/php/php-reverse-shell.php.
    - In the script I just changed the IP to my attacker machine IP and the port to 1234.

    <img src="\assets\Skynet_php_shell.png" alt="homepage" width="1000px">


## Remediation
