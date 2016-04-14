import smtplib
from email.mime.text import MIMEText


def send(sender, recipient, subj, body):
    msg = MIMEText(body)
    msg["Subject"] = subj
    msg["From"] = sender
    msg["To"] = recipient

    server = smtplib.SMTP("127.0.0.1")

    flag = False
    try:
        server.sendmail(sender, recipient, msg.as_string())
        flag = True
    except Exception as e:
        print(e.message)

    server.quit()
    return flag

