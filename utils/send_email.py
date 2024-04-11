import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(from_, to, msg_subject, msg_body, login_email, login_password):
    # create message
    msg = MIMEMultipart()
    msg['From'] = from_
    msg['To'] = to
    msg['Subject'] = msg_subject

    # add text to message
    msg.attach(MIMEText(msg_body))

    # setup gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = login_email
    smtp_password = login_password

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)


def send_emails(from_, to, bcc: list, msg_subject, msg_body, login_email, login_password):
    # send an email to multiple recipients/ccs
    bcc_emails = bcc    # BCC
    message = msg_body

    msg = MIMEText(message)
    msg['Subject'] = msg_subject
    msg['From'] = from_
    msg['To'] = to

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(login_email, login_password)
        server.sendmail(from_, [to] + bcc_emails, msg.as_string())

