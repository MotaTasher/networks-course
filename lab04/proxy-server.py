import socket
import argparse
import time
import ssl

import sys
import difflib

receive_size = 1024

noise = False


kErrorHttp = b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"


servers_stack = []

def StrToBytes(s: str):
    return s.encode().replace(b'\\r', b'\r').replace(b'\\n', b'\n')


def GetCode(receive: bytes):
    first_space = receive.find(b' ')
    second_space = receive.find(b' ', first_space + 1)
    code_str = BytesToStr(receive[first_space + 1: second_space])
    try:
        return int(code_str)
    except:
        return -1


def GetLocation(receive: bytes):
    location = b'Location: '
    rn = b'\r\n'
    start = receive.find(location)
    end = receive.find(rn, start)
    if noise: print(start, end)
    return receive[start + len(location): end]



def BytesToStr(s: bytes):
    return str(s)[2:-1]

    
def IsHTTPS(hostname: bytes):
    temp = b'://'
    pos = hostname.find(temp)
    if pos != -1 and hostname[pos - 1] == (b's')[0]: 
        return True
    else:
        return False


def DropTarget(hostname: bytes):
    temp = b'://'
    start = hostname.find(temp)
    prefix, suffix = '', hostname
    if start != -1:
        suffix = hostname[start + len(temp):]
        prefix = hostname[:start + len(temp)]

    end = suffix.find(b'/')

    if end != -1:
        suffix = suffix[:end]
    return prefix + suffix


def ReplaceHost(request: bytes, old_host: bytes, new_host: bytes):
    host = b'Host: '
    pos = request.find(host)

    pref, suf = request[:pos], request[pos:]

    suf = suf.replace(PreprocessingHost(old_host), PreprocessingHost(new_host), 1)
    return pref + suf


def PreprocessingHost(hostname: bytes):
    temp = b'://'
    start = hostname.find(temp)
    if start != -1:
        hostname = hostname[start + len(temp):]

    end = hostname.find(b'/')

    if end != -1:
        hostname = hostname[:end]
    return hostname


def GetTarget(receive: bytes):
    target = receive[receive.find(b'/') + 1: receive.find(b"HTTP/1.1")]
    return target.strip()

def GetHost(receive: bytes):
    host = b'Host: '
    start = receive.find(host) + len(host)
    end = receive.find(b'\r\n', start)
    if noise: print('???\n', start, end, receive)
    return receive[start: end]

def GetRealHostAndRequest(target: bytes):
    temp = b'://'
    pos = target.find(temp)
    pref = b''
    if pos != -1:
        pref = target[: pos + len(temp)]
        suf = target[pos + len(temp): ]
    else:
        suf = target
    pos_bs = suf.find(b'/')
    if pos_bs == -1:
        return pref + suf, b''
    else:
        return pref + suf[:pos_bs], suf[pos_bs:]
    
def SetTarget(receive: bytes, new_target: bytes):
    if len(new_target) == 0:
        new_target = b'/'
    old_target = GetTarget(receive)
    if len(old_target) == 0:
        old_target = b'/'

    if new_target == b'?gws_rd=ssl':
        new_target = b'/' 
    if new_target[0] != (b'/')[0]:
        new_target = b'/' + new_target

    if noise: print("Old target: ", old_target)
    if noise: print("New target: ", new_target)
    result = receive.replace(old_target, new_target, 1)

    first_bs = result.find(b'/')
    if first_bs + 1 == result.find(b'/', first_bs + 1):
        result = result[:first_bs] + result[first_bs + 1:]
        if noise: print("Update")
    if noise: print("Result: ", result)
    return result
    
def GetRequest(receive: bytes, my_name: bytes):
    if noise: print("\nMy name ", my_name)
    real_host, real_request = GetRealHostAndRequest(GetTarget(receive))

    if noise: print("Real host: ", real_host)
    if noise: print("Real request: ", real_request)

    drop_target = SetTarget(receive, real_request)
    return drop_target.replace(my_name, PreprocessingHost(real_host))

def ReceiveHolder(local_socket: socket.socket):
    local_socket.settimeout(1)

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
            if noise: print("Unknow error ", e)
            break
    return response


def CheckInCache(request: bytes, cache_name):
    if noise: print("---\n", request)
    host, target = map(BytesToStr, (GetHost(request), GetTarget(request)))
    with open(cache_name, 'r') as cache:
        while 1:
            known_host, known_target, answer = cache.readline(), cache.readline(), cache.readline()

            known_host = known_host.strip()
            known_target = known_target.strip()
            if len(known_host) == 0 or len(known_target) == 0:
                return b''
            if known_host == host and known_target == target:
                return StrToBytes(answer)
            else:
                if noise: print("Have host: \n", known_host)
                if noise: print("Need host: \n", host)

                if noise: print("Have target: \n", known_target)
                if noise: print("Need target: \n", target)


