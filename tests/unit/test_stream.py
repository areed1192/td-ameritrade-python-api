import unittest
from datetime import datetime
from datetime import timedelta
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

        self.stream_session = self.td_session.create_streaming_session()

    def test_creates_instance_of_session(self):
        """Create an instance and make sure it's a robot."""

        self.assertIsInstance(self.td_session, TDClient)

    def test_create_stream_session(self):
        """Test Creating a new streaming session."""
        
        self.assertIsInstance(self.stream_session, TDStreamerClient)

    def test_subscribe_level_one_quotes(self):
        """Test subscribing to Level One Quotes."""

        self.stream_session.level_one_quotes(symbols=['MSFT','AAPL'], fields=list(range(0,1,38)))
        self.assertIn('QUOTE', self.stream_session.data_requests['requests'][0]['service'])

    def test_subscribe_level_two_quotes(self):
        """Test subscribing to Level One Quotes."""

        self.stream_session.level_two_quotes(symbols=['MSFT','AAPL'], fields=[0,1,2,3])
        self.assertIn('LISTED_BOOK', self.stream_session.data_requests['requests'][0]['service'])

    def tearDown(self) -> None:
        """Teardown the Robot."""

        self.td_session = None
        self.stream_session = None


if __name__ == '__main__':
    unittest.main()
