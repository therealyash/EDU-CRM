from email.message import EmailMessage
import ssl
import smtplib
import time
from datetime import datetime



# Email Details -
sender_email = 'varadpathak011@gmail.com'
password = 'mvfr koeq nkwn kisd'
receiver_email = 'varadpathak007@gmail.com'
subject = 'Email Automation with Timing & Date'
body = """
Hello Varad,

Testing Email 1 - Yashraj from Pycharm.

Kind Regards,
Yashraj Limkar
"""


def send_email():
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, receiver_email, em.as_string())
        print(f"Email sent successfully at {datetime.now()}")


def schedule_email(send_date, send_time):
    send_datetime_str = f"{send_date} {send_time}"
    send_datetime = datetime.strptime(send_datetime_str, "%Y-%m-%d %H:%M:%S")

    print(f"Email scheduled for: {send_datetime}")

    while True:
        current_time = datetime.now()
        if current_time >= send_datetime:
            send_email()
            break
        time.sleep(30)

schedule_date = "2025-01-17"  # YYYY-MM-DD
schedule_time = "02:16:00"    # HH:MM:SS
schedule_email(schedule_date, schedule_time)

