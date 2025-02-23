# dataplattform-projekt-grupp8
 
## Crypto Data Platform
This project retrieves real-time cryptocurrency data (via CoinMarketCap Pro API) and exchange rates (via FastForex API) and processes them using Kafka, PostgreSQL, and a Streamlit dashboard.
 
## Table of Contents
1. Overview
2. Architecture
3. Components
4. Getting Started
5. Usage
6. Project Structure
 
# 1. Overview
This project consists of three main parts:
 
    1. Producer: Fetches cryptocurrency data from CoinMarketCap and exchange rates from FastForex, then sends messages to a Kafka topic.
    2. Consumer: Consumes messages from Kafka, processes the data, and writes it into PostgreSQL.
    3. Dashboard: A Streamlit-based web application that visualizes the data (price, volume, exchange rates, etc.) in near real-time.
Key Data Sources
    - CoinMarketCap Pro API: Provides up-to-date crypto prices and metadata.
    - FastForex API: Delivers exchange rates for various currencies (e.g., SEK, NOK, EUR, DKK, ISK).
 
 
# 2. Architecture
 
 
 
        +---------------------+
        |   CoinMarketCap     |
        | (Crypto Data)       |
        +----------+----------+
                              |
                             
                +---------------------+
                |    FastForex       |
                | (Exchange Rates)   |
                +----------+----------+
                              |
            v   v
        +-----------+     +--------+     +--------------+
        | Producer  | --> | Kafka  | --> |  Consumer    |
        +-----------+     +--------+     +--------------+
                                        |   PostgreSQL  |
                                        +--------------+
                                                |
                                                v
                                        +---------------+
                                        |   Dashboard   |
                                        | (Streamlit)   |
                                        +---------------+
 
### Producer:
- Periodically fetches crypto data (e.g., ORDI, XRP) from CoinMarketCap.
- Fetches exchange rates from FastForex.
- Publishes these combined data as JSON to the Kafka topic (coins).
 
### Kafka:
Acts as a message broker that stores incoming messages from the producer and makes them available to the consumer.
 
### Consumer:
Reads messages from the coins topic.
Extracts and parses crypto data, splitting it into “crypto” (static info) and “price” (dynamic info).
Writes the parsed data into two PostgreSQL tables (crypto and price).
 
### Dashboard (Streamlit):
Connects to PostgreSQL, queries the tables, and displays the latest data (prices, changes, volumes, etc.).
Allows you to filter by date, currency, and specific coin.
 
 
# 3. Components
### Producer (producer.py)
    Fetches:
        Crypto data from CoinMarketCap:
            e.g., get_latest_coin_data("ORDI", API_KEY, COINMARKET_URL)
        Exchange rates from FastForex:
            e.g., get_latest_rates(RATE_URL)
    Serializes the combined data into JSON and sends it to Kafka.
 
### Consumer (consumer.py)
    Consumes JSON messages from Kafka.
    Uses a function extract_coin_data(message) that:
        Splits data into “crypto” (ID, name, symbol, max supply, etc.) and “price” (USD, SEK, NOK, etc.).
    Writes each portion to two different PostgreSQL tables (crypto, price) via PostgreSQLSink.
 
### Dashboard (dashboard.py or app.py)
    A Streamlit application that:
        Connects to PostgreSQL via SQLAlchemy.
        Allows the user to select a cryptocurrency and target currency.
        Displays the latest data (st.dataframe()) and time-series charts (via matplotlib or plotly).
        Updates periodically (using streamlit_autorefresh or manual refresh).
 
### connect_api.py
    Helper file with functions for HTTP requests to CoinMarketCap and FastForex.
 
### constants.py
    Stores configuration constants (e.g., COINMARKET_API, RATE_URL, POSTGRES_HOST, etc.).
 
 
# 4. Getting Started
 
#### Prerequisites
    Python 3.9+
    Kafka (e.g., via Docker)
    PostgreSQL (e.g., via Docker)
    CoinMarketCap API Key (register at pro.coinmarketcap.com)
    FastForex API Key (register at fastforex.readme.io)
 
#### Installation
    Clone this repository:
        git clone https://github.com/AntonBackeus/dataplattform-projekt-grupp8.git
        cd crypto-data-platform
    Create and activate a virtual environment:
        python -m venv .venv
        source .venv/bin/activate  # On Linux/Mac
        .venv\Scripts\activate     # On Windows
    Install requirements:
        pip install -r requirements.txt
 
#### Environment Variables
    Set your API keys and PostgreSQL/Kafka info in constants.py or as environment variables:
 
        COINMARKET_API = "YOUR_CMC_KEY"
        COINMARKET_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
 
        RATE_URL = "YOUR_FASTFOREX_API_KEY"
 
        POSTGRES_USER = "postgres"
        POSTGRES_PASSWORD = "your password"
        POSTGRES_DBNAME = "coin_db"
        POSTGRES_HOST = "localhost"
        POSTGRES_PORT = 5432
 
 
# 5. Usage
### 1. Start Kafka and PostgreSQL
If using Docker Compose, ensure you have a docker-compose.yml that spins up Kafka and PostgreSQL:
 
    docker-compose up -d
 
Make sure Kafka is reachable at localhost:9092 and PostgreSQL at localhost:5432.
 
### 2. Run the Producer
 
    python producer.py
 
Fetches data from CoinMarketCap and FastForex every 60 seconds.
Sends JSON messages to Kafka topic coins.
 
### 3. Run the Consumer
 
    python consumer.py
 
Subscribes to the coins topic.
Parses each message and writes to PostgreSQL (crypto and price tables).
 
### 4. Run the Dashboard
 
    streamlit run dashboard.py
 
Connects to PostgreSQL.
Displays the latest crypto data in real time.
Provides charts and metrics (24h change, volume, etc.).
 
 
# 6. Project Structure
 
crypto-data-platform/
├── .venv
├── explorations
   ├── eda.ipynb
├── kafka_data
├──src
    ├── producer.py        # Kafka Producer
    ├── consumer.py        # Kafka Consumer
    ├── dashboard.py       # Streamlit dashboard
    ├── connect_api.py     # Helper functions for API requests
    ├── constants.py       # Configuration constants      
├── state
├── .env
├── .gitignore
├── docker-compose.yml
├── README.md              # Project documentation
├── requirements.txt