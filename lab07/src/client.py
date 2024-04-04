import socket
import argparse
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
            # print("Have timeout")
            break
        except Exception as e:
            print("Unknow error ", e)
            break
    return response, addr

def SendMsgToServer(server_host: str, server_port: str, msg: str):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    start_time = time.time()

    sock.sendto(msg.encode(), (server_host, server_port))
    
    answer, addr = ReceiveHolderUDP(sock)
    end_time = time.time()
    if addr is None:
        return None, None
    else:
        return answer.decode(), end_time - start_time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--server_host", default='127.0.0.1', type=str)
    parser.add_argument("--server_port", default=9000, type=int)

    parser.add_argument("--msg", default="Hello world!", type=str)
    parser.add_argument("--cnt", default=10, type=int)

    args = parser.parse_args()
    global_start_time = time.time()

    times = set()

    # print(f"")
    for i in range(args.cnt):
        print(f"Ping {i + 1:2.0f}: {1e3 * (time.time() - global_start_time):8.2f} microseconds")
        answer, rtt = SendMsgToServer(args.server_host, args.server_port, args.msg)
        if rtt is not None:
            times.add(rtt)
        print(answer)
        if len(times) == 0:
            print(f"""timeout: {(i + 1 - len(times)) / (i + 1) * 100:3.1f}%, """
                    f"""\n"""
                    )
        else:
            print(f"""RTT: """
                    f"""mean: {1e6 * sum(times) / len(times):6.1f}ms, """
                    f"""min: {1e6 * min(times):6.1f}ms, """
                    f"""max: {1e6 * max(times):6.1f}ms, """
                    f"""timeout: {(i + 1 - len(times)) / (i + 1) * 100:3.1f}%, """
                    f"""\n"""
                    )
            
