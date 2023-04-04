import datetime
import time
import sched
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Define the function you want to run
def send_email():
    recipients = recipients = ['pwaykos1@gmail.com', 'iitmshanker@gmail.com']
    attachment_path = 'record.csv'
    sender = "code.freaks2022@gmail.com"
    password = "gshszhjsunzhdnxl"
    subject = "Daily_mail"
    body = "Hi there, \n\nThis is a test email sent from Python."

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="csv")
        attachment.add_header('Content-Disposition', 'attachment', filename=r"record.csv")
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
    scheduler.enter(delay=1*60, priority=1, action=send_email,argument= (recipients, attachment_path))
        

# Define the time you want the function to run every day
hour = 10  # 12 PM
minute = 30  # 0 minutes

# Create a scheduler object
scheduler = sched.scheduler(time.time, time.sleep)

# Define a function to run the scheduler
def run_scheduler(recipients, attachment_path):
    # Calculate the next run time for the function
    print("Schedular Running")
    now = datetime.datetime.now()
    next_run_time = datetime.datetime(now.year, now.month, now.day, hour, minute)
    print("Next mail set at", {next_run_time})
    if next_run_time < now:
        next_run_time += datetime.timedelta(days=1)

    # Schedule the function to run at the next run time
    scheduler.enterabs(next_run_time.timestamp(), 1, send_email, (recipients, attachment_path))

    # Run the scheduler
    scheduler.run()

# Call the function to run the scheduler
recipients = ['pwaykos1@gmail.com', 'iitmshanker@gmail.com']
# run_scheduler(recipients, 'record.csv')

from apscheduler.schedulers.background import BackgroundScheduler

print("Starting")
scheduler = BackgroundScheduler()
scheduler.add_job(send_email, 'cron', hour =23, minute = 6)

scheduler.start()
print("completed..")