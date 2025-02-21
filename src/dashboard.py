import streamlit as st
from streamlit_autorefresh import st_autorefresh
from sqlalchemy import create_engine
import pandas as pd
from constants import (
    POSTGRES_USER,
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    CURRENCIES,
    COINS,
    TIMES,
)


from charts import line_chart
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


connection_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

count = st_autorefresh(interval=10 * 1000, limit=100, key="data_refresh")

engine = create_engine(connection_string)


def load_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        df = df.set_index("timestamp")
    return df


def layout():

    # df = load_data(
    #     f"""
    #         SELECT * FROM price;
    #     """
    # )

    # df2 = load_data(
    #     f"""
    #         SELECT * FROM crypto;
    #     """
    # )

    selected_coin = st.radio("Choose currency", COINS, horizontal=True)
    selected_currency = st.selectbox("Choose currency", CURRENCIES)

    df3 = load_data(
        f"""
    SELECT 
        price.timestamp, 
        price.price_{selected_currency.lower()},
        crypto.name, 
        crypto.max_supply, 
        crypto.circul_supply,
        percent_change_1h,
        percent_change_24h,
        percent_change_7d,
        cmc_rank

    FROM price
    INNER JOIN crypto 
    ON price.crypto_id = crypto.id
    WHERE crypto.name = '{selected_coin}';
    """
    )

    # df4 = load_data(
    #     f"""
    #         SELECT * FROM price;
    #     """
    # )

    st.markdown(f"# {selected_coin} data")

    with st.container():
        st.info(
            "Dessa nyckeltal visar procentuell förändring och marknadsrank för den senaste perioden."
        )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Percent Change 1h", f"{round(df3['percent_change_1h'].iloc[-1], 2)}%")
    col2.metric(
        "Percent Change 24h", f"{round(df3['percent_change_24h'].iloc[-1], 2)}%"
    )
    col3.metric(
        "Percent Change 7 days", f"{round(df3['percent_change_7d'].iloc[-1], 2)}%"
    )
    col4.metric("Coin Market Cap rank", int(df3["cmc_rank"].iloc[-1]))

    # st.dataframe(df4.tail(5))
    st.dataframe(df3.tail(5))

    st.markdown(f"## {selected_coin} latest price in {selected_currency}")

    price_chart = line_chart(
        x=df3.index,
        y=df3[f"price_{selected_currency.lower()}"],
        title=f"Price {selected_coin} ({selected_currency})",
    )

    st.pyplot(price_chart, bbox_inches="tight")


if __name__ == "__main__":
    layout()


# import streamlit as st
# from streamlit_autorefresh import st_autorefresh
# from sqlalchemy import create_engine
# import pandas as pd
# from constants import (
#     POSTGRES_USER,
#     POSTGRES_DBNAME,
#     POSTGRES_HOST,
#     POSTGRES_PASSWORD,
#     POSTGRES_PORT,
#     CURRENCIES,
#     TIMES
# )


# from charts import line_chart
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates


# connection_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

# count = st_autorefresh(interval=10 * 1000, limit=100, key="data_refresh")

# engine = create_engine(connection_string)


# def load_data(query):
#     with engine.connect() as conn:
#         df = pd.read_sql(query, conn)
#         df = df.set_index("timestamp")
#     return df


# def layout():

#     df = load_data(
#         f"""
#             SELECT * FROM price;
#         """
#     )

#     df2 = load_data(
#         f"""
#             SELECT * FROM crypto;
#         """
#     )

#     df3 = load_data(
#         f"""
#     SELECT
#         price.timestamp,
#         price.price_usd,
#         price.price_sek,
#         price_nok,
#         price_dkk,
#         price_isk,
#         price_eur,
#         crypto.name,
#         crypto.max_supply,
#         crypto.circul_supply
#     FROM price
#     INNER JOIN crypto
#     ON price.crypto_id = crypto.id;
#     """
#     )

#     df4 = load_data(
#         f"""
#             SELECT * FROM price;
#         """
#     )

#     df5 = load_data(
#         f"""
#             SELECT * FROM ordi;
#         """
#     )

#     st.markdown("# Ordi data")

#     st.info("Här kommer info")

#     col1, col2, col3, col4 = st.columns(4)

#     col1.metric("Percent Change 1h", f"{round(df['percent_change_1h'].iloc[-1], 2)}%")
#     col2.metric("Percent Change 24h", f"{round(df['percent_change_24h'].iloc[-1], 2)}%")
#     col3.metric("Percent Change 7 days", f"{round(df['percent_change_7d'].iloc[-1], 2)}")
#     col4.metric("Coin Market Cap rank", int(df2["cmc_rank"].iloc[-1]))
#     # col3.metric("Volume 24h",)
#     # col4.metric("Market Cap",)


#     st.dataframe(df4.tail(5))
#     st.dataframe(df3.tail(5))
#     st.dataframe(df5.tail(5))

#     selected_currency = st.selectbox("Choose currency", CURRENCIES)
#     st.markdown(f"## Ordi latest price in {selected_currency}")

#     price_chart = line_chart(
#         x=df.index,
#         y=df[f"price_{selected_currency.lower()}"],
#         title=f"Price {selected_currency}",
#     )

#     st.pyplot(price_chart, bbox_inches="tight")


#     selected_timeframe = st.selectbox("Choose timeframe", TIMES)
#     time_chart = line_chart(
#         x = df.index,
#         y = df[f"percent_change_{selected_timeframe}"],
#         title = f"Percent Change Last {selected_timeframe}"
#     )

#     st.pyplot(time_chart, bbox_inches="tight")


#     fig, ax = plt.subplots()
#     ax.plot(df.index, df[f"percent_change_{selected_timeframe}"])

#     # Ställ in formatet på datumetiketterna
#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:%M'))  # Ex: "Feb 21\n01:00"

#     # Rotera och justera datumetiketterna för bättre läsbarhet
#     plt.xticks(rotation=45)
#     ax.set_title(f"Percent Change Last {selected_timeframe}")

#     st.pyplot(fig, bbox_inches="tight")

# if __name__ == "__main__":
#     layout()
