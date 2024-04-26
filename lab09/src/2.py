import socket
import argparse

def find_open_ports(ip_address, port_range, timeout):
    open_ports = []
    for port in port_range:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((ip_address, port))
        
        if result != 0:
            open_ports.append(port)
        
        sock.close()
    
    return open_ports


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--ip_address", type=str, default='127.0.0.1')
    parser.add_argument("--first_port", type=int, default=0)
    parser.add_argument("--last_port", type=int, default=128)
    parser.add_argument("--timeout", type=float, default=0.5)

    args = parser.parse_args()
    
    ip_address = args.ip_address
    start_port = args.first_port
    end_port = args.last_port
    timeout = args.timeout
    port_range = range(start_port, end_port + 1)
    open_ports = find_open_ports(ip_address, port_range, timeout)
    
    print(open_ports)