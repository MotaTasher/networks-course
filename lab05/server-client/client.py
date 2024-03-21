import socket


receive_size = 1024
def ReceiveHolder(local_socket: socket.socket, timeout: float=5):
    local_socket.settimeout(timeout)
    response = b"Empty"
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

command = 'ls'

command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_socket.connect((server_host, server_port))

command_socket.send(command.encode())

result = ReceiveHolder(command_socket).decode()
print(f"Result of command {command}: ")
print(result)

command_socket.close()
