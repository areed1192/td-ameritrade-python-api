from td.oauth import TdAmeritradeOauth
from configparser import ConfigParser

# Initialize the Parser.
config = ConfigParser()

# Read the file.
config.read('config/config.ini')

# Get the specified credentials.
client_id = config.get('main', 'client_id')
redirect_uri = config.get('main', 'redirect_uri')

# Initialize the oAuthClient.
oauth_client = TdAmeritradeOauth(
    client_id=client_id,
    redirect_uri=redirect_uri
)

print(oauth_client.from_workflow())