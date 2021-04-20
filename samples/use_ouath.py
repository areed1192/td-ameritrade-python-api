from td.credentials import TdCredentials
from td.client import TdAmeritradeClient
from configparser import ConfigParser

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
    redirect_uri=redirect_uri
)

td_credentials.to_credential_file(
    file_path='config/td_credentials.json'
)

# Initalize the `TdAmeritradeClient`
td_client = TdAmeritradeClient(
    credentials=td_credentials
)