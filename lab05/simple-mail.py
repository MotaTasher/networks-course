
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtp_server = 'smtp.rambler.ru'
port = 587  
sender_email = 'matvei.isupov.education@rambler.ru'
# receiver_email = 'mot12131415@gmail.ru'
receiver_email = 'MotaTasher@yandex.ru'
password = 'Bbm-LLUrY85S8E@'
# textfile = 'text.txt'
textfile_html = 'text.html'

with open(textfile_html, 'rb') as fp:
    message = fp.read().decode()

context = ssl.create_default_context()


msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
subject = f'Context from {textfile_html}'
msg['Subject'] = subject
# body = MIMEText(message, 'plain')
body = MIMEText(message, 'html')

msg.attach(body)

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port, timeout=5) as server:
    print("success start ssl")
    server.ehlo()
    server.starttls()
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()

print("success sended")
