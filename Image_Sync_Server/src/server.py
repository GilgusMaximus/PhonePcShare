import socket as socket
import os
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind(('localhost', 2222))

serversocket.listen(5)



file = open("D:/a.txt", mode='rb')

counter = 0

BUFF_SIZE = 1024

while True:
    (clientsocket, address) = serversocket.accept()
    with clientsocket:
        index_file = open("../files/fileindex.txt", mode="a")
        # [are you pc or phone, send to phone/pc, how many images sent]
        client_auth = clientsocket.recv(3)
        print("Client auth: ", client_auth[0])
        print("Client auth: ", client_auth[1])
        print("Client auth: ", client_auth[2])

        # client will then send all of the file names (max length 20 with file type) so that the server can create these intermediate
        # filenames = clientsocket.recv(20*client_auth[2])

        filenames = clientsocket.recv(20)
        print("File name:", filenames.decode("utf-8"))
        newWriteFile = open("../files/"+filenames.decode("utf-8"), mode='wb')

        data = clientsocket.recv(1024)
        while data:
            print("data:", data)
            newWriteFile.write(data)
            data = clientsocket.recv(1024)
        newWriteFile.close()
        print("Writing done")

        index_file.write(str(client_auth[1]) + filenames.decode("utf-8")+'\n')
        index_file.close()
        #
        # data = file.read(BUFF_SIZE)
        # while data:
        #     clientsocket.sendall(data)
        #     data = file.read(BUFF_SIZE)
        clientsocket.close()