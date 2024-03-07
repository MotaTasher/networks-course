import socket
import threading
import time
import json
import argparse

threads = {}
last_ind = 0

def OneSocketWorker(current_socket: socket.socket, addr, sem: threading.Semaphore):

    sem.acquire()
    print("Sem -1: ", sem._value)
    request_data = current_socket.recv(1024).decode()
    if not request_data:
        return
    
    global threads
    global last_ind
    if not addr[1] in threads:
        threads[addr[1]] = last_ind
        last_ind += 1
    
    file_requested = request_data.split()[1][1:]
    print("Hi from thread ", threads[addr[1]])
    try:
        with open(file_requested, 'rb') as file:
            response = b"HTTP/1.1 200 OK\n\n" + file.read()
    except FileNotFoundError:
        print(f"Thread {threads[addr[1]]} start sleeping")
        time.sleep(10)
        print(f"Thread {threads[addr[1]]} wake up")
        response = b"HTTP/1.1 404 Not Found\n\nFile not found"
    print("By from thread ", threads[addr[1]])
    
    current_socket.sendall(response)
    current_socket.close()
    sem.release()
    print("Sem +1: ", sem._value)



def Main(port: int, concurrency_level: int):

    start_time = time.time()
    host = ""
    start_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    start_socket.bind((host, port))

    print("socket binded to port", port)
    start_socket.listen(7)

    cnt_request = 0
    max_cnt_request = 20

    semaphore = threading.Semaphore(value=concurrency_level)
    while True:

        local_socket, addr = start_socket.accept()

        thread = threading.Thread(target=OneSocketWorker, args=(local_socket, addr, semaphore))
        cnt_request += 1
        thread.start()
        if cnt_request == max_cnt_request:
            break

    start_socket.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('port')
    parser.add_argument('concurrency_level')
    args = parser.parse_args()
    print(args.port)
    
    Main(int(args.port), int(args.concurrency_level))