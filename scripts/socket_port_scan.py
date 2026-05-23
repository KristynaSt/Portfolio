"""
Scans ports 1-100 on a target host.
"""

import socket

target = input("Target IP: ")

for port in range(1, 100):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    result = s.connect_ex((target, port))
    if result == 0:
        print(f"Port {port} is open")

s.close()