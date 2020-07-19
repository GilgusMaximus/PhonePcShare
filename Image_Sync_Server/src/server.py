import socket as socket
import os


hostName = '127.0.0.1'
REGISTERED_FILE = "../files/registered.txt"
INDEX_FILE = "../files/fileindex.txt"
STORED_FILES_PATH = "../files/stored_files/"
PORT = 5555
BUFF_SIZE = 2048

stored_files = []  # each client gets an array with all it's associated files
active_clients = []  # each element is a list representing an client with the following structure: [Id, Ip, Name]

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((hostName, PORT))

serversocket.listen(5)

# receive a single message from a client and decode it for the calling function
def receive_message_from_client(c_socket):
    client_data_decoded = ""
    client_data_raw = c_socket.recv(BUFF_SIZE)
    # receive the number of files
    while client_data_raw:
        client_data_decoded += client_data_raw.decode()
        if len(client_data_raw) < BUFF_SIZE:
            # end of data
            break
        client_data_raw = c_socket.recv(BUFF_SIZE)
    print("> Received message from client:", client_data_decoded)
    return client_data_decoded


# takes a string and then encodes the string in order to send it to the server
def send_single_message_to_client(c_socket, message):
    c_socket.sendall(message.encode())


# reads the file with the number of registered users
def read_registered_file():
    # Does the file already exist?
    if os.path.exists(REGISTERED_FILE):
        # yes -> read all users as well as the total number of users
        print("Registered File exists. reading...")
        registered_clients = open(REGISTERED_FILE, mode='r')
        number_stored_clients = int(registered_clients.read(3))
        registered_clients.close()
        # create as many file lists as there are total registered users
        for i in range(0, number_stored_clients):
            stored_files.append([])
        print("...done reading registered file.")
    else:
        # no -> create a new registered file for upcoming users
        print("Registered File does not exist. Creating...")
        registered_clients = open(REGISTERED_FILE, mode='w+')
        registered_clients.write("0")
        registered_clients.close()
        print("...done creating registered file.")
        number_stored_clients = 0
    return number_stored_clients


# reads the file with the information about which file should be forwarded to which client
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


def write_index_file():
    if not os.path.exists(INDEX_FILE):
        open_file = open(INDEX_FILE, mode='w+', encoding='utf-8')
    else:
        open_file = open(INDEX_FILE, mode='w')
    for j in range(0, len(stored_files)):
        curr_array = stored_files[j]
        if len(curr_array) > 0:
            for file in curr_array:
                open_file.writelines(str(j) + " " + file)


# registers a new client in the system and updates the number of registered users
def register_client(csocket, number_registered_clients):
    print("Registering clients", number_registered_clients)
    # increase number of registered clients so we know which ids to expect
    number_registered_clients += 1
    registered_clients = open("../files/registered.txt", mode='w')
    registered_clients.write(str(number_registered_clients))
    registered_clients.close()

    send_single_message_to_client(csocket, str(number_registered_clients))
    device_name = receive_message_from_client(csocket)
    send_single_message_to_client(csocket, device_name)
    print(csocket.getsockname()[0])
    active_clients.append([number_registered_clients, csocket.getsockname()[0], device_name])

    print("New client with name", device_name, "registered. Currently Active Client:", str(active_clients))
    return number_registered_clients


# receive the data teh client is sending and write it to the given file on the system
def receive_file(c_socket, filename, filepath):
    # open the file
    opened_file = open(filepath+filename, mode='wb+')
    # receive the first bytes of data
    file_data = c_socket.recv(BUFF_SIZE)
    # while there is data from the client, write it to the file
    while file_data:
        opened_file.write(file_data)
        # if the client sent less than the maximum size of data, then the client is done sending, so break out of loop
        if len(file_data) < BUFF_SIZE:
            #opened_file.write(file_data)
            break
        file_data = c_socket.recv(BUFF_SIZE)
    opened_file.close()


