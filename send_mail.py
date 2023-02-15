import smtplib
import datetime
import email
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import time

def send_email_with_attachment(recipients, subject, message_body, attachment_path, sender_email, sender_password):
   
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ", ".join(recipients)
    message['Subject'] = subject
    message.attach(MIMEText(message_body))
    
    attachment_file = open(attachment_path, 'rb')
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type = mime_type.split('/')
    attachment.set_payload(attachment_file.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
    message.attach(attachment)
    
    server.sendmail(sender_email, recipients, message.as_string())
    server.quit()

def send_daily_emails_with_attachment(recipients, subject, message, attachment_path, sender_email, sender_password):
    # Set the time for the daily email to be sent (10 AM)
    send_time = datetime.time(hour=10, minute=0)
    
    
    while True:
       
        current_time = datetime.datetime.now().time()
        
        if current_time.hour == send_time.hour and current_time.minute == send_time.minute:
           
            send_email_with_attachment(recipients, subject, message, attachment_path, sender_email, sender_password)
            
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            send_time = datetime.datetime.combine(tomorrow, send_time)
            time_diff = (send_time - datetime.datetime.now()).total_seconds()
            time.sleep(time_diff)

if __name__ == '__main__':
    recipients = ['xyz@gmail.com', 'abc@gmail.com', 'mno@gmail.com', 'fgh@gmail.com']
    subject = 'Daily Email with Attachment'
    message = 'Hello,\n\nThis is your daily email with attachment.'
    attachment_path = "hi.csv"
    sender_email = 'sender@gmail.com'
    sender_password = 'sender_pass'
    send_daily_emails_with_attachment(recipients, subject, message, attachment_path, sender_email, sender_password)

