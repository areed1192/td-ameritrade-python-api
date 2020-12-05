from pprint import pprint
from configparser import ConfigParser
from td.client import TDClient

# Grab configuration values.
config = ConfigParser()
config.read('config/config.ini')

CLIENT_ID = config.get('main', 'CLIENT_ID')
REDIRECT_URI = config.get('main', 'REDIRECT_URI')
JSON_PATH = config.get('main', 'JSON_PATH')
ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

# Create a new session
TDSession = TDClient(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=JSON_PATH,
    account_number=ACCOUNT_NUMBER
)

# Login to the session
TDSession.login()

pprint(TDSession.get_quotes(instruments=['MSFT']))