# wrapper function around receive_file which handles the messages that are sent between client and server
def receive_files_from_client(c_socket):
    # client initiates the process with message "1numOfFiles[filename1, filename2,.."
    print("Client initiated sending of files.")
    client_send_info = receive_message_from_client(c_socket)
    if int(client_send_info[0]) != 1:
        print("ERROR: Client sent wrong initiation. Closing client.")
        c_socket.close()

    file_receiver_id = int(client_send_info[1])
    if file_receiver_id > number_registered_clients:
        print("ERROR: Client sent wrong receiver ID. ID does not exist. Closing client.")
        c_socket.close()

    number_of_files = int(client_send_info[2])
    file_name_array = eval(client_send_info[3:])
    # server should send a 0 byte to signal that everything is ok
    send_single_message_to_client(c_socket, str(0))
    # receive the files and after each file send an ACK message to the client to let it know, the server got the file
    for j in range(0, number_of_files):
        receive_file(c_socket, file_name_array[j], STORED_FILES_PATH)
        send_single_message_to_client(c_socket, "ACK")
        # add the file to the list of stored files for the other device
        stored_files[file_receiver_id].append(file_name_array[j])
    print("Received all files successfully.")


# open the specified file, and send it to the client in byte form
def send_file(filename, file_path, client_socket):
    # explanation equal to receive_file()
    print("Start sending process to", client_socket.getsockname()[0], ".")
    sending_file = open(file_path + filename, mode="rb")
    print("File opened successfully.")
    file_data = sending_file.read(BUFF_SIZE)
    while file_data:
        client_socket.sendall(file_data)
        file_data = sending_file.read(BUFF_SIZE)
    sending_file.close()
    print("Sending file finished.")


# wrapper function around the send_file function, which handles the messages that are send between client and server
def send_stored_files(client_socket, c_id):
    # send the client the array with the file names
    send_single_message_to_client(client_socket,str(stored_files[c_id]))
    client_answer = int(receive_message_from_client(client_socket))

    # does the client want to receive the files?
    if client_answer == 0:
        # yes -> start sending the files
        print("Client allows sending of files, initiating packages...")
        for j in range(len(stored_files[c_id]) - 1, -1, -1):
            stored_file_index = stored_files[c_id][j]
            send_file(stored_file_index, STORED_FILES_PATH, client_socket)

            client_file_ack = receive_message_from_client(client_socket)
            if client_file_ack != "ACK":
                print("ERROR: Client did not send ACK BACK, therefore stopping transmission of files")
                break
            else:
                # transmission successfully, therefore deleting the files locally
                #os.remove("../files/"+stored_file_index) TODO WIEDER EINFÜGEN
                stored_files[c_id].pop(j)
        print("Done sending files to client.")
    else:
        # no -> do nothing
        print("Client did not allow to send files.")
        return None


# sends the client the current list of clients available
def send_all_registered_devices(client_socket):
    clients_array = str(0) + str(active_clients)
    print(clients_array)
    send_single_message_to_client(client_socket, clients_array)
    return


number_registered_clients = read_registered_file()
read_index_file()
print("Entering listening mode")
while True:
    (clientsocket, address) = serversocket.accept()
    with clientsocket:
        print("Found a client. Setting up connection")
        # what kind of interaction
        c_initial_send = receive_message_from_client(clientsocket)
        initial_send = int(c_initial_send[0])
        client_id = int(c_initial_send[1])
        print("Initial byte", initial_send)

        if int(initial_send) == 0:
            # register
            number_registered_clients = register_client(clientsocket, number_registered_clients)
            send_all_registered_devices(clientsocket)

        elif int(initial_send) == 1:
            # receive files
            #send_all_registered_devices(clientsocket)

            #client_file_request = int(receive_message_from_client(clientsocket))
            #if client_file_request == 0:
            #    send_stored_files(clientsocket, client_id)
            receive_files_from_client(clientsocket)
        elif int(initial_send) == 2:
            # send files
            send_all_registered_devices(clientsocket)
            send_stored_files(clientsocket, client_id)
        clientsocket.close()
        write_index_file()
