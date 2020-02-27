import pprint
from datetime import datetime, timedelta
from td.client import TDClient

TESTING_FLAG = True

# if TESTING_FLAG:
#     from config import ACCOUNT_NUMBER, ACCOUNT_PASSWORD, CONSUMER_ID, REDIRECT_URI, TD_ACCOUNT
# else:
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


#
#   NOTES ON AUTHENTICATION AND REFRESH TOKENS:
#   ------------------------------------------
#
#   It's very important to remember that TD will only allow for one REFRESH TOKEN. What that means is if you grab a REFRESH TOKEN
#   after doing a FULL AUTHENTICATION work flow and then proceed to do ANOTHER FULL AUTHENTICATION work flow. You have now invalidated
#   the previous REFRESH TOKEN. That means if you use the REFRESH TOKEN from the FIRST FULL AUTHENTICATION work flow, you will recieve
#   an "error: not authorized" response. At which point, you will need to do another FULL AUTHENTICAITON WORKFLOW.
#
#   My advice to you is to keep the your "TDAmeritradeState.json" in the same location and make sure any scripts that use it all point
#   to the same location.
#


# See the String Representation of the TDClient Session Object.
print(TDSession)


# ------------------
#
#   ENDPOINT TESTING - GET QUOTES
#
#   NOTES: The maximum number of quotes you may request at once is 500.
#
# ------------------

# TEST - `get_quotes` endpoint with single value. Should not return an error.
quotes_single = TDSession.get_quotes(instruments=['SQ'])

# TEST - `get_quotes` endpoint with multiple values. Should not return an error.
quotes_multi = TDSession.get_quotes(instruments=['SQ', 'MSFT'])

# PRINT - `get_quotes`
# pprint.pprint(quotes_single)
# pprint.pprint(quotes_multi)


# ------------------
#
#   ENDPOINT TESTING - HISTORICAL PRICES
#
#   NOTES:
#           1. For historical 1-minute bar data, you can get 1 day, 2 day, 3 day, 4 day, 5 day, or 10 day.
#
# ------------------


#
#   HISTORICAL MINUTE BARS.
#


# Define the static arguments.
hist_symbol = 'MSFT'
hist_needExtendedHoursData = False

# Define the dynamic arguments - I want 5 DAYS of historical 1-minute bars.
hist_periodType = 'day'
hist_period = 5
hist_frequencyType = 'minute'
hist_frequency = 1

# make the request
historical_1_minute = TDSession.get_price_history(symbol=hist_symbol, periodType=hist_periodType,
                                                  period=hist_period, frequencyType=hist_frequencyType,
                                                  frequency=hist_frequency, needExtendedHoursData=hist_needExtendedHoursData)


# # Define the dynamic arguments - I want 6 DAYS of historical 1-minute bars. - THIS WILL RAISE AN ERROR.
# hist_periodType = 'day'
# hist_period = 6
# hist_frequencyType = 'minute'
# hist_frequency = 1

# # make the request
# historical_6_minute = TDSession.get_price_history(symbol = hist_symbol, periodType = hist_periodType,
#                                                     period = hist_period, frequencyType = hist_frequencyType,
#                                                     frequency = hist_frequency, needExtendedHoursData = hist_needExtendedHoursData)
# pprint.pprint(historical_6_minute)


# Define a list of all valid minute periods.
valid_minute_periods = [1, 2, 3, 4, 5, 10]

# Test them all.
for minute_period in valid_minute_periods:

    # Define the dynamic arguments - I want 6 DAYS of historical 1-minute bars. - THIS WILL RAISE AN ERROR.
    hist_periodType = 'day'
    hist_period = minute_period
    hist_frequencyType = 'minute'
    hist_frequency = 1

    # Make the request
    historical_minute = TDSession.get_price_history(symbol=hist_symbol, periodType=hist_periodType,
                                                    period=hist_period, frequencyType=hist_frequencyType,
                                                    frequency=hist_frequency, needExtendedHoursData=hist_needExtendedHoursData)

    # Grab the candle count.
    candle_count = len(historical_minute['candles'])
    print('For MINUTE PERIOD {} you got {} worth of minute candles.'.format(
        hist_period, candle_count))


