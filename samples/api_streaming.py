import requests
from td.client import TDClient

# DEFINE LOGIN CREDENTIALS
ACCOUNT_NUMBER = '<YOUR TD ACCOUNT USERNAME>'
ACCOUNT_PASSWORD = '<YOUR TD ACCOUNT PASSWORD>'
CONSUMER_ID = '<YOUR TD DEVELOPER ACCOUNT CONSUMER ID>'
REDIRECT_URI = '<YOUR TD DEVELOPER ACCOUNT REDIRECT URI>'

# Create a new session
TDSession = TDClient(account_number=ACCOUNT_NUMBER,
                     account_password=ACCOUNT_PASSWORD,
                     consumer_id=CONSUMER_ID,
                     redirect_uri=REDIRECT_URI)

# Login to the session
TDSession.login()

# Create a streaming sesion
TDStreamingClient = TDSession.create_streaming_session()

# Define the CSV Append Mode. Needs to be rewritten it's kind of awkward to call it like this.
TDStreamingClient.CSV_APPEND_MODE = True

# Actives
TDStreamingClient.actives(service='ACTIVES_NASDAQ', venue='NASDAQ', duration='ALL')

# Quality of Service
TDStreamingClient.quality_of_service(qos_level='express')

# Level One Quote
TDStreamingClient.level_one_quotes(symbols=["SPY", "IVV", "SDS", "SH", "SPXL", "SPXS", "SPXU", "SSO", "UPRO", "VOO"],  fields=list(range(0,8)))

# Level One Option
TDStreamingClient.level_one_options(symbols=['MSFT_030620P140'], fields=list(range(0,42)))

# Level One Futures
TDStreamingClient.level_one_futures(symbols=['/CL'], fields=["0", "1", "2", "3", "4"])

# Level One Forex - VALIDATE JSON RESPONSE
TDStreamingClient.level_one_forex(symbols=['EUR/USD'], fields=list(range(0,26)))

# Level One Futures Options - VALIDATE JSON RESPONSE
TDStreamingClient.level_one_futures_options(symbols=['./E1AG20C3220'], fields=list(range(0,36)))

# Charts, this looks like it only streams every one minute. Hence if you want the last bar you should use this.
TDStreamingClient.chart(service='CHART_FUTURES', symbols=['/CL'], fields=[0,1,2,3,4,5,6,7])

# Charts, this looks like it only streams every one minute. Hence if you want the last bar you should use this.
TDStreamingClient.chart(service='CHART_OPTIONS', symbols=['MSFT_030620P140'], fields=[0,1,2,3,4,5,6])

# Chart History Futures
TDStreamingClient.chart_history_futures(symbol = ['/ES'], frequency='m5', period='d1')

# Timesale
TDStreamingClient.timesale(service='TIMESALE_FUTURES', symbols=['/ES'], fields=[0, 1, 2, 3, 4])

# News Headline
TDStreamingClient.news_headline(symbols=['AAPL'], fields=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Account Activity
TDStreamingClient.account_activity()

# Level Two Options
TDStreamingClient.level_two_options(symbols=['ESH20_022120C20'], fields = [0,1,2])

# Level Two Quotes
TDStreamingClient.level_two_quotes(symbols = ['IBM'], fields = [0,1,2])

# Level Two NASQDAQ
TDStreamingClient.level_two_nasdaq(symbols = ['MSFT'], fields = [0,1,2])

# Level Two NYSE
TDStreamingClient.level_two_nyse(symbols = ['AA'], fields = [0,1,2])

# Level Two Total View 
TDStreamingClient.level_two_total_view(symbols = ['AAPL'], fields = [0,1,2])

# Stream it.
TDStreamingClient.stream()


'''
    DEFINING CLOSE LOGIC

    Closing the stream involves defining the number of seconds you want to keep it open. Right now,
    the logic is basic but in future releases we will be able to specify specific times like during
    market hours.
'''

# # Let's keep the server open for only 10 seconds, so define the time in seconds.
# keep_open_in_seconds = 10

# # Call the streaming client, and set the logic.
# TDStreamingClient.close_logic(run_duration=keep_open_in_seconds)

# # Start Streaming.
# TDStreamingClient.stream()
