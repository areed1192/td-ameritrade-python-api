# import the client
from client import TDClient
from config import ACCOUNT_NUMBER, ACCOUNT_PASSWORD, CONSUMER_ID, REDIRECT_URI, TD_ACCOUNT, TRANSACTION_ID

# create a new session
TDSession = TDClient(account_number = ACCOUNT_NUMBER,
                     account_password = ACCOUNT_PASSWORD,
                     consumer_id = CONSUMER_ID,
                     redirect_uri = REDIRECT_URI)

# login to the session
TDSession.login()


# ------------------
# ENDPOINT TESTING
# ------------------


# TEST - `get_quotes` endpoint with single value. Should not return an error.
quotes_single = TDSession.get_quotes(instruments=['SQ'])

# TEST - `get_quotes` endpoint with multiple values. Should not return an error.
quotes_multi = TDSession.get_quotes(instruments=['SQ', 'MSFT'])


# TEST - `search_instruments` Endpoint. Should return error
# instrument_search_data = TDSession.search_instruments(symbol='MSFT', projection='INVALID VALUE')

# TEST - `search_instruments` Endpoint. Should not return an error
instrument_search_data = TDSession.search_instruments(symbol='MSFT', projection='symbol-search')


# TEST - `get_movers` Endpoint. Should return an error
# movers_data = TDSession.get_movers(market = '$DJI', direction = 'INVALID', change = 'value')

# TEST - `get_movers` Endpoint. Should not return an error
movers_data = TDSession.get_movers(market = '$DJI', direction = 'up', change = 'value')


# TEST - `get_instruments` Endpoint. Should not return an error
get_instrument_data = TDSession.get_instruments(cusip= '594918104')


# TEST - `get_quotes` Endpoint. Should not return an error
quote_data = TDSession.get_quotes(instruments=['MSFT','GOOG'])


# TEST - `get_market_hours` Endpoint with one value. Should not return an error
market_hours_single = TDSession.get_market_hours(markets = ['EQUITY'], date = '2019-10-19')

# TEST - `get_market_hours` Endpoint with multiple values. Should not return an error
market_hours_multi = TDSession.get_market_hours(markets = ['EQUITY','FOREX'], date = '2019-10-19')


# TEST - `get_accounts` Endpoint with single values. Should not return an error
accounts_data_single = TDSession.get_accounts(account = TD_ACCOUNT,  fields = ['orders'])

# TEST - `get_accounts` Endpoint with single values. Should not return an error
accounts_data_multi = TDSession.get_accounts(account = 'all',  fields = ['orders'])


# TEST - `get_transactions` Endpoint with single values. Should not return an error
transaction_data_single = TDSession.get_transactions(transaction_id= TRANSACTION_ID)

# TEST - `get_transactions` Endpoint. Should not return an error
transaction_data_multi = TDSession.get_transactions(account = TD_ACCOUNT, transaction_type = 'ALL')


# TEST - `get_preferences` endpoint. Should not return an error
preference_data = TDSession.get_preferences(account = TD_ACCOUNT)

# TEST - `get_subscription_keys` endpoint. Should not return an error
streamer_keys = TDSession.get_streamer_subscription_keys(accounts = [TD_ACCOUNT])

# TEST - `get_user_ principals` endpoint. Should not return an error.
prinicpals_data = TDSession.get_user_principals(fields = ['preferences','surrogateIds'])


# Print the data from the tests
print(quotes_single)
print(quotes_multi)

print(get_instrument_data)
print(movers_data)

print(market_hours_single)
print(market_hours_multi)

print(accounts_data_single)
print(accounts_data_multi)

print(transaction_data_single)
print(transaction_data_multi)

print(preference_data)
print(streamer_keys)
print(prinicpals_data)
