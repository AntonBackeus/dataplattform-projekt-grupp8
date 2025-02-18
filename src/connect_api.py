import json
from requests import Session
import requests


def get_latest_coin_data(target_symbol, API_KEY, API_URL):

    parameters = {"symbol": target_symbol, "convert": "USD"}

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(API_URL, params=parameters)
    return json.loads(response.text)["data"][target_symbol]


def get_latest_rates(api):
    url = f"https://api.fastforex.io/fetch-multi?from=USD&to=SEK%2C%20EUR%2C%20DKK%2C%20NOK%2C%20ISK&api_key={api}"

    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)
