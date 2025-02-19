from quixstreams import Application
from constants import COINMARKET_API, COINMARKET_URL, RATE_URL
from connect_api import get_latest_coin_data, get_latest_rates
import time


def main():
    app = Application(broker_address="localhost:9092", consumer_group="coin_group")
    coins_topic = app.topic(name="coins", value_serializer="json")

    with app.get_producer() as producer:
        while True:
            try:
                ordi_latest = get_latest_coin_data(
                    "ORDI", COINMARKET_API, COINMARKET_URL
                )
                rate_latest = get_latest_rates(RATE_URL)

                crypto_data = {
                    "ordi_data": ordi_latest,
                    "rates": rate_latest,
                }

                kafka_message = coins_topic.serialize(
                    key=ordi_latest["symbol"], value=crypto_data
                )

                producer.produce(
                    topic=coins_topic.name,
                    key=kafka_message.key,
                    value=kafka_message.value,
                )

                print(
                    f"Data sent to Kafka: Cryptocurrency - {ordi_latest['name']} with price {ordi_latest['quote']['USD']['price']:.4f} USD/ {ordi_latest['quote']['USD']['price'] * rate_latest['SEK']:.2f} SEK"
                )

                time.sleep(30)

            except Exception as e:
                print(f"Error sending data {e}")


if __name__ == "__main__":

    main()
