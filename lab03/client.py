import socket
import argparse



def GetRequestStr(filename, host, port):
    return f"GET /{filename} HTTP/1.1 Host: {host}:{port}\r\n\n"

def Main(host, port, filename):
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    local_socket.connect((host, port))
    local_socket.sendall(GetRequestStr(filename, host, port).encode())

    data = local_socket.recv(1024)

    print(data)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('server_host')
    parser.add_argument('server_port')
    parser.add_argument('filename')
    args = parser.parse_args()
    Main(args.server_host,int(args.server_port), args.filename)