import requests
from td.client import TDClient
from td.config import ACCOUNT_NUMBER, ACCOUNT_PASSWORD, CONSUMER_ID, REDIRECT_URI, TD_ACCOUNT

# Create a new session
TDSession = TDClient(account_number = ACCOUNT_NUMBER,
                     account_password = ACCOUNT_PASSWORD,
                     consumer_id = CONSUMER_ID,
                     redirect_uri = REDIRECT_URI)

# Login to the session
TDSession.login()

# message_key_response = TDSession.message_key()
# print(message_key_response)

# Create a streaming sesion
TDStreamingClient = TDSession.create_streaming_session()

# # # Actives
# TDStreamingClient.actives(service = 'ACTIVES_NASDAQ', venue = 'NASDAQ', duration = 'ALL')

# # Charts, LOOK INTO!
# chart_fields = ['key', 'open_price','high_price','low_price','close_price','volume','sequence','chart_time']
# TDStreamingClient.chart(service = 'CHART_EQUITY', symbols = ['MSFT'], fields = chart_fields)

# # Quality of Service
# TDStreamingClient.quality_of_service(qos_level = 1)

# # Account Activity, LOOK INTO!
# TDStreamingClient.account_activity()

# # Chart History
# TDStreamingClient.chart_history()

# # Level One Quote
# TDStreamingClient.level_one_quote(symbols = ['MSFT'], fields = [0,1,2,3])

# # Level One Option
# TDStreamingClient.level_one_options(symbols = ['MSFT'], fields = [0,1,2,3])

# Level One Futures
# TDStreamingClient.level_one_futures(symbols = ['/ES'], fields = [0,1,2,3,4])

# # Level One Forex
# TDStreamingClient.level_one_forex(symbols = ['EUR/USD'], fields = [0,1,2,3,4])

# # Level One Futures Options - GET A SYMBOL TO VERIFY
# TDStreamingClient.level_one_futures_options(symbols = ['/ESZ3P990'], fields = [0,1,2,3,4])

# # News Headline
# TDStreamingClient.news_headline(symbols = ['AAPL'], fields = [0,1,2,3,4])

# # Timesale
# TDStreamingClient.timesale(service = 'TIMESALE_EQUITY', symbols = ['AAPL'], fields = [0,1,2,3,4])

# Level Two Quotes
TDStreamingClient.level_two_quotes()

# Print the requests
for request in TDStreamingClient.data_requests['requests']:
    print(request)
    print('-'*80)

# Stream it.
TDStreamingClient.stream()

# Close the stream.
# TDStreamingClient.close_stream()