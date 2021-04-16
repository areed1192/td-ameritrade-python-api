from pprint import pprint
from configparser import ConfigParser
from td.credentials import TdCredentials
from td.client import TdAmeritradeClient

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

# Initialize the Quotes service.
quote_service = td_client.quotes()

# Grab a single quote.
pprint(
    quote_service.get_quote(instrument='AAPL')
)

# Grab multiple quotes.
pprint(
    quote_service.get_quotes(instruments=['AAPL', 'SQ'])
)
