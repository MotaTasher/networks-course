import socket
import struct
import time
import select
import argparse

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

def create_packet(id):
    header = struct.pack('>BBHHH', ICMP_ECHO_REQUEST, ICMP_CODE, 0, id, 1)
    data = 192 * b'Q'
    my_checksum = calculate_checksum(header + data)
    header = struct.pack('>BBHHH', ICMP_ECHO_REQUEST, ICMP_CODE, my_checksum, id, 1)
    return header + data

def get_hostname(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        return ip

def main(dest_name, max_hops=30, num_packets=3, timeout=2.0):
    dest_addr = dest_name
    port = 33434
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    print(f'Tracing route to {dest_name} [{dest_addr}] over a maximum of {max_hops} hops:')

    for ttl in range(1, max_hops + 1):
        for _ in range(num_packets):
            recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
            send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            timeout_packet = struct.pack("ll", int(timeout), 0)
            recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout_packet)
            
            recv_socket.bind(("", port))
            id = 42
            packet = create_packet(id)
            send_socket.sendto(packet, (dest_addr, port))
            
            start_time = time.time()
            ready = select.select([recv_socket], [], [], 5)
            if ready[0]:
                _, curr_addr = recv_socket.recvfrom(512)
                time_received = time.time()
                curr_addr = curr_addr[0]
                hostname = get_hostname(curr_addr)
                print(f"{ttl}\t{curr_addr} ({hostname})\t{int((time_received - start_time) * 1000)} ms")
            else:
                print(f"{ttl}\t*\tRequest timed out.")

            send_socket.close()
            recv_socket.close()

        if curr_addr == dest_addr:
            print("Trace complete.")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    icmp_seq = 1

    parser.add_argument("--max_hops", default=30, type=int)
    parser.add_argument("--num_packets", default=3, type=int)
    parser.add_argument("--host", default='google.com', type=str)
    parser.add_argument("--timeout", default=2.0, type=float)
    args = parser.parse_args()
    
    host = args.host
    timeout = args.timeout
    num_packets = args.num_packets
    max_hops = args.max_hops
    main(host, max_hops, num_packets, timeout)
