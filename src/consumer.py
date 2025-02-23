from quixstreams import Application
from constants import (
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from quixstreams.sinks.community.postgresql import PostgreSQLSink


def parse_currency(currency, rates):
    try:
        quote_usd = currency.get("quote", {}).get("USD", {})

        crypto_data = {
            "id": currency.get("id"),
            "name": currency.get("name"),
            "symbol": currency.get("symbol"),
            "max_supply": currency.get("max_supply"),
            "circul_supply": currency.get("circulating_supply"),
            "cmc_rank": currency.get("cmc_rank"),
        }

        price_data = {
            "crypto_id": currency.get("id"),
            "price_usd": quote_usd.get("price"),
            "price_sek": quote_usd.get("price") * rates.get("SEK"),
            "price_nok": quote_usd.get("price") * rates.get("NOK"),
            "price_dkk": quote_usd.get("price") * rates.get("DKK"),
            "price_eur": quote_usd.get("price") * rates.get("EUR"),
            "price_isk": quote_usd.get("price") * rates.get("ISK"),
            "percent_change_1h": quote_usd.get("percent_change_1h"),
            "percent_change_24h": quote_usd.get("percent_change_24h"),
            "percent_change_7d": quote_usd.get("percent_change_7d"),
        }

        return [crypto_data, price_data]

    except Exception as e:
        print(f"Error while parsing data: {e}")


def extract_coin_data(message):
    try:
        ordi_raw = message.get("ordi_data", {})
        xrp_raw = message.get("xrp_data", {})
        rates = message.get("rates", {})

        ordi_crypto, ordi_price = parse_currency(ordi_raw, rates)
        xrp_crypto, xrp_price = parse_currency(xrp_raw, rates)

        return {
            "ordi": {"crypto": ordi_crypto, "price": ordi_price},
            "xrp": {"crypto": xrp_crypto, "price": xrp_price},
        }

    except Exception as e:
        print(f"Error while processing data: {e}")
        return {"ordi": {"crypto": {}, "price": {}}, "xrp": {"crypto": {}, "price": {}}}


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
    # --------------------------------------------------------------------------------------------------------
    # divide the data into two separate dataframes
    ordi_crypto_df = sdf.apply(lambda message: message["ordi"]["crypto"])
    ordi_price_df = sdf.apply(lambda message: message["ordi"]["price"])

    xrp_crypto_df = sdf.apply(lambda message: message["xrp"]["crypto"])
    xrp_price_df = sdf.apply(lambda message: message["xrp"]["price"])

    # save the data into the appropriate tables
    ordi_crypto_df.sink(postgres_sink_crypto)
    ordi_price_df.sink(postgres_sink_price)

    xrp_crypto_df.sink(postgres_sink_crypto)
    xrp_price_df.sink(postgres_sink_price)

    app.run()


if __name__ == "__main__":
    main()
