import socket
import threading
import tkinter as tk
from tkinter import messagebox
import random
import time

class UDPClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Отправитель UDP")

        self.label_ip = tk.Label(root, text="Ввод IP адреса получателя:")
        self.label_ip.pack()
        self.entry_ip = tk.Entry(root)
        self.entry_ip.pack()
        self.entry_ip.insert(0, "127.0.0.1")

        self.label_port = tk.Label(root, text="Выбор порта отправки:")
        self.label_port.pack()
        self.entry_port = tk.Entry(root)
        self.entry_port.pack()
        self.entry_port.insert(0, "8080")

        self.label_packet_count = tk.Label(root, text="Ввод количества пакетов для отправки:")
        self.label_packet_count.pack()
        self.entry_packet_count = tk.Entry(root)
        self.entry_packet_count.pack()
        self.entry_packet_count.insert(0, "5")

        self.button = tk.Button(root, text="Отправить", command=self.start_client)
        self.button.pack()

    def start_client(self):
        ip = self.entry_ip.get()
        port = int(self.entry_port.get())
        packet_count = int(self.entry_packet_count.get())
        client_thread = threading.Thread(target=self.run_client, args=(ip, port, packet_count))
        client_thread.start()

    def run_client(self, ip, port, packet_count):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(packet_count):
            send_time = time.time()
            data = f"{send_time}|{packet_count}|{(b'Q' * 192).decode('utf-8')}"
            client_socket.sendto(data.encode('utf-8'), (ip, port))
            time.sleep(0.1)
        client_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    client = UDPClient(root)
    root.mainloop()
