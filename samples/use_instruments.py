from pprint import pprint
from configparser import ConfigParser
from td.credentials import TdCredentials
from td.client import TdAmeritradeClient
from td.utils.enums import Projections

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

# Initialize the `Instruments` service.
instruments_service = td_client.instruments()

# Search for a symbol.
pprint(
    instruments_service.search_instruments(
        symbol='MSFT',
        projection='symbol-search'
    )
)

# Search for fundamental data.
pprint(
    instruments_service.search_instruments(
        symbol='MSFT',
        projection=Projections.Fundamental
    )
)

# Search for a symbol using regular expression.
pprint(
    instruments_service.search_instruments(
        symbol='MS*',
        projection=Projections.SymbolRegex
    )
)

# Search for companies using description key words.
pprint(
    instruments_service.search_instruments(
        symbol='Technology',
        projection=Projections.DescriptionSearch
    )
)

# Search for companies using description regular expression.
pprint(
    instruments_service.search_instruments(
        symbol='[Quantum Computing]',
        projection=Projections.DescriptionRegex
    )
)

# Get an Insturment by using their CUSIP.
pprint(
    instruments_service.get_instrument(
        cusip='617446448'
    )
)
