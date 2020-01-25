from td.client import TDClient
from td.config import ACCOUNT_NUMBER, ACCOUNT_PASSWORD, CONSUMER_ID, REDIRECT_URI, TD_ACCOUNT

# Create a new session
TDSession = TDClient(account_number = ACCOUNT_NUMBER,
                     account_password = ACCOUNT_PASSWORD,
                     consumer_id = CONSUMER_ID,
                     redirect_uri = REDIRECT_URI)

# Login to the session
TDSession.login()

# Create a streaming sesion
TDStreamingClient = TDSession.create_streaming_session()

# Define a service you want to stream.
TDStreamingClient.actives(service = 'ACTIVES_NASDAQ', venue = 'NASDAQ', duration = 'ALL')

# DOESN'T LIKE CERTAIN KEYS - LOOK INTO IT.
# chart_equity_fields = ['open_price','high_price','low_price','close_price','volume','sequence','chart_time','chart_day']
# TDStreamingClient.chart_equity(symbols = ['MSFT','GOOG','AAPL'], fields = chart_equity_fields)

print(TDStreamingClient.data_requests)

# Stream it.
TDStreamingClient.stream()