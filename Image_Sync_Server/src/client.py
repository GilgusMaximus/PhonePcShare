import socket
import os
import struct

ID_PATH = "id.txt"

HOST = '127.0.0.1'  # '192.168.178.3'  # The server's hostname or IP address
PORT = 5555  # The port used by the server
BUFFER_SIZE = 2048
CLIENT_ID = 1
CLIENT_LIST = []
CLIENT_FILES_STORE_LOCATION = "../client_files/"
CLIENT_ALREADY_REGISTERED = False


def receive_messages_from_server(c_socket):
    server_data_decoded = ""
    server_data_raw = c_socket.recv(BUFFER_SIZE)
    # receive the number of files
    while server_data_raw:
        server_data_decoded += server_data_raw.decode()
        if len(server_data_raw) < BUFFER_SIZE:
            # end of data
            break
        server_data_raw = c_socket.recv(BUFFER_SIZE)
    return server_data_decoded


def receive_messages_from_server_raw(c_socket):
    server_data_decoded = []
    server_data_raw = c_socket.recv(BUFFER_SIZE)
    # receive the number of files
    while server_data_raw:
        server_data_decoded += server_data_raw.decode()
        if len(server_data_raw) < BUFFER_SIZE:
            # end of data
            break
        server_data_raw = c_socket.recv(BUFFER_SIZE)
    return server_data_decoded


# takes a string and then encodes the string in order to send it to the server
def send_single_message_to_server(c_socket, message):
    c_socket.sendall(message.encode())


def send_single_message_to_server_raw(c_socket, message):
    c_socket.sendall(message)


def receive_client_list_from_server(c_socket):
    received_string = ""
    list_data = c_socket.recv(BUFFER_SIZE)
    # receive data from the server until the server does send less than 2048 bytes -> end of list
    while list_data:
        received_string += list_data.decode()
        if len(list_data) < BUFFER_SIZE:
            # end of data stream
            break
        list_data = c_socket.recv(BUFFER_SIZE)
    # is the first byte of the server message a 0, as expected?
    if received_string[0] != "0":
        # no -> abort
        print("ERROR: No acknowledgement before client list")
        SystemExit(-1)
    # yes -> take client list string
    client_list_string = received_string[1:]
    return client_list_string


# attempts to receive the data from the server about possible waiting files and then tries to download them
def download_files_from_server(c_socket):
    file_counter = 0
    print("Requested file download from server...")

    # receive the information about the queued files
    download_file_names = eval(receive_messages_from_server(c_socket))

    print("File download request accepted.", len(download_file_names), "files will be downloaded.")
    # send the final clearance to receive files
    send_single_message_to_server(c_socket, str(0))
    # for the number of files available, each time receive the data and write it into a file
    for i in range(0, len(download_file_names)):
        curr_file = open(CLIENT_FILES_STORE_LOCATION + download_file_names[i] + ".txt", mode='wb+')
        file_counter += 1
        server_data = c_socket.recv(BUFFER_SIZE)
        # receive the client list
        while server_data:
            # write byte data to a file
            curr_file.write(server_data)
            if len(server_data) < BUFFER_SIZE:
                #curr_file.write(server_data)
                # either 0 or end of data
                break
            server_data = c_socket.recv(BUFFER_SIZE)
        curr_file.close()
        # send acknowledge for this file
        send_single_message_to_server(c_socket, "ACK")

        print("ACKKER")
    return download_file_names


# tries to open the file which should be sent, and if available, then reads and sends it to the server
def send_file_to_server(c_socket, filepath):
    if os.path.exists(filepath):
        # send the server the name of the file
        #send_single_message_to_server(c_socket, filename)
        print("File found. Start sending...")
        open_file = open(filepath, mode='rb')
        file_data = open_file.read(BUFFER_SIZE)
        while file_data:
            c_socket.sendall(file_data)
            file_data = open_file.read(BUFFER_SIZE)
        print("...sending done.")
        open_file.close()
    else:
        print("ERROR: File under path", filepath, "was not found. Aborting sending of file.")


