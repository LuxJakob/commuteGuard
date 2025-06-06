import os
import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

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
    message_body += link_back_weather()

    message_body += fetch_traffic('start', 'destination')
    return message_body


def create_message_body_evening() -> str:
    message_body = ""

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
    # fetch data from api
    api_token_weather = os.environ.get('API_TOKEN_WEATHER')

    base_url = 'https://api.weatherapi.com/v1/forecast.json'
    stuttgart_coordinates = 'q=48.78275%2C9.182583'
    scope = 'days=1'

    response = requests.get(
        base_url + '?' + stuttgart_coordinates + '&' + scope + '&key=' + api_token_weather
    )

    if response.status_code == 200:
        data = response.json()
    else:
        return parse_json_weather([])

    # parse response
    hourly_data = []

    forecast_day = data['forecast']['forecastday'][0]
    hours = forecast_day['hour']

    for hour in hours:
        time_str = hour['time']
        hour_num = int(time_str.split(' ')[1].split(':')[0])

        if 7 <= hour_num <= 20:
            hourly_data.append({
                'time': time_str,
                'temp_c': hour['temp_c'],
                'feelslike_c': hour['feelslike_c'],
                'will_it_rain': hour['will_it_rain'],
                'chance_of_rain': hour['chance_of_rain'],
                'precip_mm': hour['precip_mm'],
                'condition': hour['condition']['text']
            })

    html_weather = parse_json_weather(hourly_data)

    return html_weather


def parse_json_weather(hourly_data: List) -> str:
    html_table = """
    <table>
        <thead>
            <tr>
                <th>Time</th>
                <th>Temperature (°C)</th>
                <th>Feels Like (°C)</th>
                <th>Chance of Rain</th>
                <th>Precipitation (mm)</th>
                <th>Condition</th>
            </tr>
        </thead>
        <tbody>
    """

    for entry in hourly_data:
        row_class = "rain" if entry['will_it_rain'] else "no-rain"

        html_table += f"""
                <tr class="{row_class}">
                    <td>{entry['time']}</td>
                    <td>{entry['temp_c']}</td>
                    <td>{entry['feelslike_c']}</td>
                    <td>{entry['chance_of_rain']}%</td>
                    <td>{entry['precip_mm']}</td>
                    <td>{entry['condition'].strip()}</td>
                </tr>
        """

    html_table += """
            </tbody>
        </table>
    """

    return html_table


def link_back_weather() -> str:
    return """
    <a href="https://www.weatherapi.com/" title="Free Weather API">
    <img src='//cdn.weatherapi.com/v4/images/weatherapi_logo.png' alt="Weather data by WeatherAPI.com" border="0">
    </a>
    """


def fetch_traffic(start: str, destination: str) -> str:
    return start + destination
