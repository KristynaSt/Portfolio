"""
Scans ports 1-100 on a target host using threading.
"""

import socket
import threading

target_host = input("Target host: ")

def scan(port):
    s = socket.socket()
    s.settimeout(0.5)
    if s.connect_ex((target_host, port)) == 0:
        print(f"Open: {port}")

for port in range(1, 100):
    t = threading.Thread(target=scan, args=(port,))
    t.start()