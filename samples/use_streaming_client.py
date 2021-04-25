from pprint import pprint
from configparser import ConfigParser
from td.credentials import TdCredentials
from td.client import TdAmeritradeClient
from td.utils.enums import LevelOneQuotes
from td.utils.enums import LevelOneOptions
from td.utils.enums import LevelOneFutures

# Initialize the Parser.
config = ConfigParser()

# Read the file.
config.read('config/config.ini')

# Get the specified credentials.
client_id = config.get('main', 'client_id')
redirect_uri = config.get('main', 'redirect_uri')
account_number = config.get('main', 'account_number')

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

# Initialize the `StreamingApiClient` service.
streaming_api_service = td_client.streaming_api_client()

# Let's see what services we have access to.
streaming_services = streaming_api_service.services()

# Set the Quality of Service.
streaming_services.quality_of_service(
    qos_level='1'
)

# Grab level one quotes.
streaming_services.level_one_quotes(
    symbols=['MSFT'],
    fields=LevelOneQuotes.All
)

# Grab level one options quotes.
streaming_services.level_one_options(
    symbols=['MSFT_043021C120'],
    fields=LevelOneOptions.All
)

# Grab level one futures quotes.
streaming_services.level_one_futures(
    symbols=['/ESM4', '/ES'],
    fields=LevelOneFutures.All
)

# Start Streaming.
streaming_api_service.open_stream()
