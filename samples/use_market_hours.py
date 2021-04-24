from pprint import pprint
from configparser import ConfigParser
from td.credentials import TdCredentials
from td.client import TdAmeritradeClient
from td.utils.enums import Markets
from datetime import datetime

# Initialize the Parser.
config = ConfigParser()

# Read the file.
config.read('config/config.ini')

# Get the specified credentials.
client_id = config.get('main', 'client_id')
redirect_uri = config.get('main', 'redirect_uri')

# Intialize our `Crednetials` object.
td_credentials = TdCredentials(
    client_id=client_id,
    redirect_uri=redirect_uri,
    credential_file='config/td_credentials.json'
)

# Initalize the `TdAmeritradeClient`
td_client = TdAmeritradeClient(
    credentials=td_credentials
)

# Initialize the `MarketHours` service.
market_hours_service = td_client.market_hours()

# Grab the market hours
pprint(
    market_hours_service.get_multiple_market_hours(
        markets=['EQUITY', Markets.Bond],
        date=datetime.now()
    )
)

# Grab the hours for a specific market.
pprint(
    market_hours_service.get_market_hours(
        market='EQUITY',
        date=datetime.now()
    )
)
