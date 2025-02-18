from quixstreams import Application
from constants import COINMARKET_API, RATE_URL
from pprint import pprint
from connect_api import get_latest_coin_data, get_latest_rates
import time
import json


def main():
    app = Application(broker_address="localhost:9092", consumer_group="coin_group")
    coins_topic = app.topic(name="coins", value_serializer="json")

    with app.get_producer() as producer:
        while True:
            coin_latest = get_latest_coin_data(
                "ORDI",
                COINMARKET_API,
                "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest",
            )
            rate_latest = get_latest_rates(RATE_URL)

            kafka_message = coins_topic.serialize(
                key=coin_latest["symbol"],
                value={"coin_data": coin_latest, "rate_data": rate_latest},
            )

            print(
                f"produce event with key = {kafka_message.key}, price =  {coin_latest['quote']['USD']['price']}, price i SEK = {coin_latest['quote']['USD']['price'] * rate_latest['results']['SEK']}"
            )

            producer.produce(
                topic=coins_topic.name, key=kafka_message.key, value=kafka_message.value
            )

            time.sleep(10)


if __name__ == "__main__":
    # coin_data = get_latest_coin_data()
    # pprint(coin_data)

    main()
