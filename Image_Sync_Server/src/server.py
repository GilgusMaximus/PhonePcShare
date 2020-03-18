import socket as socket
import os
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind(('localhost', 2222))

serversocket.listen(5)

file = open("D:/a.txt", mode='rb')
filesize = os.path.getsize("D:/config.jar")

BUFF_SIZE = 1024

while True:
    (clientsocket, address) = serversocket.accept()
    with clientsocket:
        print("Connected by ", address)
        print('Connected by', clientsocket)
        counter = 0
        data = file.read(BUFF_SIZE)
        while data:
            print(counter)
            counter += 1
            clientsocket.sendall(data)
            data = file.read(BUFF_SIZE)
        clientsocket.close()