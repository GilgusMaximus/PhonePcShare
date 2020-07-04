import socket
import os
import time

ID_PATH = "./client_files/id"

HOST = '127.0.0.1'  # '192.168.178.3'  # The server's hostname or IP address
PORT = 5555  # The port used by the server
BUFFER_SIZE = 2048
CLIENT_ID = 1
CLIENT_LIST = []
CLIENT_FILES_STORE_LOCATION = "../c_files/"
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


# takes a string and then encodes the string in order to send it to the server
def send_single_message_to_server(c_socket, message):
    c_socket.sendall(message.encode())


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
    # send the request to receive files
    send_single_message_to_server(c_socket, str(0))

    # receive the information about the queued files
    server_message = receive_messages_from_server(c_socket)
    print("File download request accepted.", server_message, "files will be downloaded.")
    # send the final clearance to receive files
    send_single_message_to_server(c_socket, str(0))
    # for the number of files available, each time receive the data and write it into a file
    for i in range(0, int(server_message)):
        curr_file = open(CLIENT_FILES_STORE_LOCATION + str(file_counter) + ".txt", mode='wb+')
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
        c_socket.sendall("ACK".encode())


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
            curr_filename = filenames[i]
            send_file_to_server(c_socket, curr_filepath)
            server_file_response = receive_messages_from_server(c_socket)
            if server_file_response != "ACK":
                print("ERROR: Server did not acknowledge file.", str(i-1), "out of", str(len(filepaths)), "sent successfully. Aborting remaining sending process.")
                break


#####################################################################################################################
#                                           Start of the main routine
#####################################################################################################################
if os.path.exists(ID_PATH):
    client_id_file = open(ID_PATH, mode='r')
    CLIENT_ID = int(client_id_file.read(1))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    # did the client already connect to the server and save an assigned id?
    if CLIENT_ID == -1:
        # no -> send server the information that a new client id must be issued
        send_string = str(0) + str(1)
        send_single_message_to_server(client_socket, send_string)
        CLIENT_ID = int.from_bytes(client_socket.recv(1), byteorder="big")
    else:
        # yes -> send the server the information that the client already registered as well as the assigned id
        send_string = str(1) + str(CLIENT_ID)
        send_single_message_to_server(client_socket, send_string)
        CLIENT_ALREADY_REGISTERED = True

    client_list = eval(receive_client_list_from_server(client_socket))
    print("Client list:", client_list)
    if CLIENT_ALREADY_REGISTERED:
        download_files_from_server(client_socket)

    # send the server the files
    send_files_to_server(client_socket, ["../test.txt"], ["test23224.txt"], 1)


