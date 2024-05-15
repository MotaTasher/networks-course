import socket

def run_server(port=12345):
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(1)
    print(f"Listening on port {port}...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connected to {addr}")
            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    client_socket.sendall(data.upper())
            finally:
                client_socket.close()
                print(f"Connection with {addr} closed")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_server()
