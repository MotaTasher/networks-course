import socket
import threading
import tkinter as tk
from tkinter import messagebox
import time

class UDPServer:
    def __init__(self, root):
        self.root = root
        self.root.title("Получатель UDP")

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
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((ip, port))

        received_data = ""
        packet_count = 0
        start_time = None
        packet_count = None
        
        while True:
            try:
                data, addr = server_socket.recvfrom(2048)
                server_socket.settimeout(1)
                if not data:
                    break
                data = data.decode('utf-8')
                if start_time is None:
                    start_time = float(data.split('|')[0])
                if packet_count is None:
                    packet_count = int(data.split('|')[1])

                received_data += data.split('|')[2]
            except:
                break

        end_time = time.time() - 1
        duration = end_time - start_time
        speed = len(received_data) / duration
        self.speed_var.set(f"{speed:.2f} B/S")
        self.packets_var.set(f"{packet_count} / {packet_count}")
        print(speed, packet_count, packet_count)

        server_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    server = UDPServer(root)
    root.mainloop()
