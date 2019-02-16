import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_list, subject, body):

    email_address = "kyakuluahmed@gmail.com"
    email_password = "CHRISTINE77"

    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = to_list
    msg['Subject'] = subject

    body = body
    msg.attach(MIMEText(body, 'plain'))

    try:
        email_conn = smtplib.SMTP('smtp.gmail.com', 587)
        email_conn.starttls()
        email_conn.login(email_address, email_password)
        msg_to_send = msg.as_string()
        email_conn.sendmail(email_address, to_list,  msg_to_send)
        email_conn.quit()
        return "email sent"
    except:
        return "email not sent"
   