def OneRequestHandler(request_socket: socket.socket, addr, black_list: set, cache_path: str):

    cache = open(cache_path, 'a')
    receive = ReceiveHolder(request_socket)
    host, port = request_socket.getsockname()    
    request = GetRequest(receive, (host + ":" + str(port)).encode())

    if noise: print("\nFake receive: ", receive)
    if noise: print("\nTarget", GetTarget(receive))
    if noise: print("\nRequest       ", request)

    if noise: print('\n', request)

    real_host, _ = GetRealHostAndRequest(GetTarget(receive))
    code = 404
    while True:
        if noise: print("Real_host: ", real_host)
        socket_for_real_request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_port = 80
        
        # cache_res = CheckInCache(request, cache_path)
        # if len(cache_res) > 0:
        #     # real_receive = cache_res
        #     if noise: print("Has found in cache")
        #     # break

        if IsHTTPS(real_host):
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            socket_for_real_request = context.wrap_socket(socket_for_real_request, server_hostname=PreprocessingHost(real_host))
            target_port = 443
            if noise: print("Ask https")
        try:
            socket_for_real_request.connect((PreprocessingHost(real_host), target_port))
        except:
            if noise: print('\n\n\n\n\n')
            new_host = ''
            new_host = servers_stack[-1]
            request = ReplaceHost(request, real_host, new_host)
            request = SetTarget(request, real_host + b'/' + GetTarget(request))
            if noise: print("Update host to ", new_host)
            real_host = new_host
            if noise: print("New request:\n", request)
            continue

        socket_for_real_request.send(request)

        real_receive = ReceiveHolder(socket_for_real_request)

        if noise: print("Receive:\n", real_receive)
        if noise: print(f"Code: '{GetCode(real_receive)}'")

        code = GetCode(real_receive)
        if code == 404 or code == -1:
            request_socket.sendall(kErrorHttp)
            break

        if 300 <= code < 400:
            new_host = GetLocation(real_receive)
            if noise: print('\n\n\n\n\n')
            if noise: print("Old host: ", real_host)
            if noise: print("New host: ", new_host)
            request = ReplaceHost(request, real_host, new_host)
            request = SetTarget(request, GetRealHostAndRequest(new_host)[1])
            
            socket_for_real_request.close()
            real_host = new_host
            if noise: print("New request:\n", request)
            continue

        if code >= 400 or 200 <= code < 300:
            break


    if code == 200:
        servers_stack.append(DropTarget(real_host))

        if not cache is None:
            if noise: print("!!!\n", request)
            host, target = map(BytesToStr, (GetHost(request), GetTarget(request)))
            cache.write(host + '\n')
            cache.write(target + '\n')

            cache.write(BytesToStr(real_receive) + '\n')
            cache.close()

    if CheckIsBlock(real_host, black_list):
        request_socket.sendall(kErrorHttp)
        if noise: print("Server in black list")
        request_socket.close()
        return
    request_socket.sendall(real_receive)
    if noise: print(real_receive)
    request_socket.close()
    if noise: print(servers_stack)
    if noise: print("\nEndl with code: ", code)

def CheckIsBlock(target, black_list):

    for bad_site in black_list:
        if bad_site in target:
            return True
    return False

def Main(port, bl_path, cache_path):

    has_cache = True
    has_bl = True

    black_list = set()

    try:
        black_list_file = open(bl_path, 'r')

        while 1:
            site = black_list_file.readline()
            if len(site) == 0:
                break
            black_list.add(site[:-1].encode())
    except:
        has_bl = False

    cache = None

    server_name = '127.0.0.1'
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while 1:
        try:
            host_socket.bind((server_name, port))
            break
        except:
            port += 1
    print(f"Server work on {server_name}:{port}")
    host_socket.listen(10)

    cnt_question = -1
    while True:
        request_socket, addr = host_socket.accept()
        OneRequestHandler(request_socket, addr, black_list, cache_path)
        if noise: print("End work")
        cnt_question -= 1
        if cnt_question == 0:
            break
    
    host_socket.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('port', type=int)
    parser.add_argument('--black_list', type=str, default="black_list.txt")
    parser.add_argument('--cache', type=str, default="cache.txt")
    parser.add_argument("--noise", action="store_true")
    args = parser.parse_args()

    if args.noise:
        noise = True
    
    Main(args.port, args.black_list, args.cache)