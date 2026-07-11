import socket

url = "example.com"
port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((url, port))

request = b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
client.sendall(request)

response = b""
while True:
    data = client.recv(4096)
    if not data:
        break
    response += data

client.close()

print(response.decode(errors="ignore"))