#
#   HISTORICAL DAILY BARS.
#


# Define a list for each period type and their valid FrequencyType.
valid_daily_periods_month = [1, 2, 3, 6]
valid_daily_periods_year = [1, 2, 3, 5, 10, 15, 20]
valid_daily_periods_ytd = [1]

# Define the period types that return daily data and assign their respective list.
valid_daily_periodTypes = {'month': valid_daily_periods_month,
                           'year': valid_daily_periods_year, 'ytd': valid_daily_periods_ytd}

# Test them all
for period, period_list in valid_daily_periodTypes.items():
    for period_list_item in period_list:

        # Define the dynamic arguments
        hist_periodType = period
        hist_period = period_list_item
        hist_frequencyType = 'daily'
        hist_frequency = 1

        # Make the request
        historical_minute = TDSession.get_price_history(symbol=hist_symbol, periodType=hist_periodType,
                                                        period=hist_period, frequencyType=hist_frequencyType,
                                                        frequency=hist_frequency, needExtendedHoursData=hist_needExtendedHoursData)

        # Grab the candle count.
        candle_count = len(historical_minute['candles'])
        print('For PERIOD TYPE {} with DAILY PERIOD {} you got {} candles.'.format(
            hist_periodType, hist_period, candle_count))


#
#   HISTORICAL WEEKLY BARS.
#


# Define a list for each period type and their valid FrequencyType.
valid_daily_periods_month = [1, 2, 3, 6]
valid_daily_periods_year = [1, 2, 3, 5, 10, 15, 20]
valid_daily_periods_ytd = [1]

# Define the period types that return daily data and assign their respective list.
valid_daily_periodTypes = {'month': valid_daily_periods_month,
                           'year': valid_daily_periods_year, 'ytd': valid_daily_periods_ytd}

# Test them all
for period, period_list in valid_daily_periodTypes.items():
    for period_list_item in period_list:

        # Define the dynamic arguments
        hist_periodType = period
        hist_period = period_list_item
        hist_frequencyType = 'weekly'
        hist_frequency = 1

        # Make the request
        historical_minute = TDSession.get_price_history(symbol=hist_symbol, periodType=hist_periodType,
                                                        period=hist_period, frequencyType=hist_frequencyType,
                                                        frequency=hist_frequency, needExtendedHoursData=hist_needExtendedHoursData)

        # Grab the candle count.
        candle_count = len(historical_minute['candles'])
        print('For PERIOD TYPE {} with WEEKLY PERIOD {} you got {} candles.'.format(
            hist_periodType, hist_period, candle_count))


#
#   HISTORICAL MONTHLY BARS.
#


# Define a list for each period type and their valid FrequencyType.
valid_daily_periods_year = [1, 2, 3, 5, 10, 15, 20]

# Define the period types that return daily data and assign their respective list.
valid_daily_periodTypes = {'year': valid_daily_periods_year}

# Test them all
for period, period_list in valid_daily_periodTypes.items():
    for period_list_item in period_list:

        # Define the dynamic arguments
        hist_periodType = period
        hist_period = period_list_item
        hist_frequencyType = 'monthly'
        hist_frequency = 1

        # Make the request
        historical_minute = TDSession.get_price_history(symbol=hist_symbol, periodType=hist_periodType,
                                                        period=hist_period, frequencyType=hist_frequencyType,
                                                        frequency=hist_frequency, needExtendedHoursData=hist_needExtendedHoursData)

        # Grab the candle count.
        candle_count = len(historical_minute['candles'])
        print('For PERIOD TYPE {} with MONTHLY PERIOD {} you got {} candles.'.format(
            hist_periodType, hist_period, candle_count))


#
#   HISTORICAL MINUTE BARS - CUSTOM RANGE 31 DAYS.
#

# We will need the datetime module.

# The max look back period for minute data is 31 Days.
lookback_period = 31

# Define today.
today_00 = datetime.now()

