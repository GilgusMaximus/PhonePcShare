import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 2222        # The port used by the server

file = open("E:/a.txt", "wb")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)

    while data:
        print("i")
        file.write(data)
        data = s.recv(1024)
    file.close()

print('Received', repr(data))