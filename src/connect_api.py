import json
from requests import Session
import requests


# def get_latest_coin_data(target_symbol, API_KEY, API_URL):

#     parameters = {"symbol": target_symbol, "convert": "USD"}

#     headers = {
#         "Accepts": "application/json",
#         "X-CMC_PRO_API_KEY": API_KEY,
#     }

#     session = Session()
#     session.headers.update(headers)

#     response = session.get(API_URL, params=parameters)
#     return json.loads(response.text)["data"][target_symbol]


# def get_latest_rates(url):

#     headers = {"accept": "application/json"}
#     response = requests.get(url, headers=headers)
#     return json.loads(response.text)["results"]


def get_latest_coin_data(symbol, key, url):

    parameters = {"symbol": symbol, "convert": "USD"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": key,
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()

        data = response.json()
        if "data" in data and symbol in data["data"]:
            return data["data"][symbol]
        else:
            print(f"Error: Symbol {symbol} has not been found in API request")
            return None

    except requests.exceptions.RequestException as e:
        print(f"CoinMarketCap request error: {e}")
        return None


def get_latest_rates(url):

    try:
        response = requests.get(url, headers={"Accept": "application/json"})
        response.raise_for_status()

        data = response.json()
        if "results" in data:
            return data["results"]
        else:
            print("Error: Invalid response format from FastForex API")
            return None

    except requests.exceptions.RequestException as e:
        print(f"FastForex request error: {e}")
        return None
