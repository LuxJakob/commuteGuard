import os
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List

import requests


def fetch_traffic(start: int, destination: str, time_hour: str, departure_time: str) -> str:
    # fetch data from api
    current_date = datetime.now().strftime('%y%m%d')
    response = requests.get(
        _build_request_url(start, current_date, time_hour),
        headers=_get_request_headers()
    )

    # parse response
    root = ET.fromstring(response.text)

    departure_date_time = f'{current_date}{departure_time}'

    matching_trains = []
    for s in root.findall('s'):
        dp = s.find('dp')
        if dp is not None and dp.get('pt') == departure_date_time:
            route = dp.get('ppth', '')
            if destination in route:
                matching_trains.append(s)

    formatted_time = f'{departure_time[:2]}:{departure_time[2:]}'

    if matching_trains:
        return _parse_matching_trains(matching_trains, destination, formatted_time)

    return f'No trains found to {destination} at {formatted_time}'


def _build_request_url(start: int, current_date: str, time_hour: str) -> str:
    url_base = 'https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/plan/'
    url_parameters = f'{start}/{current_date}/{time_hour}'
    url = url_base + url_parameters
    return url


def _get_request_headers() -> dict:
    db_client_id = os.environ.get('DB_CLIENT_ID')
    db_client_api_key = os.environ.get('DB_CLIENT_API_KEY')
    headers = {
        'DB-Api-Key': db_client_api_key,
        'DB-Client-Id': db_client_id,
        'accept': 'application/xml'
    }

    return headers

def _parse_matching_trains(matching_trains: List, destination: str, formatted_time: str) -> str:
    result = [f"""<p>Dein Zug nach {destination}, um {formatted_time} Uhr:</p>"""]
    for train in matching_trains:
        tl = train.find('tl')
        dp = train.find('dp')

        train_number = tl.get('n', 'Unknown')
        train_type = tl.get('c', 'Unknown')
        platform = dp.get('pp', 'Unknown')
        route = dp.get('ppth', '').replace('|', ' → ')

        result.extend([
            """<p>\nTrain:</p>""",
            f"""<p>Type/Number: {train_type} {train_number}</p>""",
            f"""<p>Platform: {platform}</p>""",
            f"""<p>Route: {route}</p>"""
        ])
    return '\n'.join(result)
