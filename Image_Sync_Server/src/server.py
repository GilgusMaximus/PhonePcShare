import socket as socket
import os
from binascii import hexlify
import time

# hostName = socket.gethostbyname( '192.168.178.2' )
hostName = '127.0.0.1'
REGISTERED_FILE = "../files/registered.txt"
INDEX_FILE = "../files/fileindex.txt"
PORT = 5555
BUFF_SIZE = 2048

stored_files = []
active_clients = []

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((hostName, PORT))

serversocket.listen(5)


# file = open("D:/a.txt", mode='rb')


def read_registered_file():
    # Does the file already exist?
    if os.path.exists(REGISTERED_FILE):
        # yes -> read all users as well as the total number of users
        print("Registered File exists. reading...")
        registered_clients = open(REGISTERED_FILE, mode='r')
        number_stored_clients = int(registered_clients.read(1))
        registered_clients.close()
        # create as many file lists as there are total registered users
        for i in range(0, number_stored_clients):
            stored_files.append([])
        print("...done reading registered file.")
    else:
        # no -> create a new registered file for upcoming users
        print("Registered File does not exist. Creating...")
        registered_clients = open(REGISTERED_FILE, mode='c')
        # registered_clients.write("0")
        # registered_clients.close()
        print("...done creating registered file.")
        number_stored_clients = 0
    return number_stored_clients


def read_index_file():
    # does the INDEX file exist?
    if os.path.exists(INDEX_FILE):
        # yes -> read its content
        print("Index File exists. reading...")
        index_file = open(INDEX_FILE, mode='r')
        # read all lines
        while index_file:
            print("a")
            # split the lines for white space -> [0] is the id of the receiver and [1] is the file, an
            line = index_file.readline()
            if line != "":
                text = line.split()
                stored_files[int(text[0])].append(text[1])
            else:
                break
        index_file.close()
        print("...done reading Index File")


def send_file(filename, file_path, client_socket):
    print("Start sending process to", client_socket.getsockname()[0], ".")
    sending_file = open(file_path + filename, mode="rb")
    print("File opened successfully.")
    file_data = sending_file.read(BUFF_SIZE)
    while file_data:
        client_socket.sendall(file_data)
        file_data = sending_file.read(BUFF_SIZE)
    sending_file.close()
    print("Sending file finished.")


def register_client(csocket, number_registered_clients):
    print("Registering clients", number_registered_clients)
    # increase number of registered clients so we know which ids to expect
    number_registered_clients += 1
    registered_clients = open("../files/registered.txt", mode='w')
    registered_clients.write(str(number_registered_clients))
    registered_clients.close()

    csocket.send(number_registered_clients.to_bytes(1, byteorder='big'))
    print(csocket.getsockname()[0])
    active_clients.append([number_registered_clients, csocket.getsockname()[0]])
    print("New client registered. Currently Active Client:", str(active_clients))
    return number_registered_clients


def save_file(file_data, type, name):
    print("Writing file to system...")
    write_file = open("./" + name + "." + type, mode="wb+")
    write_file.write(file_data)
    write_file.close()
    print("...finished writing file to system.")
    return None


def receive_data(csocket):
    print("Receiving and sending files")
    return 0


def send_data(csocket):
    return 0


def send_all_registered_devices(client_socket):
    clients_array = str(0) + str(active_clients)
    print(clients_array)
    sending_data = clients_array.encode()
    client_socket.sendall(sending_data)
    return

def delete_sent_files(csocket):
    print("Deleting files")
    return 0


number_registered_clients = read_registered_file()

print("Entering listening mode")
while True:

    (clientsocket, address) = serversocket.accept()
    with clientsocket:
        print("Found a client. Setting up connection")
        # what kind of interaction
        initial_send = int.from_bytes(clientsocket.recv(1), byteorder='big')

        print("Initial byte", initial_send)

        if initial_send == 0:
            # register
            number_registered_clients = register_client(clientsocket, number_registered_clients)
            send_all_registered_devices(clientsocket)
        elif initial_send == 1:
            # first send files to client and then receive files from client
            send_all_registered_devices(clientsocket)
            send_data(clientsocket)
            receive_data(clientsocket)
        # [id, send to phone/pc, how many images sent]
        # client_auth = clientsocket.recv(3)

        # client will then send all of the file names (max length 20 with file type) so that the server can create these intermediate
        # filenames = clientsocket.recv(20*client_auth[2])

        filenames = clientsocket.recv(20)
        print("File name:", filenames.decode("utf-8"))
        newWriteFile = open("../files/" + filenames.decode("utf-8"), mode='wb')

        data = clientsocket.recv(BUFF_SIZE)
        while data:
            print("data:", data)
            newWriteFile.write(data)
            data = clientsocket.recv(BUFF_SIZE)
            if not data:
                break
        clientsocket.close()
        newWriteFile.close()
        print("Writing done")

        # index_file.write(str(client_auth[1]) + " " + filenames.decode("utf-8")+'\n')
        # index_file.close()
        #
        # data = file.read(BUFF_SIZE)
        # while data:
        #     clientsocket.sendall(data)
        #     data = file.read(BUFF_SIZE)
        clientsocket.close()
