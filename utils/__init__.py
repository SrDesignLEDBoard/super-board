import datetime
import requests
from typing import Dict

try:
    import ujson as json
except ImportError:
    import json


def get_date(delta: int) -> str:
    """Build a date object with given day offset.

    Function is necessary to check games for NHL since the API returns games for entire week.
    Get the date as a string in a particular format used in JSON returned from NHL API.

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
    """Request JSON from API server.

    GET requests to URL provided to the function and return a python dict.
    APIs like NHL have a wrapper so handles that as well.

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
    else:
        response = json.loads(response.text)
    return response
