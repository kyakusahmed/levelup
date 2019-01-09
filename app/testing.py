import smtplib

host = "smtp.gmail.com"
port = 587
username = "kyakuluahmed@gmail.com"
password = "CHRISTINE77"
from_email = username
to_list = ["kyakusahmed@outlook.com"]

email_conn = smtplib.SMTP(host, port)
email_conn.ehlo()
email_conn.starttls()
email_conn.login(username, password)
email_conn.sendmail(from_email, to_list, "your redflag status was updated to")

