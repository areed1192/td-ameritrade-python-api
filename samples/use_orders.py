from pprint import pprint
from configparser import ConfigParser
from td.credentials import TdCredentials
from td.client import TdAmeritradeClient
from td.enums import OrderStatus

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

# Initialize the `Orders` service.
orders_service = td_client.orders()

# Query all our orders for a specific account.
pprint(
    orders_service.get_orders_by_path(
        account_id=account_number,
        order_status=OrderStatus.Filled
    )
)

# Query all our orders.
pprint(
    orders_service.get_orders_by_query()
)
