import socket
import argparse
import numpy as np
import typing as tp
import time

kRecvSize = 1024


receive_size = 1024
def ReceiveHolderUDP(local_socket: socket.socket, timeout: float=1):
    local_socket.settimeout(timeout)
    response = b"" 
    addr = None
    while True:
        try:
            data, addr = local_socket.recvfrom(receive_size)
            if not data:
                break
            response += data
            if len(data) < receive_size:
                break
        except socket.timeout:
            # print("Time out")
            break
        except Exception as e:
            print("Unknow error ", e)
            break
    return response, addr

def CheckLives(lives: tp.Dict[int, float], max_diff: float = 4):
    t = time.time()

    for_del = []
    # print("Start check", t, lives)
    for ind in lives.keys():
        last_time = lives[ind]
        if last_time + max_diff < t:
            for_del.append(ind)
    
    for ind in for_del:
        print(f"Index {ind} died")
        lives.pop(ind)

def RunEchoServerWithLost(host: str, port: str):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind((host, port))

    alive_application = {}

    last_check = time.time()
    time_check = 1

    while True:
        data, addr = ReceiveHolderUDP(sock)
        if last_check + time_check < time.time():
            CheckLives(alive_application)
        if np.random.randint(0, 5) == 0 or addr is None:
            continue

        ind, t = data.decode().split()
        if alive_application.get(ind, None) is None:
            print("Reiterate: ", ind)
        alive_application[ind] = float(t)


        sock.sendto(data.decode().upper().encode(), addr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default='127.0.0.1', type=str)
    parser.add_argument("--port", default=9000, type=int)
    args = parser.parse_args()
    RunEchoServerWithLost(args.host, args.port)