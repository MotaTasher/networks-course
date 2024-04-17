import checksum

import socket
import random
import os
import argparse
import FileSender


def server(filename, timeout, host, port, size):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    
    print("Server started, waiting for messages...")
    print("Server listening on: ", server_socket.getsockname())

    while True:
        try:
            data, client_address = FileSender.FakeRecvFrom(server_socket, 1024)

            message, _ = data.decode().split('|')
            print(message)
            # packet_number = int(packet_number)

            # print(f"Received packet {packet_number}: {message} from {client_address}")

            # print(f"Acknowledging packet {packet_number}")
            # server_socket.sendto(str(packet_number).encode(), client_address)
            
            if message == "REQUEST_FILE":
                print("Sending file to client...")
                FileSender.SendingFile(server_socket, client_address, timeout, FileSender.SplitFile(filename, size))
                print("File sent successfully.")
        except socket.timeout:
            continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--timeout", default=0.5, type=float)
    parser.add_argument("--host", default='127.0.0.1', type=str)
    parser.add_argument("--port", default=0, type=int)
    parser.add_argument("--size", default=512, type=int)
    args = parser.parse_args()

    
    host = args.host
    port = args.port
    size = args.size
    filename = args.file
    timeout = args.timeout
    server(filename, timeout, host, port, size)


# filename = 'text_1.txt'
# size = 512
# with open(filename, 'rb') as file:
#     while True:
#         data = file.read(size)
#         if not data:
#             exit()
#         print(len(data).to_bytes(4, 'little'))