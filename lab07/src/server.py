import socket
import argparse
import numpy as np

kRecvSize = 1024


def RunEchoServerWithLost(host: str, port: str):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind((host, port))

    alive_application = {}

    while True:
        data, addr = sock.recvfrom(kRecvSize)
        if np.random.randint(0, 5) == 0:
            continue

        print("Receive from: ", addr)

        sock.sendto(data.decode().upper().encode(), addr)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default='127.0.0.1', type=str)
    parser.add_argument("--port", default=9000, type=int)
    args = parser.parse_args()
    RunEchoServerWithLost(args.host, args.port)