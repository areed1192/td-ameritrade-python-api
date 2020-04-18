import pprint
import config.credentials as config

from datetime import datetime
from datetime import timedelta
from td.client import TDClient

# Create a new session
TDSession = TDClient(
    account_number=config.ACCOUNT_NUMBER,
    client_id=config.CLIENT_ID,
    redirect_uri=config.REDIRECT_URI,
    credentials_path=config.JSON_PATH
)

# Login to the session
TDSession.login()

# `get_quotes` endpoint with single value. Should not return an error.
quotes_single = TDSession.get_quotes(instruments=['SQ'])

# `get_quotes` endpoint with multiple values. Should not return an error.
quotes_multi = TDSession.get_quotes(instruments=['SQ', 'MSFT'])

# `search_instruments` Endpoint
instrument_search_data = TDSession.search_instruments(symbol='MSFT', projection='symbol-search')

# `get_movers` Endpoint
movers_data = TDSession.get_movers(market = '$DJI', direction = 'up', change ='value')

# `get_instruments` Endpoint
get_instrument_data = TDSession.get_instruments(cusip= '594918104')

# `get_market_hours` Endpoint with multiple values
market_hours_multi = TDSession.get_market_hours(markets = ['EQUITY','FOREX'], date = datetime.today().isoformat())

# `get_accounts` Endpoint with single values
accounts_data_single = TDSession.get_accounts(account = config.ACCOUNT_NUMBER,  fields = ['orders'])

# `get_accounts` Endpoint with single values
accounts_data_multi = TDSession.get_accounts(account = 'all',  fields = ['orders'])

# `get_transactions` Endpoint. Should not return an error
transaction_data_multi = TDSession.get_transactions(account = config.ACCOUNT_NUMBER, transaction_type = 'ALL')

# `get_preferences` endpoint. Should not return an error
preference_data = TDSession.get_preferences(account = config.ACCOUNT_NUMBER)

# `get_subscription_keys` endpoint. Should not return an error
streamer_keys = TDSession.get_streamer_subscription_keys(accounts = [config.ACCOUNT_NUMBER])

# `get_user_ principals` endpoint. Should not return an error.
prinicpals_data = TDSession.get_user_principals(fields = ['preferences','surrogateIds'])

# # `get_transactions` Endpoint with single values
# transaction_data_single = TDSession.get_transactions(transaction_id= 'YOUR_TRANSACTION_ID')