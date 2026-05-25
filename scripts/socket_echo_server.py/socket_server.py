"""
Server recieves message from client and echos is back to the client.¨
Server script.
"""
import socket

HOST = input("Host IP: ")
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server is waiting for connection ...")

conn, addr = server.accept()

print(f"Connection successful from: {addr}")

while True:
    data = conn.recv(1024)

    if not data:
        break

    print("Message accepted: ", data.decode())
    conn.send(data)

conn.close()
server.close()