# Define 300 days ago.
today_ago = datetime.now() - timedelta(days=lookback_period)

# The TD API expects a timestamp in milliseconds. However, the timestamp() method only returns to seconds so multiply it by 1000.
today_00 = str(int(round(today_00.timestamp() * 1000)))
today_ago = str(int(round(today_ago.timestamp() * 1000)))

# These values will now be our startDate and endDate parameters.
hist_startDate = today_ago
hist_endDate = today_00

# Define the dynamic arguments, PERIOD IS NOT NEEDED!!!!
hist_periodType = 'day'
hist_frequencyType = 'minute'
hist_frequency = 1

# Make the request
historical_custom = TDSession.get_price_history(symbol=hist_symbol, periodType=hist_periodType,
                                                frequencyType=hist_frequencyType, startDate=hist_startDate, endDate=hist_endDate,
                                                frequency=hist_frequency, needExtendedHoursData=hist_needExtendedHoursData)

# Grab the candle count.
candle_count = len(historical_custom['candles'])
print('For PERIOD TYPE {} with CUSTOM PERIOD {} you got {} candles.'.format(
    hist_periodType, lookback_period, candle_count))


# # TEST - `search_instruments` Endpoint. Should return error
# # instrument_search_data = TDSession.search_instruments(symbol='MSFT', projection='INVALID VALUE')

# # TEST - `search_instruments` Endpoint. Should not return an error
# instrument_search_data = TDSession.search_instruments(symbol='MSFT', projection='symbol-search')


# # TEST - `get_movers` Endpoint. Should return an error
# # movers_data = TDSession.get_movers(market = '$DJI', direction = 'INVALID', change = 'value')

# # TEST - `get_movers` Endpoint. Should not return an error
# movers_data = TDSession.get_movers(market = '$DJI', direction = 'up', change = 'value')


# # TEST - `get_instruments` Endpoint. Should not return an error
# get_instrument_data = TDSession.get_instruments(cusip= '594918104')


# # TEST - `get_quotes` Endpoint. Should not return an error
# quote_data = TDSession.get_quotes(instruments=['MSFT','GOOG'])


# # TEST - `get_market_hours` Endpoint with one value. Should not return an error
# market_hours_single = TDSession.get_market_hours(markets = ['EQUITY'], date = '2019-10-19')

# # TEST - `get_market_hours` Endpoint with multiple values. Should not return an error
# market_hours_multi = TDSession.get_market_hours(markets = ['EQUITY','FOREX'], date = '2019-10-19')


# # TEST - `get_accounts` Endpoint with single values. Should not return an error
# accounts_data_single = TDSession.get_accounts(account = TD_ACCOUNT,  fields = ['orders'])

# # TEST - `get_accounts` Endpoint with single values. Should not return an error
# accounts_data_multi = TDSession.get_accounts(account = 'all',  fields = ['orders'])


# # TEST - `get_transactions` Endpoint with single values. Should not return an error
# # transaction_data_single = TDSession.get_transactions(transaction_id= TRANSACTION_ID)

# # TEST - `get_transactions` Endpoint. Should not return an error
# transaction_data_multi = TDSession.get_transactions(account = TD_ACCOUNT, transaction_type = 'ALL')


# # TEST - `get_preferences` endpoint. Should not return an error
# preference_data = TDSession.get_preferences(account = TD_ACCOUNT)

# # TEST - `get_subscription_keys` endpoint. Should not return an error
# streamer_keys = TDSession.get_streamer_subscription_keys(accounts = [TD_ACCOUNT])

# # TEST - `get_user_ principals` endpoint. Should not return an error.
# prinicpals_data = TDSession.get_user_principals(fields = ['preferences','surrogateIds'])


# print(get_instrument_data)
# print(movers_data)

# print(market_hours_single)
# print(market_hours_multi)

# print(accounts_data_single)
# print(accounts_data_multi)

# # print(transaction_data_single)
# print(transaction_data_multi)

# print(preference_data)
# print(streamer_keys)
# print(prinicpals_data)
