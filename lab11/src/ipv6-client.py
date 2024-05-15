import socket

def run_client(server_ip, port=12345):
    client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print(f"Connected to {server_ip} on port {port}")

    try:
        while True:
            message = input("Enter message to send (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            client_socket.sendall(message.encode('utf-8'))
            data = client_socket.recv(1024)
            print(f"Received from server: {data.decode('utf-8')}")
    finally:
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    server_ip = "::1"
    run_client(server_ip)
