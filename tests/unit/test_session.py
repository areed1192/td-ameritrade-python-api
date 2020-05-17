import unittest

from unittest import TestCase
from datetime import datetime
from datetime import timedelta
from configparser import ConfigParser

from td.client import TDClient
from td.stream import TDStreamerClient


class TDSession(TestCase):

    """Will perform a unit test for the TD session."""

    def setUp(self) -> None:
        """Set up the Robot."""

        # Grab configuration values.
        config = ConfigParser()
        config.read('config/config.ini')

        CLIENT_ID = config.get('main', 'CLIENT_ID')
        REDIRECT_URI = config.get('main', 'REDIRECT_URI')
        JSON_PATH = config.get('main', 'JSON_PATH')
        ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

        # Initalize the session.
        self.td_session = TDClient(
            client_id=CLIENT_ID, 
            redirect_uri=REDIRECT_URI, 
            credentials_path=JSON_PATH,
            account_number = ACCOUNT_NUMBER
        )

    def test_creates_instance_of_session(self):
        """Create an instance and make sure it's a robot."""

        self.assertIsInstance(self.td_session, TDClient)

    def test_login(self):
        """Test whether the session is authenticated or not."""

        self.assertTrue(self.td_session.login())
        self.assertTrue(self.td_session.authstate)

    def test_state(self):
        """Make sure the state is updated."""

        self.assertIsNotNone(self.td_session.state['refresh_token'])
        self.assertNotEqual(self.td_session.state['refresh_token_expires_at'], 0)
        self.assertIsNotNone(self.td_session.state['access_token'])
        self.assertNotEqual(self.td_session.state['access_token_expires_at'], 0)

    def test_single_get_quotes(self):
        """Test Getting a Single quote."""

        # Grab a single quote.
        quotes = self.td_session.get_quotes(instruments=['MSFT'])

        # See if the Symbol is in the Quotes.
        self.assertIn('MSFT', quotes)

    def test_get_quotes(self):
        """Test Getting Multiple Quotes."""

        # Grab multiple Quotes.
        quotes = self.td_session.get_quotes(instruments=['MSFT', 'AAPL'])

        # See if the Symbols are in the Quotes.
        self.assertTrue(set(['MSFT','AAPL']).issuperset(set(quotes.keys())))

    def test_get_accounts(self):
        """Test Get Accounts."""

        accounts = self.td_session.get_accounts(
            account='all',
            fields=['orders','positions']
        )
        
        self.assertIn('positions', accounts[0]['securitiesAccount'])
        self.assertIn('currentBalances', accounts[0]['securitiesAccount'])
        # self.assertIn('orderStrategies', accounts[0]['securitiesAccount'])

    def test_create_stream_session(self):
        """Test Creating a new streaming session."""

        stream_session = self.td_session.create_streaming_session()
        self.assertIsInstance(stream_session, TDStreamerClient)

    def test_get_transactions(self):
        """Test getting transactions."""

        # `get_transactions` Endpoint. Should not return an error
        transaction_data_multi = self.td_session.get_transactions(
            account=self.td_session.account_number,
            transaction_type='ALL'
        )

        # Make sure it's a list.
        self.assertIsInstance(transaction_data_multi, list)
        self.assertIn('type', transaction_data_multi[0])

    def test_get_market_hours(self):
        """Test get market hours."""

        # `get_market_hours` Endpoint with multiple values
        market_hours_multi = self.td_session.get_market_hours(
            markets=['EQUITY','FOREX'],
            date=datetime.today().isoformat()
        )

        # If it's a weekend nothing is returned, so raise an error.
        if datetime.today().weekday() in (5,6):

            # Make sure it's a list.
            self.assertIsInstance(market_hours_multi, dict)
            self.assertIn('isOpen', market_hours_multi['equity']['equity'])

        else:
            # Make sure it's a list.
            self.assertIsInstance(market_hours_multi, dict)
            self.assertIn('isOpen', market_hours_multi['equity']['EQ'])

    def test_get_instrument(self):
        """Test getting an instrument."""

        # `get_instruments` Endpoint.
        get_instrument = self.td_session.get_instruments(
            cusip='594918104'
        )

        # Make sure it's a list.
        self.assertIsInstance(get_instrument, list)
        self.assertIn('cusip', get_instrument[0])

    def test_chart_history(self):
        """Test getting historical prices."""
        
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
                    historical_prices = self.td_session.get_price_history(
                        symbol=hist_symbol, 
                        period_type=hist_periodType,
                        period=hist_period, 
                        frequency_type=hist_frequencyType,
                        frequency=hist_frequency,
                        extended_hours=hist_needExtendedHoursData
                    )

                    self.assertIsInstance(historical_prices, dict)
                    self.assertFalse(historical_prices['empty'])
    
    def test_custom_historical_prices(self):
        """Test getting historical prices for a custom date range."""

        # The max look back period for minute data is 31 Days.
        lookback_period = 10

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

        # Define the dynamic arguments.
        hist_periodType = 'day'
        hist_frequencyType = 'minute'
        hist_frequency = 1

        # Make the request
        historical_custom = self.td_session.get_price_history(
            symbol='MSFT',
            period_type=hist_periodType,
            frequency_type=hist_frequencyType,
            start_date=hist_startDate,
            end_date=hist_endDate,
            frequency=hist_frequency,
            extended_hours=True
        )

        self.assertIsInstance(historical_custom, dict)
        self.assertFalse(historical_custom['empty'])

    def test_search_instruments(self):
        """Test Searching for Instruments."""

        # `search_instruments` Endpoint
        instrument_search_data = self.td_session.search_instruments(
            symbol='MSFT',
            projection='symbol-search'
        )

        self.assertIsInstance(instrument_search_data, dict)
        self.assertIn('MSFT', instrument_search_data)

    def test_get_movers(self):
        """Test getting Market movers."""

        # `get_movers` Endpoint
        movers_data = self.td_session.get_movers(
            market='$DJI',
            direction='up',
            change ='value'
        )

        if datetime.today().weekday() in (5,6):
            self.assertIsInstance(movers_data, list)
            self.assertFalse(movers_data)
        else:
            self.assertIsInstance(movers_data, list)
            self.assertIn('symbol', movers_data[0])

    def test_get_user_preferences(self):
        """Test getting user preferences."""

        # `get_preferences` endpoint. Should not return an error
        preference_data = self.td_session.get_preferences(account=self.td_session.account_number)

        self.assertIsInstance(preference_data, dict)
        self.assertIn('expressTrading', preference_data)

    def test_get_user_principals(self):
        """Test getting user principals."""

        # `get_preferences` endpoint. Should not return an error
        user_principals = self.td_session.get_user_principals(fields=['preferences','surrogateIds'])

        self.assertIsInstance(user_principals, dict)
        self.assertIn('authToken', user_principals)

    def test_get_streamer_keys(self):
        """Test getting user preferences."""

        # `get_subscription_keys` endpoint. Should not return an error
        streamer_keys = self.td_session.get_streamer_subscription_keys(accounts=[self.td_session.account_number])

        self.assertIsInstance(streamer_keys, dict)
        self.assertIn('keys', streamer_keys)

    def tearDown(self) -> None:
        """Teardown the Robot."""

        self.td_session = None


if __name__ == '__main__':
    unittest.main()
