from datetime import datetime
from datetime import timedelta
from td.client import TDClient

# Create a new session
TDSession = TDClient(
    client_id='<CLIENT_ID>',
    redirect_uri='<REDIRECT_URI>',
    credentials_path='<CREDENTIALS_PATH>'
)


# Login to the session
TDSession.login()

# `get_quotes` endpoint with single value. Should not return an error.
quotes_single = TDSession.get_quotes(instruments=['SQ'])

# `get_quotes` with a Options Contract
quotes_option_contract = TDSession.get_quotes(instruments=['MSFT_041720C75'])

# `get_quotes` with a Futures Contract
quotes_futures = TDSession.get_quotes(instruments=['/ES'])

# `get_quotes` with Forex
quotes_forex = TDSession.get_quotes(instruments=['AUD/USD'])

# `get_quotes` endpoint with multiple values
quotes_multi = TDSession.get_quotes(instruments=['SQ', 'MSFT'])

# `search_instruments` Endpoint
instrument_search_data = TDSession.search_instruments(
    symbol='MSFT',
    projection='symbol-search'
)

# `get_movers` Endpoint
movers_data = TDSession.get_movers(
    market='$DJI',
    direction='up',
    change='value'
)

# `get_instruments` Endpoint
get_instrument_data = TDSession.get_instruments(cusip='594918104')

# `get_market_hours` Endpoint with multiple values
market_hours_multi = TDSession.get_market_hours(
    markets=['EQUITY','FOREX'],
    date=datetime.today().isoformat()
)

# `get_accounts` Endpoint with single values
accounts_data_single = TDSession.get_accounts(
    account='<ACCOUNT_NUMBER>',
    fields=['orders']
)

# `get_accounts` Endpoint with single values
accounts_data_multi = TDSession.get_accounts(
    account='all',
    fields=['orders']
)

# `get_transactions` Endpoint. Should not return an error
transaction_data_multi = TDSession.get_transactions(
    account='<ACCOUNT_NUMBER>',
    transaction_type='ALL'
)

# `get_preferences` endpoint. Should not return an error
preference_data = TDSession.get_preferences(account='<ACCOUNT_NUMBER>')

# `get_subscription_keys` endpoint. Should not return an error
streamer_keys = TDSession.get_streamer_subscription_keys(accounts=['<ACCOUNT_NUMBER>'])

# `get_user_ principals` endpoint. Should not return an error.
prinicpals_data = TDSession.get_user_principals(fields=['preferences', 'surrogateIds'])

# `get_transactions` Endpoint with single values
transaction_data_single = TDSession.get_transactions(transaction_id='YOUR_TRANSACTION_ID')

# Option Chain Example
opt_chain = {
    'symbol':'MSFT',
    'contractType':'CALL',
    'optionType':'S',
    'fromDate':'2020-04-01',
    'afterDate':'2020-05-01',
    'strikeCount':4,
    'includeQuotes':True,
    'range':'ITM',
    'strategy':'ANALYTICAL',
    'volatility': 29.0
}

# Get Option Chains
option_chains = TDSession.get_options_chain(option_chain=opt_chain)
