import os
from typing import List

import requests


def fetch_weather() -> str:
    # fetch data from api
    api_token_weather = os.environ.get('API_TOKEN_WEATHER')

    base_url = 'https://api.weatherapi.com/v1/forecast.json'
    stuttgart_coordinates = 'q=48.78275%2C9.182583'
    scope = 'days=1'

    url = f'{base_url}?{stuttgart_coordinates}&{scope}&key={api_token_weather}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        return f'Error {response.status_code}: Weather API is broken! \n{response.text}'

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

    html_weather = _parse_json_weather(hourly_data)

    return html_weather


def _parse_json_weather(hourly_data: List) -> str:
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
        row_class = 'rain' if entry['will_it_rain'] else 'no-rain'

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
