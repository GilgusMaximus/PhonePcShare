import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 2222        # The port used by the server

file = open("../test.txt", "rb")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #data = s.recv(1024)

    #startbytes
    s.send(b'\x00\x03\x02')
    s.send(b"test.txt")

    data = file.read(1024)
    while data:
        s.sendall(data)
        data = file.read(1024)
    print("Sending done")
    # while data:
    #     print("i")
    #     file.write(data)
    #     data = s.recv(1024)
    # file.close()

#print('Received', repr(data))