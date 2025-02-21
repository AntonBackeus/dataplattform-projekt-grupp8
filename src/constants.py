import os
from dotenv import load_dotenv

load_dotenv()


COINMARKET_API = os.getenv("COINMARKET_API")
COINMARKET_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DBNAME = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

CURRENCIES = ["USD", "EUR", "SEK", "NOK", "DKK", "ISK"]

TIMES = ["1h", "24h", "7d"]

RATE_API = os.getenv("RATE_API")
RATE_URL = f"https://api.fastforex.io/fetch-multi?from=USD&to=SEK%2C%20EUR%2C%20DKK%2C%20NOK%2C%20ISK&api_key={RATE_API}"
