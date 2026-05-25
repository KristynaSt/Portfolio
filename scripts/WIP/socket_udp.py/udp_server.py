"""
Server recieving UDP.
"""

import socket

HOST = input("Host IP: ")
PORT = 5002

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print("UDP server is running...")

server.settimeout(10)

try:
    data, addr = server.recvfrom(1024)
    print(f"From: {addr}: {data.decode()}")
except socket.timeout:
    print("No data received, shutting down")
    break

server.close()