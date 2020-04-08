import pprint
from td.client import TDClient
from datetime import datetime, timedelta
from samples.config import (CONSUMER_ID, REDIRECT_URI, TRADING_ACCOUNT, JSON_PATH)

# Create a new session
TDSession = TDClient(consumer_id=CONSUMER_ID, redirect_uri=REDIRECT_URI, json_path=JSON_PATH)

# Login to the session
TDSession.login()

# Create a streaming sesion
TDStreamingClient = TDSession.create_streaming_session()

# Set the data dump location
TDStreamingClient.write_behavior(file_path = r"C:\Users\Alex\OneDrive\Desktop\Sigma\Repo - TD API Client\td-ameritrade-python-api\samples\raw_data.csv", append_mode = False)

# # Actives
# TDStreamingClient.actives(service='ACTIVES_NASDAQ', venue='NASDAQ', duration='ALL')

# # Quality of Service
# TDStreamingClient.quality_of_service(qos_level='express')

# # Level One Quote
# TDStreamingClient.level_one_quotes(symbols=["SPY", "IVV", "SDS", "SH", "SPXL", "SPXS", "SPXU", "SSO", "UPRO", "VOO"],  fields=list(range(0,50)))

# # Level One Option
# TDStreamingClient.level_one_options(symbols=['AAPL_040920C115'], fields=list(range(0,42)))

# # Level One Futures
# TDStreamingClient.level_one_futures(symbols=['/CL'], fields = list(range(0,34)))

# Level One Forex
# TDStreamingClient.level_one_forex(symbols=['EUR/USD'], fields=list(range(0,20)))

# # Level One Futures Options
# TDStreamingClient.level_one_futures_options(symbols=['./EW2J20C2675'], fields=list(range(0,36)))

# # Charts Futures
# TDStreamingClient.chart(service='CHART_FUTURES', symbols=['/CL'], fields=[0,1,2,3,4,5,6,7])

# # Timesale - Equity
# TDStreamingClient.timesale(service='TIMESALE_EQUITY', symbols=['AAPL'], fields=[0, 1, 2, 3, 4])

# # Timesale - Futures
# TDStreamingClient.timesale(service='TIMESALE_FUTURES', symbols=['/ES'], fields=[0, 1, 2, 3, 4])

# # News Headline
# TDStreamingClient.news_headline(symbols=['AAPL', 'SPY'], fields=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# # Account Activity
# TDStreamingClient.account_activity()

# # Level Two Quotes
# TDStreamingClient.level_two_quotes(symbols = ['IBM'], fields = [0,1,2])

# # Level Two Options
# TDStreamingClient.level_two_options(symbols=['AAPL_040920C115'], fields = [0,1,2])

# # Level Two NASQDAQ
# TDStreamingClient.level_two_nasdaq(symbols = ['MSFT'], fields = [0,1,2])

# # Level Two Total View 
# TDStreamingClient.level_two_total_view(symbols = ['AAPL'], fields = ['0','1','2'])

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



# # Charts Futures Options - CANT GET TO WORK.
# TDStreamingClient.chart(service='CHART_OPTIONS', symbols=['./EW2J20C2675'], fields=[0,1,2,3,4,5,6,7])

# # Chart History Futures - WORKS FOR WRIITNG BUT ONLY ONE BAR SENT BACK.
# TDStreamingClient.chart_history_futures(symbol = ['/ES'], frequency='m1', start_time='1586304000000', end_time='1586329200000')

# # Timesale - Options - SUBS BUT NO DATA.
# TDStreamingClient.timesale(service='TIMESALE_OPTIONS', symbols=['AAPL_040920C115'], fields=[0, 1, 2, 3, 4])