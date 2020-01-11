import smtplib
from email.mime.text import MIMEText


def send_mail(guest, favorite, email):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '7728418512a6c8'
    password = '8f360fdf9cb5db'
    message = f"<p>Dear {guest}, </br>Thank you for your feedback! We are happy you enjoyed our wedding! And we are a lot more excited by the fact that your favorite thing was {favorite}<p>With love,</br>Alexu &Lavi"

    sender_email = "alexu_lavi@weddings.com"
    reciever_email = email
    msg = MIMEText(message, 'html')
    msg['Subject'] = "Wedding survey"
    msg['From'] = sender_email
    msg['To'] = reciever_email

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, reciever_email, msg.as_string())