import tkinter as tk
from tkinter import messagebox
from ftplib import FTP

def CreateFTPConnect():
    global ftp
    host = host_entry.get()
    port = int(port_entry.get())
    username = username_entry.get()
    password = password_entry.get()

    try:
        ftp = FTP()
        ftp.connect(host, port)
        ftp.login(username, password)
        messagebox.showinfo("Success", "Connected to FTP server successfully!")
        ListFiles(ftp)
        return ftp
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to FTP server: {e}")
        return None
    

def SelectInList():
    selected_index = file_listbox.curselection()
    if selected_index:
        if selected_index[0] == 0:
            return '..'
        selected_row = file_listbox.get(selected_index[0])
        ind = selected_row.find(selected_row.split()[3])
        selected_item = selected_row[ind:]
        print(f"Selected item: {selected_item}")
        return selected_item
    return ""

def GetName():
    box = filename_entry.get()
    if len(box) > 0:
        return box
    else:
        return SelectInList()

def ListFiles(ftp):
    files = []
    ftp.dir(files.append)
    file_listbox.delete(0, tk.END)
    file_listbox.insert(tk.END, ' ' * 22 + ':  go up')
    for file in files:
        words = file.split()
        time = words[7]
        file_listbox.insert(tk.END, f'{words[5]:4s} {words[6]:2s} {time:5s}: {file[file.find(time) + len(time):]}')

def CreateEmptyFile(ftp):
    filename = GetName()
    try:
        ftp.storbinary('STOR ' + filename, tk.NONE)
        messagebox.showinfo("Success", f"Empty file '{filename}' created successfully!")
        ListFiles(ftp)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create empty file: {e}")

def RetrieveFile(ftp):
    filename = GetName()
    print("'" + filename + "'")
    try:
        with open(filename, 'wb') as file:
            ftp.retrbinary('RETR ' + filename, file.write)
        messagebox.showinfo("Success", f"File '{filename}' retrieved successfully!")
        ListFiles(ftp)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve file: {e}")

def UploadFile(ftp):
    filename = GetName()
    try:
        with open(filename, 'rb') as file:
            ftp.storbinary('STOR ' + filename, file)
        messagebox.showinfo("Success", f"File '{filename}' uploaded successfully!")
        ListFiles(ftp)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to upload file: {e}")

def DeleteFile(ftp):
    filename = GetName()
    try:
        ftp.delete(filename)
        messagebox.showinfo("Success", f"File '{filename}' deleted successfully!")
        ListFiles(ftp)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete file: {e}")

def FTPConnect(host, port, username, password):
    ftp = FTP()
    ftp.connect(host, port)
    ftp.login(username, password)
    return ftp


def GoToFolder(ftp):
    foldername = GetName()

    try:
        ftp.cwd(foldername)
        ListFiles(ftp)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to go in folder: {e}")

def CreateFolder(ftp):

    foldername = GetName()

    try:
        ftp.mkd(foldername)
        ListFiles(ftp)
    except Exception as e:
        messagebox.showerror("Error", f"Failed in create folder: {e}")

def main():
    global host_entry, port_entry, username_entry, password_entry
    global ftp, filename_entry, file_listbox

    root = tk.Tk()
    root.title("FTP Client")

    row_ind = 0
    host_label = tk.Label(root, text="Host:")
    host_label.grid(row=row_ind, column=0, sticky=tk.W)
    host_entry = tk.Entry(root)
    host_entry.grid(row=row_ind, column=1)

    row_ind += 1
    port_label = tk.Label(root, text="Port:")
    port_label.grid(row=row_ind, column=0, sticky=tk.W)
    port_entry = tk.Entry(root)
    port_entry.grid(row=row_ind, column=1)

    row_ind += 1
    username_label = tk.Label(root, text="Username:")
    username_label.grid(row=row_ind, column=0, sticky=tk.W)
    username_entry = tk.Entry(root)
    username_entry.grid(row=row_ind, column=1)

    row_ind += 1
    password_label = tk.Label(root, text="Password:")
    password_label.grid(row=row_ind, column=0, sticky=tk.W)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=row_ind, column=1)

    row_ind += 1
    connect_button = tk.Button(root, text="Connect", command=CreateFTPConnect)
    connect_button.grid(row=row_ind, column=0, columnspan=2, pady=5)

    row_ind += 1
    file_label = tk.Label(root, text="Filename:")
    file_label.grid(row=row_ind, column=0, sticky=tk.W)
    filename_entry = tk.Entry(root)
    filename_entry.grid(row=row_ind, column=1)

    row_ind += 1
    create_button = tk.Button(root, text="Go", command=lambda: GoToFolder(ftp))
    create_button.grid(row=row_ind, column=0, pady=4)

    retrieve_button = tk.Button(root, text="Retrieve", command=lambda: RetrieveFile(ftp))
    retrieve_button.grid(row=row_ind, column=1, pady=4)


    row_ind += 1
    upload_button = tk.Button(root, text="Upload", command=lambda: UploadFile(ftp))
    upload_button.grid(row=row_ind, column=0, pady=5)

    delete_button = tk.Button(root, text="Delete", command=lambda: DeleteFile(ftp))
    delete_button.grid(row=row_ind, column=1, pady=5)

    row_ind += 1
    retrieve_button = tk.Button(root, text="Create Folder", command=lambda: CreateFolder(ftp))
    retrieve_button.grid(row=row_ind, column=0, pady=4)

    row_ind += 1
    file_listbox = tk.Listbox(root, width=50)
    file_listbox.grid(row=row_ind, column=0, columnspan=2)



    root.mainloop()

if __name__ == "__main__":
    global ftp
    ftp = None
    main()
 