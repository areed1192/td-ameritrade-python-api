account_activity_fields = ['subscription-key',
                           'account-id', 'message-type', 'message-data']
level_one_forex_fields = ['symbol', 'bid-price', 'ask-price', 'last-price', 'bid-size', 'ask-size', 'total-volume', 'last-size', 'trade-time', 'quote-time', 'high-price', 'low-price', 'close-price', 'exchange-id', 'description',
                          'digits', 'open-price', 'net-change', '52-week-low', 'exchange-name', 'security-status', 'mark', 'tick', 'tick-amount', 'product', 'percent-change', 'trading-hours', 'is-tradable', 'market-maker', '52-week-high']
level_one_futures_fields = ['symbol', 'bid-price', 'ask-price', 'last-price', 'bid-size', 'ask-size', 'ask-id', 'bid-id', 'total-volume', 'last-size', 'trade-time', 'quote-time', 'high-price', 'low-price', 'close-price', 'exchange-id', 'description', 'last-id', 'open-price', 'net-change',
                            'security-status', 'mark', 'open-interest', 'future-percent-change', 'exhange-name', 'tick', 'tick-amount', 'product', 'future-price-format', 'future-trading-hours', 'future-is-tradable', 'future-multiplier', 'future-is-active', 'future-settlement-price', 'future-active-symbol', 'future-expiration-date']
level_one_futures_options_fields = ['symbol', 'bid-price', 'ask-price', 'last-price', 'bid-size', 'ask-size', 'ask-id', 'bid-id', 'total-volume', 'last-size', 'trade-time', 'quote-time', 'high-price', 'low-price', 'close-price', 'exchange-id', 'description', 'last-id', 'open-price', 'net-change',
                                    'security-status', 'mark', 'open-interest', 'future-percent-change', 'exhange-name', 'tick', 'tick-amount', 'product', 'future-price-format', 'future-trading-hours', 'future-is-tradable', 'future-multiplier', 'future-is-active', 'future-settlement-price', 'future-active-symbol', 'future-expiration-date']
level_one_option_fields = ['symbol', 'bid-price', 'ask-price', 'last-price', 'bid-size', 'ask-size', 'total-volume', 'last-size', 'trade-time', 'quote-time', 'high-price', 'low-price', 'close-price', 'quote-day', 'trade-day', 'volatility', 'description', 'digits', 'open-price', 'net-change', 'security-status', 'mark',
                           'open-interest', 'money-intrinsic-value', 'expiration-year', 'multiplier', 'strike-price', 'contract-type', 'underlying', 'expiration-month', 'deliverables', 'time-value', 'expiration-day', 'days-to-expiration', 'delta', 'gamma', 'theta', 'vega', 'rho', 'theoretical-option-value', 'underlying-price', 'uv-expiration-type']
level_one_quote_fields = ['symbol', 'bid-price', 'ask-price', 'last-price', 'bid-size', 'ask-size', 'ask-id', 'bid-id', 'total-volume', 'last-size', 'trade-time', 'quote-time', 'high-price', 'low-price', 'bid-tick', 'close-price', 'exchange-id', 'marginable', 'shortable', 'island-bid', 'island-ask', 'island-volume', 'quote-day', 'trade-day', 'volatility', 'description', 'last-id', 'digits', 'open-price', 'net-change', '52 -week-high', '52-week-low',
                          'pe-ratio', 'dividend-amount', 'dividend-yield', 'island-bid-size', 'island-ask-size', 'nav', 'fund-price', 'exchange-name', 'dividend-date', 'regular-market-quote', 'regular-market-trade', 'regular-market-last-price', 'regular-market-last-size', 'regular-market-trade-time', 'regular-market-trade-day', 'regular-market-net-change', 'security-status', 'mark', 'quote-time-in-long', 'trade-time-in-long', 'regular-market-trade-time-in-long']
news_headline_fields = ['symbol', 'error-code', 'story-datetime', 'headline-id', 'status',
                        'headline', 'story-id', 'count-for-keyword', 'keyword-array', 'is-hot', 'story-source']
qos_request_fields = ['express', 'real-time',
                      'fast', 'moderate', 'slow', 'delayed']
timesale_fields = ['symbol', 'last-price',
                   'last-size', 'trade-time', 'last-sequence']
chart_fields = ['key', 'open-price', 'high-price', 'low-price',
                'close-price', 'volume', 'sequence', 'chart-time', 'chart-day']

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

    NOTES - THINGS I FOUND
    ----------------------
    Order seems to matter with the fields. For example in Level One Quotes if I request fields like this [3, 8, 20, 1, 6]
    It will not work, but if I put all the fields in the correct sequential order [1, 2, 3, ... ,18 19, 20] There doesn't
    seem to be an issue anymore.

'''

import requests
from td.client import TDClient

TESTING_FLAG = True

if TESTING_FLAG:
    from td.config import ACCOUNT_NUMBER, ACCOUNT_PASSWORD, CONSUMER_ID, REDIRECT_URI, TD_ACCOUNT
else:
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

'''
    REGULAR - WORKING
'''

# Actives
TDStreamingClient.actives(service='ACTIVES_NASDAQ', venue='NASDAQ', duration='ALL')

# Quality of Service
TDStreamingClient.quality_of_service(qos_level='express')

'''
    LEVEL ONE DATA
'''

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

'''
    Hard to Identify what fixed the inital error.
    ---------------------------------------------
    1st. I set Streaming News to on for both of my accounts and the inital result was nothing.
    2nd. I opened ToS and then made a request to this endpoint and go success. However, even after closing it I still go a request.

    It's possible that step one fixed the issue, but there is a delay before you start seeing anything? Maybe a 15 minute delay? Additionally,
    I only had it on for one of my accounts and not the other, so you may need to turn it on for the account that is the main one you use.
'''

# News Headline
TDStreamingClient.news_headline(symbols=['AAPL'], fields=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

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
TDStreamingClient.account_activity()


'''
    EXPERIMENTAL SECTION
'''

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


# # Level Two Futures - NOT WORKING - MAY WORK IF YOU HAVE FUTURES TRADING ENABLED ON YOUR ACCOUNT.
# TDStreamingClient.level_two_futures(symbols=['/ES'], fields= [0,1,2])

# # Level Two Forex - NOT WORKING - MAY WORK IF YOU HAVE FOREX TRADING ENABLED ON YOUR ACCOUNT.
# TDStreamingClient.level_two_forex(symbols = ['AUD/CAD'], fields = [0,1,2,3])

# # Level Two Futures Options - MAY WORK IF YOU HAVE FUTURES TRADING ENABLED ON YOUR ACCOUNT.
# TDStreamingClient.level_two_futures_options(symbols=['./E1AG20'])

# News History - NOT WORKING
# TDStreamingClient.news_history()

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
