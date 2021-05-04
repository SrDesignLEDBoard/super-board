import datetime
import requests
from typing import Dict

try:
    import ujson as json
except ImportError:
    import json


def get_date(delta: int) -> str:
    """Build a date object with given day offset

    Args:
        delta (int): Offset

    Returns:
        str: Date in the format "%Weekday %-month%-dayofmonth"
    """
    date = datetime.datetime.now()
    if delta is not None:
        offset = datetime.timedelta(days=delta)
        date = date + offset
    date = date.strftime("%A %-m/%-d")
    return date


def get_JSON(URL: str) -> Dict:
    """Request JSON from API server

    Args:
        URL (str): [description]

    Returns:
        Dict: JSON object that was parsed into a python dictionary
    """
    response = requests.get(URL)
    # the live.nhle.com/ API has a wrapper, so remove it
    if 'nhle' in URL:
        response = response.text.replace('loadScoreboard(', '')
        response = response.replace(')', '')
        response = json.loads(response)
    # elif 'mlb' in URL or 'espn' in URL:
    #     response = json.loads(response.text)
    else:
        response = json.loads(response.text)
    return response
