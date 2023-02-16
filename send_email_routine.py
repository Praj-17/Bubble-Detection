import datetime
import time
import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Define the function you want to run
def send_email():
    print ('sending email')
    recipients = ['pwaykos1@gmail.com', 'iitmshanker@gmail.com']
   # recipients = ['iitmshanker@gmail.com','snr@durvah.com'] #, 'Mounesh.Panchal@unilever.com','Subir.Misra@unilever.com', 'Sabarinath.Mani@unilever.com', 'Pranay.Dugyala@unilever.com' ]
    attachment_path = 'record.csv'
    sender = "iitmshanker@gmail.com"
    password = "euzqwftrrwvmfvfv"
    subject = "Daily Update | Zerofill Transactions"
    body = "Hi, \n\nPlease find the attached file consisting the transactions on Zerofill ZF002."

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="csv")
        attachment.add_header('Content-Disposition', 'attachment', filename="record.csv")
        msg.attach(attachment)
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        smtp_server.close()
    except Exception as e:
        print("Exception", e)
  

def run_scheduler():
    schedule.every().day.at("17:31").do(send_email)
    #schedule.every(2).minutes.do(send_email)
    

    print ('done')
    while True:
        schedule.run_pending()
        time.sleep(2)


