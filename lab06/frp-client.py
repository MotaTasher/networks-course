from ftplib import FTP
import tkinter as tk
from tkinter import messagebox

def FTPConnect(host, port, username, password):
    ftp = FTP()
    ftp.connect(host, port)
    ftp.login(username, password)
    return ftp

def GoToFolder(ftp, foldername):
    ftp.cwd(foldername)

def CreateFolder(ftp, foldername):
    ftp.mkd(foldername)

def DeleteFile(ftp, filename):
    ftp.delete(filename)

def DeleteFolder(ftp, foldername):
    ftp.rmd(foldername)

def ListFiles(ftp):
    files = []
    ftp.dir(files.append)
    return files

def DownloadFile(ftp, filename):
    with open(filename, 'wb') as file:
        ftp.retrbinary('RETR ' + filename, file.write)

def UploadFile(ftp, filename):
    with open(filename, 'rb') as file:
        ftp.storbinary('STOR ' + filename, file)

def main():
    host = '127.0.0.1'
    port = 21
    username = 'testuser'
    password = 'motaisupov8'

    ftp = FTPConnect(host, port, username, password)

    print("Available actions")
    print("\nДоступные действие:")
    print("exit")
    print("ls")
    print("download file (get)")
    print("upload file (send)")
    print("cd foldername")
    print("mkdir foldername")
    print("rm foldername")
    print("remove filename")
    print("touch filename")

    while True:
        print()
        inp = input()
        action = inp.split()
        command = action[0]
        if len(action) > 1:
            args = inp[inp.find(' ') + 1: ]

        if command == 'exit':
            break
        elif command == 'ls':
            files = ListFiles(ftp)
            for file in files:
                print(file)
        elif command == 'download' or command == 'get':
            filename = args
            DownloadFile(ftp, filename)
            print(f"Файл '{filename}' успешно скачан.")
        elif command == 'upload' or command == 'send':
            filename = args
            UploadFile(ftp, filename)
            print(f"Файл '{filename}' успешно загружен на сервер.")
        elif command == 'cd':
            foldername = args
            GoToFolder(ftp, foldername)
        elif command == 'mkdir':
            foldername = args
            CreateFolder(ftp, foldername)

        elif command == 'rm':
            foldername = args
            DeleteFolder(ftp, foldername)

        elif command == 'remove':
            filename = args
            DeleteFile(ftp, filename)
        else:
            print("Unknown command")

    ftp.quit()
    print("Connection close")

if __name__ == "__main__":
    main()