# wrapper function around the actual sending, which handles the messages that are being send for the acknowledgements
def send_files_to_server(c_socket, filepaths, filenames, receiver_id):
    # send the server the info 'sending', the receiver if, how many files the client wants to send and the list of file names
    send_single_message_to_server(c_socket, str(1)+str(receiver_id)+str(len(filepaths))+str(filenames))
    server_response = receive_messages_from_server(c_socket)
    if int(server_response) == 0:
        for i in range(0, len(filepaths)):
            curr_filepath = filepaths[i]
            send_file_to_server(c_socket, curr_filepath)
            server_file_response = receive_messages_from_server(c_socket)
            if server_file_response != "ACK":
                print("ERROR: Server did not acknowledge file.", str(i-1), "out of", str(len(filepaths)), "sent successfully. Aborting remaining sending process.")
                break


# TODO make it writing a settings file
def write_id_file(c_id, c_name):
    id_file = open(CLIENT_FILES_STORE_LOCATION+ID_PATH, mode='w+')
    id_file.writelines(c_id)
    id_file.writelines(c_name)
    id_file.close()


# send the server the new name of the device
def update_device_name(new_device_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        send_single_message_to_server(client_socket, "3"+str(CLIENT_ID))
        send_single_message_to_server(client_socket, new_device_name)
        message = receive_messages_from_server(client_socket)
        if message[0] == "0" and message[1:] == new_device_name:
            write_id_file(CLIENT_ID, new_device_name)
        return


# read the client id or register the client at the server
def setup_client(device_name):
    global CLIENT_ID
    global CLIENT_LIST
    if os.path.exists(CLIENT_FILES_STORE_LOCATION+ID_PATH):
        client_id_file = open(CLIENT_FILES_STORE_LOCATION+ID_PATH, mode='r')
        client_id_read = client_id_file.readline()
        client_name_read = client_id_file.readline()

        client_id_file.close()
        # check if the read file was empty or not
        if client_id_read == "" or client_name_read == "":
            # if the file was empty, no id was read -> therefore delete the file and restart the setup
            os.remove(CLIENT_FILES_STORE_LOCATION+ID_PATH)
            setup_client(device_name)
            return device_name
        else:
            CLIENT_ID = int(client_id_read)
            return client_name_read
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            send_single_message_to_server(client_socket, (str(0)+str(1)))
            CLIENT_ID = receive_messages_from_server(client_socket)
            print("IDIDIDIDI:", CLIENT_ID)
            write_id_file(CLIENT_ID, device_name)
            send_single_message_to_server(client_socket, device_name)
            if receive_messages_from_server(client_socket) != device_name:
                print("ERROROROROR: WRONG NAME SENT BACK")
            CLIENT_LIST = eval(receive_client_list_from_server(client_socket))
            client_socket.close()
        return device_name


# function used to check whether files are available for download and whether new clients are available
def update_download_client_list():
    global CLIENT_LIST
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        # pack the action and the own id as raw bytes because a 2 decimal id will use > 1 Byte if converted to string
        s = struct.pack("!2B", 2, CLIENT_ID)
        send_single_message_to_server_raw(client_socket, s)
        # receive the list of all client that registered on the server
        CLIENT_LIST = eval(receive_client_list_from_server(client_socket))
        # download possible waiting files
        files = download_files_from_server(client_socket)
        client_socket.close()
        return files, CLIENT_LIST


# setup the socket for sending files and call the respective function
def file_send_setup(filepaths, filenames ,receiver_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        send_single_message_to_server(client_socket, str(1)+str(CLIENT_ID))
        send_files_to_server(client_socket, filepaths=filepaths, filenames=filenames, receiver_id=receiver_id)
        client_socket.close()
