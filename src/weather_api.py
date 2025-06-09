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
                'precip_mm': hour['precip_mm']
            })

    html_weather = _get_greeting(hourly_data)
    html_weather += _parse_json_weather(hourly_data)

    return html_weather


def _parse_json_weather(hourly_data: List) -> str:
    html_table = """
    <table style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr style="border: 1px solid #ddd; background-color: #f2f2f2;">
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Uhrzeit</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Temp (°C)</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Gefühlt (°C)</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Regen</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: right;">Niederschlag (mm)</th>
            </tr>
        </thead>
        <tbody>
    """

    for entry in hourly_data:
        row_class = 'rain' if entry['will_it_rain'] else 'no-rain'
        time_str = entry['time'].split(' ')[1][:5]

        html_table += f"""
                    <tr class="{row_class}" style="border: 1px solid #ddd;">
                        <td style="border: 1px solid #ddd; padding: 8px;">
                            {time_str}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">
                            {entry['temp_c']}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">
                            {entry['feelslike_c']}</td>
                        <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">
                            {entry['chance_of_rain']}%</td>
                        <td style="border: 1px solid #ddd; padding: 8px; text-align: right;">
                            {entry['precip_mm']}</td>
                    </tr>
                """

    html_table += """
            </tbody>
        </table>
        <br><br>
    """
    return html_table


def _get_greeting(hourly_data: List) -> str:
    max_temp = "N/A"
    max_felt_temp = "N/A"
    avg_precip_mm = "N/A"

    if hourly_data:
        max_temp = max(hour['temp_c'] for hour in hourly_data)
        max_felt_temp = max(hour['feelslike_c'] for hour in hourly_data)
        avg_precip_mm = sum(hour['precip_mm'] for hour in hourly_data) / len(hourly_data)

    greetings = f"""
        <p>Guten Morgen! 🥱</p>
        <p>Heute wird es bis zu {max_temp}°C geben! Gefühlt ca. {max_felt_temp}°C 🌡️.<p>
        <p>Ein durchschnittlicher Niederschlag von {avg_precip_mm} 🌧️</p>
        <br>
        """
    return greetings
