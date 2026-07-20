# Hack The Box - Lame

**OWASP Category: A07:2025 – Vulnerable and Outdated Components** 

The target was running an outdated version of Samba with a known vulnerability CVE-2007-2447. Using Metasploit, we were able to exploit this vulnerability and gain root shell on the target.

## Tools:
- **Nmap**
- **Metasploit**

## Methodology:

1. **Enumerating open ports with Nmap**
    - We found an open SMB port 445 with an outdated version of Samba (3.0.20) running.

     <img src="\assets\Lame_nmap.png" alt="nmap" width="1000px">

2. **Exploiting Samba with Metasploit**
    - We will exploit the vulnerability CVE-2007-2447 with the Matasploit exploit "exploit/multi/samba/usermap_script".

    ```bash
    use exploit/multi/samba/usermap_script
     ```
    We only need to set the RHOST - target machine IP and LHOST - attacker machine IP.

3. **Successfully gaining shell**
    - We successfully gained a shell as root. Now we just browse through the directories to find flags.

     <img src="\assets\Lame_shell.png" alt="gained_shell" width="1000px">

# Remediation
Upgrade Samba to the lastest supported version adn establish a regular patch management. Restrict SMB access using firewall rules or network segmentation.