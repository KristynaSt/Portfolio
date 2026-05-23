"""
Runs nmap scan in "Fast mode" in the terminal.
"""

import subprocess

target_host = input("Target host: ")
result = subprocess.run(["nmap", "-F", target_host], capture_output=True, text=True)

print(result.stdout)
