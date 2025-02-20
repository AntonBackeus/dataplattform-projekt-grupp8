from quixstreams import Application
from constants import (
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from quixstreams.sinks.community.postgresql import PostgreSQLSink

# import json


def extract_coin_data(message):
    try:
        latest_ordi_data = message.get("ordi_data", {})
        latest_ordi_quote = latest_ordi_data["quote"]["USD"]
        latest_rates = message.get("rates", {})

        crypto_data = {
            "id": latest_ordi_data["id"],
            "name": latest_ordi_data["name"],
            "symbol": latest_ordi_data["symbol"],
            "max_supply": latest_ordi_data["max_supply"],
            "circul_supply": latest_ordi_data["circulating_supply"],
        }

        price_data = {
            "crypto_id": latest_ordi_data["id"],
            "price_usd": round(latest_ordi_quote["price"], 3),
            "price_sek": round(latest_ordi_quote["price"] * latest_rates["SEK"], 2),
            "price_nok": round(latest_ordi_quote["price"] * latest_rates["NOK"], 2),
            "price_dkk": round(latest_ordi_quote["price"] * latest_rates["DKK"], 2),
            "price_eur": round(latest_ordi_quote["price"] * latest_rates["EUR"], 2),
            "price_isk": round(latest_ordi_quote["price"] * latest_rates["ISK"], 2),
        }

        return {"crypto": crypto_data, "price": price_data}

    except Exception as e:
        print(f"Error while processing data: {e}")


def create_postgres_sink(table_name):
    sink = PostgreSQLSink(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DBNAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        table_name=table_name,
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

    # use the transformation function that returns an object with two keys: "crypto" and "price"
    sdf = sdf.apply(extract_coin_data)
    sdf.update(lambda message: print(message))

    # create two PostgreSQL sinks for different tables
    postgres_sink_crypto = create_postgres_sink("crypto")  # table with constant data
    postgres_sink_price = create_postgres_sink("price")  # table with changing data

    # divide the data into two separate dataframes
    crypto_df = sdf.apply(lambda message: message["crypto"])
    price_df = sdf.apply(lambda message: message["price"])

    # save the data into the appropriate tables
    crypto_df.sink(postgres_sink_crypto)
    price_df.sink(postgres_sink_price)

    app.run()


if __name__ == "__main__":
    main()
