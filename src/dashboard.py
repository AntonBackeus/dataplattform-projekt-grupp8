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
)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


connection_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

count = st_autorefresh(interval=10 * 1000, limit=100, key="data_refresh")

engine = create_engine(connection_string)


def format_large_numbers(value):
    """Omvandlar stora tal till K, M, B-format"""
    try:
        value = float(value)
        if value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.1f}B"
        elif value >= 1_000_000:
            return f"{value / 1_000_000:.1f}M"
        elif value >= 1_000:
            return f"{value / 1_000:.1f}K"
        else:
            return f"{value:.2f}"
    except (ValueError, TypeError):
        return value  # Om det inte är ett tal, returnera som det är


def load_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        df = df.set_index("timestamp")
    return df


def layout():

    with st.sidebar:
        st.markdown("## Settings")
        selected_coin = st.radio("Choose currency", COINS, horizontal=True)
        selected_currency = st.selectbox("Choose currency", CURRENCIES)

        st.markdown("---")

        st.markdown("### ℹ️ API Information")
        st.write("Data is fetched from:")
        st.markdown("- 🌍 [CoinMarketCap API](https://coinmarketcap.com/api/)")
        st.markdown("- 💱 [FastForex API](https://www.fastforex.io/)")

    df = load_data(
        f"""
    SELECT 
        price.timestamp, 
        price.price_{selected_currency.lower()},
        crypto.name as coin, 
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


    st.subheader("Latest Metrics")

    latest_data = df.sort_index(ascending=False).groupby("coin").head(1)

    cols = st.columns(len(latest_data.index))
    for i, (idx, row) in enumerate(latest_data.iterrows()):
        with cols[i]:
            st.markdown(f"**{row['coin']}**")

            st.metric(
                label=f"Price ({selected_currency})",
                value=f"{row[f'price_{selected_currency.lower()}']:.2f}",
                delta=f"{row['percent_change_24h']:.2f} % (24h)",
            )

    st.markdown(f"# {selected_coin} data")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Percent Change 1h", f"{round(df['percent_change_1h'].iloc[-1], 2)}%")
    col2.metric(
        "Percent Change 24h", f"{round(df['percent_change_24h'].iloc[-1], 2)}%"
    )
    col3.metric(
        "Percent Change 7 days", f"{round(df['percent_change_7d'].iloc[-1], 2)}%"
    )
    col4.metric("Coin Market Cap rank", int(df["cmc_rank"].iloc[-1]))

    display_df = df.head(5).style.format(
        {
            "max_supply": format_large_numbers,
            "circul_supply": format_large_numbers,
            f"price_{selected_currency.lower()}": format_large_numbers,
        }
    )

    st.dataframe(display_df)

    st.markdown(f"## {selected_coin} latest price in {selected_currency}")

    df = df.sort_index()

    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots()

    ax.plot(
        df.index,
        df[f"price_{selected_currency.lower()}"],
        color="green",
    )
    ax.set_title(f"Price {selected_currency}", fontsize=16)
    ax.set_ylabel(f"Price ({selected_currency})", fontsize=12)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d (%H:%M)"))
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Summary Statistics")

    grouped = df.groupby("coin")[f"price_{selected_currency.lower()}"].agg(
        ["mean", "median", "std", "min", "max"]
    )
    st.table(grouped.style.format("{:.2f}"))


if __name__ == "__main__":
    layout()
