from quixstreams import Application
from constants import (
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from quixstreams.sinks.community.postgresql import PostgreSQLSink
import json


def extract_coin_data(message):
    try:
        latest_ordi_data = message.get("ordi_data", {})
        latest_rates = message.get("rates", {})

        return {
            "name": message.get("name"),
            "price_usd": latest_ordi_data.get("quote", {})
            .get("USD", {})
            .get("price", 0),
            "price_sek": latest_rates["SEK"],
            # "volume": latest_ordi_data["volume_24h"],
            # "updated": message["coin_data"]["last_updated"],
        }
    except Exception as e:
        print(f"Error while processing data: {e}")


def create_postgres_sink():
    sink = PostgreSQLSink(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DBNAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        table_name="ordi",
        schema_auto_update=True,
    )
    return sink


def main():
    app = Application(
        broker_address="localhost:9092",
        consumer_group="coin_group",
        auto_offset_reset="latest",
    )

    coins_topic = app.topic(name="coins", value_deserializer="json")
    sdf = app.dataframe(topic=coins_topic)

    # transformations

    sdf = sdf.apply(extract_coin_data)
    sdf.update(lambda message: print(message))

    # sink to postgres

    postgres_sink = create_postgres_sink()
    sdf.sink(postgres_sink)

    app.run()


if __name__ == "__main__":
    main()
