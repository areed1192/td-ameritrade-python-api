import requests
from td.client import TDClient
from td.config import ACCOUNT_NUMBER, ACCOUNT_PASSWORD, CONSUMER_ID, REDIRECT_URI, TD_ACCOUNT

'''

    WORKING
    -------

    1. ACTIVES
    2. QUALITY OF SERVICE
    3. CHART HISTORY FUTURES
    4. CHART
    5. LEVEL ONE QUOTES
    6. LEVEL ONE FUTURES
    7. LEVEL ONE OPTIONS
    8. LEVEL ONE FUTURES OPTIONS
    9. TIMESALES


    WORKING - WITH NOTES
    --------------------
    10. NEWS_HEADLINE
    11. ACCT_ACTIVITY


    EXPERIMENTAL - WORKING
    ----------------------
    1. LEVEL TWO QUOTES
    2. LEVEL TWO OPTIONS
    3. LEVEL TWO NASDAQ

'''

# Create a new session
TDSession = TDClient(account_number = ACCOUNT_NUMBER,
                     account_password = ACCOUNT_PASSWORD,
                     consumer_id = CONSUMER_ID,
                     redirect_uri = REDIRECT_URI)

# Login to the session
TDSession.login()

# Create a streaming sesion
TDStreamingClient = TDSession.create_streaming_session()

'''
    REGULAR - WORKING
'''

# # Actives
# TDStreamingClient.actives(service = 'ACTIVES_NASDAQ', venue = 'NASDAQ', duration = 'ALL')

# # Charts, this looks like it only streams every one minute. Hence if you want the last bar you should use this.
# chart_fields = ['key', 'open_price','high_price','low_price','close_price','volume','sequence','chart_time','chart_day']
# TDStreamingClient.chart(service = 'CHART_EQUITY', symbols = ['MSFT'], fields = chart_fields)

# # Quality of Service
# TDStreamingClient.quality_of_service(qos_level = 1)

# # Chart History, THIS MIGHT BE RESTRICTED TO JUST FUTURES BECAUSE OF THE NEW PRICE HISTORY ENDPOINT
# TDStreamingClient.chart_history(service = 'CHART_HISTORY_EQUITY',symbols = ['AAPL'],frequency='m1',period='d1')

# # Level One Quote
# TDStreamingClient.level_one_quote(symbols = ['MSFT'], fields = [0,1,2,3])

# # Level One Option
TDStreamingClient.level_one_options(symbols = ['MSFT_013120C115'], fields = [0,1,2,3])

# Level One Futures
# TDStreamingClient.level_one_futures(symbols = ['/ES'], fields = [0,1,2,3,4])

# # Level One Forex
# TDStreamingClient.level_one_forex(symbols = ['EUR/USD'], fields = [0,1,2,3,4])

# # Level One Futures Options - GET A SYMBOL TO VERIFY
# TDStreamingClient.level_one_futures_options(symbols = ['/ESZ3P990'], fields = [0,1,2,3,4])

# # Timesale
# TDStreamingClient.timesale(service = 'TIMESALE_EQUITY', symbols = ['AAPL'], fields = [0,1,2,3,4])

'''
    WORKING BUT WITH NOTES.
'''


'''
    Hard to Identify what fixed the inital error.
    ---------------------------------------------
    1st. I set Streaming News to on for both of my accounts and the inital result was nothing.
    2nd. I opened ToS and then made a request to this endpoint and go success. However, even after closing it I still go a request.

    It's possible that step one fixed the issue, but there is a delay before you start seeing anything? Maybe a 15 minute delay? Additionally,
    I only had it on for one of my accounts and not the other, so you may need to turn it on for the account that is the main one you use.
'''
# News Headline
# TDStreamingClient.news_headline(symbols = ['AAPL'], fields = [0,1,2,3,4,5,6,7,8,9,10])

'''
    The Documentation makes this one confusing.
    ---------------------------------------------
    The documentation kept mentioning something related to a MessageKey API. The problem was there was no reference to it anywhere
    on the TD Ameritrade website. It appears it was an old endpoint in the old API. However, the documentation seems to not reflect
    the new protocol for subscribing to this stream.

    When you get the streaming key, this appears to also be the MessageKey needed for this request. In other words, to use this endpoint

    1.Make a request to either the "Get User Principals" endpoint or the "Get Streamer Subscription Keys" endpoint and grab the subscription
      key from that one.
    2.Use the Subscription Key from that request as the "Keys" argument for the request.
'''
# Account Activity
# TDStreamingClient.account_activity()


'''
    EXPERIMENTAL SECTION
'''

# Level Two Options
# TDStreamingClient.level_two_options()

# Level Two Quotes
# TDStreamingClient.level_two_quotes()

# Level Two NASQDAQ
# TDStreamingClient.level_two_nasdaq()

# Level Two Futures
# TDStreamingClient.level_two_futures()

TDStreamingClient.level_two_forex()

# Print the requests
for request in TDStreamingClient.data_requests['requests']:
    print(request)
    print('-'*80)

# Stream it.
TDStreamingClient.stream()


# Level Two Quotes - OLD
# TDStreamingClient.level_two_quotes_nasdaq()

# News History
# TDStreamingClient.news_history()

# Close the stream.
# TDStreamingClient.close_stream()