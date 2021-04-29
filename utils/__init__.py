import datetime
import requests

try:
    import ujson as json
except ImportError:
    import json


def get_date(delta: int):
    """Build a date object with given day offset"""
    date = datetime.datetime.now()
    if delta is not None:
        offset = datetime.timedelta(days=delta)
        date = date + offset
    date = date.strftime("%A %-m/%-d")
    return date


def get_JSON(URL):
    "Request JSON from API server"
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
