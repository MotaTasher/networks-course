import socket
import subprocess

receive_size = 1024
def ReceiveHolder(local_socket: socket.socket, timeout: float=1):
    local_socket.settimeout(timeout)
    response = b""
    while True:
        try:
            data = local_socket.recv(receive_size)
            if not data:
                break
            response += data
        except socket.timeout:
            break
        except Exception as e:
            print("Unknow error ", e)
            break
    return response


server_host = '127.0.0.1'
server_port = 9900

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for port in range(server_port, server_port + 100):
    try:
        server_socket.bind((server_host, server_port))
    except:
        continue

server_socket.listen(3)

print(f"Server work on port: {server_socket.getsockname()}")

while True:
    client_socket, client_address = server_socket.accept()
    print("Подключение установлено с", client_address)

    command = ReceiveHolder(client_socket).decode()
    print("Получена команда:", command)

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        result = e.output

    client_socket.send(result)

    client_socket.close()
