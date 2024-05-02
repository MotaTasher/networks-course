import checksum
import FileSender

import socket
import random
import argparse



def client(host, port, timeout, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(timeout)  # Set a timeout for receiving ACK
    
    # Send request for file to server
    print("Requesting file from server...")
    
    with open(filename, "wb") as file:
        # while True:
        #     try:
        #         data, _ = FileSender.FakeRecvFrom(socket, 1024)

        #         packet_number, packet_data = data.decode().split('|')
        #         packet_number = int(packet_number)
                
        #         file.write(packet_data.encode())
                
        #         client_socket.sendto(str(packet_number).encode(), (host, port))
                
        #     except socket.timeout:
        #         break
        while True:
            client_socket.sendto("REQUEST_FILE|".encode(), (host, port))
            
            data = FileSender.GettingFile(client_socket, timeout)
            if len(data) == 0:
                continue
            file.write(data)
            break
    
    print("File received successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("port", type=int)
    parser.add_argument("--host", default='127.0.0.1', type=str)
    parser.add_argument("--timeout", default=2.0, type=float)
    args = parser.parse_args()
    
    filename = args.file
    host = args.host
    port = args.port
    timeout = args.timeout
    client(host, port, timeout, filename)
