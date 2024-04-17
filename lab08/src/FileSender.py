import checksum
import random
import socket

def SplitFile(filename, size):
    packets = []
    with open(filename, 'rb') as file:
        while True:
            data = file.read(size)
            if not data:
                return
            yield data


def FakeRecvFrom(socket: socket.socket, size):
    while True:
        data, client_address = socket.recvfrom(size)

        if random.random() > 0.3:
            return data, client_address


def SendingFile(socket_send: socket.socket, address, timeout, generator):
    socket_send.settimeout(timeout)
    for ind, data in enumerate(generator):
        while True:
            data = ind.to_bytes(4, 'little') + data
            socket_send.sendto(checksum.CreatePacket(data), address)
            try:
                data, addr = FakeRecvFrom(socket_send, 1024)
                get_ind = int.from_bytes(checksum.GetData(data)[:4], 'little')
                print("Try send: ", ind, ' ack: ', get_ind)
                if checksum.ValidatePacket(data) and get_ind == ind + 1:
                    break
            except socket.timeout:
                continue
    print("End sending")

def GettingFile(socket_get: socket.socket, timeout):
    socket_get.settimeout(timeout)
    data = b''

    ind_wait = 0
    last_packet = None
    while True:
        try:
            data, address = FakeRecvFrom(socket_get, 1024)
            get_ind = int.from_bytes(checksum.GetData(data)[:4], 'little')
            print("Try get: ", ind_wait, " got ", get_ind)
            # print("Send to ", address)
            if checksum.ValidatePacket(data) and get_ind == ind_wait:
                ind_wait += 1
                ack = ind_wait
                last_packet = checksum.CreatePacket(ack.to_bytes(4, 'little'))
                socket_get.sendto(checksum.CreatePacket(ack.to_bytes(4, 'little')) , address)
            else:
                if not last_packet is None:
                    socket_get.sendto(last_packet, address)


        except socket.timeout:
            break
    return data

