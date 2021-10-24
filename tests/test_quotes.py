import unittest
from unittest import TestCase
from configparser import ConfigParser

from td.rest.quotes import Quotes
from td.credentials import TdCredentials
from td.client import TdAmeritradeClient

class TestTdClient(TestCase):

    """Will perform a unit test for the `TdAmeritradeClient` object."""

    def setUp(self) -> None:
        """Set up the `TdAmeritradeClient` Client."""

        # Initialize the Parser.
        config = ConfigParser()

        # Read the file.
        config.read('config/config.ini')

        # Get the specified credentials.
        client_id = config.get('main', 'client_id')
        redirect_uri = config.get('main', 'redirect_uri')

        # Intialize our `Crednetials` object.
        self.td_credentials = TdCredentials(
            client_id=client_id,
            redirect_uri=redirect_uri,
            credential_file='config/td_credentials.json'
        )

        # Initalize the `TdAmeritradeClient`
        self.td_client = TdAmeritradeClient(
            credentials=self.td_credentials
        )

    def test_creates_instance_of_client(self):
        """Create an instance and make sure it's a `TdAmeritradeClient` object."""

        self.assertIsInstance(self.td_client, TdAmeritradeClient)
        self.assertIsInstance(self.td_credentials, TdCredentials)

    def test_creates_instance_of_quote(self):
        """Create an instance and make sure it's a `Quotes` object."""

        self.assertIsInstance(self.td_client.quotes(), Quotes)

    def test_get_quote(self):
        """Test grabbing a single quote."""

        quote_service = self.td_client.quotes()
        response = quote_service.get_quote(instrument='AAPL')

        self.assertEqual('AAPL', list(response.keys())[0])

    def test_get_quotes(self):
        """Test grabbing multiple quotes."""

        quote_service = self.td_client.quotes()
        response = quote_service.get_quotes(instruments=['AAPL', 'SQ'])
        keys = ['AAPL', 'SQ']

        self.assertListEqual(keys, list(response.keys()))

    def tearDown(self) -> None:
        """Teardown the `TdAmeritradeClient` Client."""

        del self.td_client
        del self.td_credentials


if __name__ == '__main__':
    unittest.main()
