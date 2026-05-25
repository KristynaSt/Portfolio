"""
Server recieves message from client and echos is back to the client.¨
Client script.
"""
import socket

HOST = input("Host IP: ")
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    message = input("Type your message here: ")

    if message == "end":
        break
    client.send(message.encode())
    data = client.recv(1024)
    print("Servers answer: ", data.decode())

client.close()