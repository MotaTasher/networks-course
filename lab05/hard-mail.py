import socket
import base64
import time
import ssl

endmsg = '\r\n.\r\n'

bound_msg = f"""\
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="boundary"

--boundary
Content-Type: text/plain

"""

middle_msg = f"""\


--boundary
Content-Type: image/jpeg
Content-Disposition: attachment; filename="image.jpg"
Content-Transfer-Encoding: base64

"""

receive_size = 1024
def ReceiveHolder(local_socket: socket.socket, timeout: float=1):
    local_socket.settimeout(timeout)
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
            print("Unknow error ", e)
            break
    return response

def GetBadNewsString(code: int):
    return f'Code is note {code} - bad news: connect troubles'


def read_image(path: str):
    with open(path, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode('utf-8')
    return encoded_image

def GetImgData(path: str) -> str:
    header = ("""Content-Type: image/png"""
    """Content-Disposition: attachment;"""
    """Content-Transfer-Encoding: base64""")

    data = read_image(path)

    tailer = "\n--boundary--"

    return header + data + tailer


def read_image(filename):
    with open(filename, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode('utf-8')
    return encoded_image

def SendMail(my_address, target_address, smtp_server,
             port, password, subject,  msg, img_path) -> None:

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((smtp_server, port))
    recv = ReceiveHolder(client_socket).decode()

    print("Success connect:" + recv)
    if recv[:3] != '220':
        print(GetBadNewsString(220))

    heloCommand = f'EHLO {client_socket.getsockname()[0]}\r\n'
    client_socket.send(heloCommand.encode())
    recv = ReceiveHolder(client_socket).decode()
    print("Message after EHLO command:" + recv)

    if recv[:3] != '250':
        print(GetBadNewsString(250))

    login_str = base64.b64encode(("\x00" + my_address + "\x00" + password).encode())
    authMsg = "AUTH PLAIN ".encode() + login_str + b'\r\n'
    client_socket.send(authMsg)
    recv = ReceiveHolder(client_socket).decode()
    print("After AUTH PLAIN:" + recv)

    mailFrom = f"MAIL FROM:<{my_address}>\r\n"
    client_socket.send(mailFrom.encode())
    recv = ReceiveHolder(client_socket).decode()
    print("After MAIL FROM command: " + recv)

    rcptTo = f"RCPT TO:<{target_address}>\r\n"
    client_socket.send(rcptTo.encode())
    recv = ReceiveHolder(client_socket).decode()
    print("After RCPT TO command: " + recv)

    client_socket.send(b"DATA\r\n")
    recv = ReceiveHolder(client_socket).decode()
    print("After DATA command: " + recv)

    header = (f"""From: {my_address}\r\n"""
              f"""To: {target_address}\r\n"""
              f"""Subject: {subject}\r\n\r\n""")
    # msg = header + msg
    
    msg = header + bound_msg + msg + middle_msg
    msg += read_image("images/Jokes.png")
    msg += "\n--boundary--"
    print(msg)

    client_socket.send(msg.encode())
    client_socket.send(endmsg.encode())
    recv = ReceiveHolder(client_socket).decode()
    print("Response after sending message body:" + recv)
    quit = "QUIT\r\n"
    client_socket.send(quit.encode())
    recv = ReceiveHolder(client_socket).decode()
    print(recv)
    client_socket.close()

smtp_server = 'smtp.rambler.ru'
port = 587

target_address = 'MotaTasher@yandex.ru'
my_address = 'matvei.isupov.education@rambler.ru'
password = 'xxxxxxxx' # а вы думали тут пароль от моей почты увидеть? Не-а, не на того напали
msg = (f"""Попытка +1""")
subject = "Письмо от самого сасного человека" 
img_path = "images/Jokes.png"

SendMail(my_address=my_address,
         target_address=target_address,
         smtp_server=smtp_server,
         port=port,
         password=password,
         subject=subject,
         msg=msg,
         img_path=img_path)