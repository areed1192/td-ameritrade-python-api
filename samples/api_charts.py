import pprint
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

# Define a list of all valid periods
valid_values = {
    'minute':{
        'day':[1, 2, 3, 4, 5, 10]
    },
    'daily':{
        'month':[1, 2, 3, 6],
        'year':[1, 2, 3, 5, 10, 15, 20],
        'ytd':[1]
    },
    'weekly':{
        'month':[1, 2, 3, 6],
        'year':[1, 2, 3, 5, 10, 15, 20],
        'ytd':[1]
    },
    'monthly':{
        'year':[1, 2, 3, 5, 10, 15, 20]
    }
}

valid_minute_frequencies = [1, 5, 10, 15, 30]


# Define the static arguments.
hist_symbol = 'MSFT'
hist_needExtendedHoursData = False

for frequency_type in valid_values.keys():
    frequency_periods = valid_values[frequency_type]

    for frequency_period in frequency_periods.keys():
        possible_values = frequency_periods[frequency_period]

        for value in possible_values:
            
            # Define the dynamic arguments - I want 5 DAYS of historical 1-minute bars.
            hist_periodType = frequency_period
            hist_period = value
            hist_frequencyType = frequency_type
            hist_frequency = 1

            # make the request
            historical_1_minute = TDSession.get_price_history(
                symbol=hist_symbol, 
                period_type=hist_periodType,
                period=hist_period, 
                frequency_type=hist_frequencyType,
                frequency=hist_frequency,
                extended_hours=hist_needExtendedHoursData
            )

"""
    CUSTOM RANGE
"""

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
historical_custom = TDSession.get_price_history(
    symbol=hist_symbol, 
    period_type=hist_periodType,
    frequency_type=hist_frequencyType,
    start_date=hist_startDate,
    end_date=hist_endDate,
    frequency=hist_frequency,
    extended_hours=hist_needExtendedHoursData
)

# Grab the candle count.
candle_count = len(historical_custom['candles'])
print('For PERIOD TYPE {} with CUSTOM PERIOD {} you got {} candles.'.format(hist_periodType, lookback_period, candle_count))