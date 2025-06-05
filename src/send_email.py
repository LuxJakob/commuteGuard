import os
import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests


def send_email(timestamp: datetime) -> None:
    port = 465
    smtp_server = "smtp.gmail.com"
    username = os.environ.get('MAIL_USERNAME')
    pwd_secure = os.environ.get('MAIL_PASSWORD')

    if username is None or pwd_secure is None:
        print("Error: MAIL_USERNAME or MAIL_PASSWORD is not set.")
        return

    if timestamp.hour < 12:
        subject = 'You better work b*tch!'
        message_body = create_message_body_morning()
    else:
        subject = 'The end is near..'
        message_body = create_message_body_evening()

    email_message = MIMEMultipart()
    email_message['From'] = username
    email_message['To'] = username
    email_message['Subject'] = subject

    email_message.attach(MIMEText(message_body, 'html'))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(username, pwd_secure)
            server.sendmail(username, username, email_message.as_string())
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication error: {e}")
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}")
    except Exception as e:  # pylint: disable=W0718
        print(f"An unexpected error occurred: {e}") # Fallback


def create_message_body_morning() -> str:
    message_body = ""

    message_body += fetch_weather()
    message_body += fetch_traffic('start', 'destination')
    return message_body


def create_message_body_evening() -> str:
    message_body = ""

    message_body += fetch_weather()
    message_body += fetch_traffic('start', 'destination')
    return message_body


def body_default(message_body: str) -> str:
    message_body += '''
        <div style="font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: left; font-size: 18px; 
        color: #333; padding: 20px; border-radius: 8px;">
            <p>Do it for her! ❤️</p>
        </div>'''
    return message_body

def fetch_weather() -> str:
    return 'weather'


def fetch_traffic(start: str, destination: str) -> str:
    return 'traffic'
