import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def sender(subject, message, from_email, to_emails, login_pwd):
    if isinstance(to_emails, list):
        to_email = ", ".join(to_emails)
    else:
        to_email = to_emails
    msg = MIMEMultipart()
    msg['From'] = from_email 
    msg['To'] = to_email  
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(from_email, login_pwd)
    text = msg.as_string()
    server.sendmail(from_email, to_emails, text)  
    server.quit()
file = open('config.json',encoding='utf-8')
config = json.load(file)
sender_mail = config['sender_email']
sender_pwd = config['sender_pwd']
    