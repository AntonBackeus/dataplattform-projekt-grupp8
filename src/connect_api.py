import json
from requests import Session

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