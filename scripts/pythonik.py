import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 8888))

print("UDP server běží...")

while True:
    data, address = server.recvfrom(1024)
    print(f"Od {address}: {data.decode()}")

    server.sendto(b"Zprava prijata", address)