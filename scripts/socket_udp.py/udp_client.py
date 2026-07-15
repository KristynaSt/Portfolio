"""
Client sending UDP.
"""

import socket

HOST = input("Host IP: ")
PORT = 5002

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Message for server - UDP style"

client.sendto(message.encode(), (HOST, PORT))
client.close()
