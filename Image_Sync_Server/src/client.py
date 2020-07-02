import socket
import os
ID_PATH = "./client_files/id"

HOST = '127.0.0.1'#'192.168.178.3'  # The server's hostname or IP address
PORT = 5555        # The port used by the server

client_id = 1

if os.path.exists(ID_PATH):
    client_id_file = open(ID_PATH, mode='r')
    client_id = int(client_id_file.read(1))

file = open("../test.txt", "rb")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #data = s.recv(1024)
    # if the client does not have an id it needs to register first and then send data
    if client_id == -1:
        send_string = str(0)+str(1)
        s.sendall(send_string.encode())
        client_id = int.from_bytes(s.recv(1), byteorder="big")
    else:
        send_string = str(1) + str(client_id)
        s.sendall(send_string.encode())

    print(client_id)
    data = s.recv(2048)
    stringer = ""
    # receive the client list
    while data:
        stringer += data.decode()
        if len(data) < 2048:
            # either 0 or end of data
            break
        data = s.recv(2048)
    if stringer[0] != "0":
        print("ERROR: No acknowledgement before client list")
        SystemExit(-1)
    client_list = stringer[1:]
    print("Clientlist:", client_list)

    print("Requested file download from server...")
    # send the request to receive files
    s.sendall(str(0).encode())

    data = s.recv(2048)
    stringer = ""
    # receive the number of files
    while data:
        stringer += data.decode()
        if len(data) < 2048:
            # either 0 or end of data
            break
        data = s.recv(2048)
    print("File download request accepted.", stringer, "files will be downloaded.")
    print(stringer)
    # send the final clearance to receive files
    s.sendall(str(0).encode())
    file_c = 0
    for i in range(0, int(stringer)):
        curr_file = open("../c_files/"+str(file_c)+".txt", mode='wb+')
        file_c += 1
        data = s.recv(2048)
        # receive the client list
        while data:
            curr_file.write(data)
            if len(data) < 2048:
                curr_file.write(data)
                # either 0 or end of data
                break
            data = s.recv(2048)
        curr_file.close()
        s.sendall("ACK".encode())
    #startbytes
    #s.sendall(b'\x00\x03\x02')
    s.sendall(b"test.txt")

    data = file.read(1024)
    while data:
        s.sendall(data)
        data = file.read(1024)
    print("Sending done")
    s.close()
    # while data:
    #     print("i")
    #     file.write(data)
    #     data = s.recv(1024)
    # file.close()

#print('Received', repr(data))