import socket
import struct
import time
import argparse
import os

# ICMP параметры
ICMP_ECHO_REQUEST = 8
ICMP_CODE = 0
ICMP_HEADER_SIZE = 8

def calculate_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        checksum += (data[i] << 8) + (data[i + 1])
    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    checksum = ~checksum & 0xFFFF
    return checksum


def send_ping(dest_addr, ttl, timeout=3):
    """Отправляет ICMP-запрос и получает время отклика."""
    icmp = socket.getprotobyname("icmp")
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

    my_id = os.getpid() & 0xFFFF
    header = struct.pack('>BBHHH', ICMP_ECHO_REQUEST, ICMP_CODE, 0, my_id, 1)
    my_checksum = calculate_checksum(header)
    header = struct.pack('>BBHHH', ICMP_ECHO_REQUEST, ICMP_CODE, my_checksum, my_id, 1)

    my_socket.sendto(header, (dest_addr, 1))
    time_sent = time.time()
    
    time_left = timeout
    my_socket.settimeout(timeout)
    try:
        # Получает ответ
        recv_packet, addr = my_socket.recvfrom(1024)
        delay = time.time() - time_sent
    except socket.timeout:
        delay = None

    my_socket.close()
    return delay


# Проверка через ICMP-пинг


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    icmp_seq = 1

    parser.add_argument("--cnt_trys", default='30', type=int)
    parser.add_argument("--ttl", default='128', type=int)
    parser.add_argument("--host", default='127.0.0.1', type=str)
    parser.add_argument("--timeout", default=2.0, type=float)
    args = parser.parse_args()
    
    host = args.host
    timeout = args.timeout
    ttl = args.ttl
    cnt_trys = args.cnt_trys
    while True:

        sums_delays = 0
        cnt_success = 0
        cnt_miss = 0 
        for ind in range(cnt_trys):
            
            delay = send_ping(host, ttl, timeout)
            if delay is None:
                cnt_miss += 1
            else:
                cnt_success += 1
                sums_delays += delay

        print(f"64 bytes from {host}: icmp_seq={icmp_seq} ttl={ttl} time={sums_delays / cnt_success * 1e3:.3f} ms, miss={cnt_miss / cnt_trys * 100:.2f}%")
        icmp_seq += 1
