import os
import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from src.weather_api import fetch_weather
from src.db_api import fetch_traffic


def send_email(timestamp: datetime) -> None:
    port = 465
    smtp_server = 'smtp.gmail.com'
    username = os.environ.get('MAIL_USERNAME')
    pwd_secure = os.environ.get('MAIL_PASSWORD')

    if username is None or pwd_secure is None:
        print('Error: MAIL_USERNAME or MAIL_PASSWORD is not set.')
        return

    if timestamp.hour < 12:
        subject = 'You better work b*tch!'
        message_body = create_message_body_morning()
    else:
        subject = 'The end is near..'
        message_body = create_message_body_evening()

    message_body += footer()

    email_message = MIMEMultipart()
    email_message['From'] = username
    email_message['To'] = username
    email_message['Subject'] = subject

    with open('images/DB_logo_red_filled_200px_rgb.png', 'rb') as img_file:
        img = MIMEImage(img_file.read())
        img.add_header('Content-ID', '<db_logo>')
        email_message.attach(img)

    email_message.attach(MIMEText(message_body, 'html'))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(username, pwd_secure)
            server.sendmail(username, username, email_message.as_string())
        print('Email sent successfully.')
    except smtplib.SMTPAuthenticationError as e:
        print(f'Authentication error: {e}')
    except smtplib.SMTPException as e:
        print(f'SMTP error: {e}')
    except Exception as e:  # pylint: disable=W0718
        print(f'An unexpected error occurred: {e}') # Fallback


def create_message_body_morning() -> str:
    message_body = ''

    message_body += fetch_weather()

    # Karlsruhe Hauptbahnhof IBNR - 8000191
    message_body += fetch_traffic(8000191, 'Stuttgart Hbf', '06', '0632')
    return message_body


def create_message_body_evening() -> str:
    message_body = ''

    # Stuttgart Hauptbahnhof IBNR - 8000096
    message_body += fetch_traffic(8000096, 'Karlsruhe Hbf', '16', '1658')
    return message_body


def footer() -> str:
    motivation = '''<br><br>
        <div style="font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: left; font-size: 18px; 
        color: #333; padding: 20px; border-radius: 8px;">
            <p>Do it for her! ❤️</p>
        </div><br><br>'''

    linking_back = """
            <table>
              <tr>
                <td>
                    <p>Powered by: </p>
                </td>
                <td width="10"></td>
                <td>
                  <a href="https://www.weatherapi.com/" title="Free Weather API">
                    <img src='https://cdn.weatherapi.com/v4/images/weatherapi_logo.png' alt="Weather data by WeatherAPI.com" border="0">
                  </a>
                </td>
                <td width="10"></td>
                <td>
                  <a href="https://www.bahn.de/" 
                    title="Mit den APIs der Deutschen Bahn neue Lösungen für die Mobilität von morgen entwickeln!">
                    <img src="cid:db_logo" border="0" style="width:60%; height:auto;"
                    alt="Data by https://developers.deutschebahn.com/" border="0">
                  </a>
                </td>
              </tr>
              <tr>
                <td colspan="5">
                  <br><br><br>
                </td>
              </tr>
            </table>
        """

    return motivation + linking_back
