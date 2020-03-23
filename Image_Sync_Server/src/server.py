import socket as socket
import os
from binascii import hexlify
import time



REGISTERED_FILE = "../files/registered.txt"
INDEX_FILE = "../files/fileindex.txt"


stored_files = [[]]

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 2222))

serversocket.listen(5)

number_registered_clients = 0

# read the registered users
if os.path.exists(REGISTERED_FILE):
    registered_clients = open(REGISTERED_FILE, mode='r')
    number_registered_clients = int(registered_clients.read(1))
    registered_clients.close()
else:
    registered_clients = open(REGISTERED_FILE, mode='w')
    registered_clients.write("0")
    registered_clients.close()

# read the file which are stored temporarily with the ids
if os.path.exists(INDEX_FILE):
    index_file = open(INDEX_FILE, mode='r')
    # read all lines
    while index_file:
        # split the lines for white space -> [0] is the id of the receiver and [1] is the file
        line = index_file.readline()
        text = line.split()
        exists = False
        for array in stored_files:
            if array[0] == int(text[0]):
                array.append(text[1])
                exists = True
                break
        if not exists:
            stored_files.append([int(text[0]), text[1]])
    index_file.close()

file = open("D:/a.txt", mode='rb')

counter = 0

BUFF_SIZE = 1024


def register_client(csocket, number_registered_clients):
    print("Registering clients", number_registered_clients)
    #increase number of registered clients so we know which ids to expect
    number_registered_clients += 1
    registered_clients = open("../files/registered.txt", mode='w')
    registered_clients.write(str(number_registered_clients))
    registered_clients.close()


    csocket.send(number_registered_clients.to_bytes(1, byteorder='big'))

    return number_registered_clients

def receive_data(csocket):
    print("Receiving and sending files")
    return 0

def send_data(csocket):
    return 0

def send_all_registered_devices(csocket):
    return 0

def delete_sent_files(csocket):
    print("Deleting files")
    return 0

while True:
    (clientsocket, address) = serversocket.accept()
    with clientsocket:


        #what kind of interaction
        initial_send = int.from_bytes(clientsocket.recv(1), byteorder='big')

        print("Initial byte", initial_send)

        if initial_send == 0:
            #register
            number_registered_clients = register_client(clientsocket, number_registered_clients)
            send_all_registered_devices(clientsocket)
        elif initial_send == 1:
            # first send files to client and then receive files from client
            send_all_registered_devices(clientsocket)
            send_data(clientsocket)
            receive_data(clientsocket)
        # [id, send to phone/pc, how many images sent]
        #client_auth = clientsocket.recv(3)

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

        #index_file.write(str(client_auth[1]) + " " + filenames.decode("utf-8")+'\n')
        index_file.close()
        #
        # data = file.read(BUFF_SIZE)
        # while data:
        #     clientsocket.sendall(data)
        #     data = file.read(BUFF_SIZE)
        clientsocket.close()