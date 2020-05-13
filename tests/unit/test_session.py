import unittest
from datetime import datetime
from unittest import TestCase
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

    def test_get_quotes(self):
        """Test Get Quotes."""

        quotes = self.td_session.get_quotes(instruments=['MSFT', 'AAPL'])
        
        self.assertIn('MSFT', quotes)
        self.assertIn('AAPL', quotes)

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

    def tearDown(self) -> None:
        """Teardown the Robot."""

        self.td_session = None


if __name__ == '__main__':
    unittest.main()
