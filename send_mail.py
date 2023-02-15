import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(recipients, attachment_path):
    sender = ""
    password = ""
    subject = "Daily_mail"
    body = "Hi there, \n\nThis is a test email sent from Python."

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="csv")
        attachment.add_header('Content-Disposition', 'attachment', filename=r"C:\Users\ASUS\Downloads\Data (2)\timeline.csv")
        msg.attach(attachment)

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.close()

if __name__ == '__main__':
    # Schedule the email to be sent every day at 10 AM
    send_time = "19:15"
    schedule.every().day.at(send_time).do(send_email, recipients=["pwaykos1@gmail.com"], attachment_path=r"C:\Users\ASUS\Downloads\Data (2)\timeline.csv")

    # Keep the program running to allow scheduled tasks to be executed
    while True:
        print('Running the loop')
        schedule.run_pending()
        time.sleep(1)