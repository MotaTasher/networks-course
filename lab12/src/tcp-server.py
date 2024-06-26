import socket
import threading
import tkinter as tk
from tkinter import messagebox
import time

class TCPServer:
    def __init__(self, root):
        self.root = root
        self.root.title("Получатель TCP")

        self.label_ip = tk.Label(root, text="Ввод IP:")
        self.label_ip.pack()
        self.entry_ip = tk.Entry(root)
        self.entry_ip.pack()
        self.entry_ip.insert(0, "127.0.0.1")

        self.label_port = tk.Label(root, text="Выбор порта для получения:")
        self.label_port.pack()
        self.entry_port = tk.Entry(root)
        self.entry_port.pack()
        self.entry_port.insert(0, "8080")

        self.label_speed = tk.Label(root, text="Скорость передачи:")
        self.label_speed.pack()
        self.speed_var = tk.StringVar()
        self.speed_label = tk.Label(root, textvariable=self.speed_var)
        self.speed_label.pack()

        self.label_packets = tk.Label(root, text="Число полученных пакетов:")
        self.label_packets.pack()
        self.packets_var = tk.StringVar()
        self.packets_label = tk.Label(root, textvariable=self.packets_var)
        self.packets_label.pack()

        self.button = tk.Button(root, text="Получить", command=self.start_server)
        self.button.pack()

    def start_server(self):
        ip = self.entry_ip.get()
        port = int(self.entry_port.get())
        server_thread = threading.Thread(target=self.run_server, args=(ip, port))
        server_thread.start()

    def run_server(self, ip, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip, port))
        server_socket.listen(1)
        conn, addr = server_socket.accept()

        received_data = ""
        packet_count = 0
        start_time = None

        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode('utf-8')
            if start_time is None:
                start_time = float(data.split('|')[0])
            if packet_count is None:
                start_time = int(data.split('|')[1])

            received_data += data.split('|')[2]

        end_time = time.time()
        duration = end_time - start_time
        speed = len(received_data) / duration
        self.speed_var.set(f"{speed:.2f} B/S")
        self.packets_var.set(f"{packet_count} / {packet_count}")

        conn.close()
        server_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    server = TCPServer(root)
    root.mainloop()
