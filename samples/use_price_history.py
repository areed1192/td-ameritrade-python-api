from configparser import ConfigParser
from datetime import datetime
from datetime import timedelta
from td.credentials import TdCredentials
from td.client import TdAmeritradeClient
from td.utils.enums import PeriodType
from td.utils.enums import FrequencyType

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

# Initialize the `PriceHistory` service.
price_history_service = td_client.price_history()

# Grab the Price History, with enums.
price_history = price_history_service.get_price_history(
    symbol='MSFT',
    frequency_type=FrequencyType.Minute,
    frequency=1,
    period_type=PeriodType.Day,
    period=10,
    extended_hours_needed=False
)
# pprint(price_history)

# Grab the Price History, without enums.
price_history = price_history_service.get_price_history(
    symbol='MSFT',
    frequency_type='minute',
    frequency=1,
    period_type='day',
    period=10,
    extended_hours_needed=False
)

# The max look back period for minute data is 31 Days.
end_date = datetime.now()
start_date = datetime.now() - timedelta(seconds=60)

# Grab the Price History, custom time frame.
price_history = price_history_service.get_price_history(
    symbol='MSFT',
    frequency_type=FrequencyType.Minute,
    frequency=1,
    start_date=1628260200000,
    end_date=1628260220000,
    extended_hours_needed=False
)
print(price_history['candles'])
