import unittest
from unittest import TestCase
from configparser import ConfigParser

from td.rest.quotes import Quotes
from td.client import TdAmeritradeClient
from td.credentials import TdCredentials


class TestQuotesService(TestCase):

    """Will perform a unit test for the `Quotes` service object."""

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

        self.service = self.td_client.quotes()

    def test_creates_instance_of_client(self):
        """Create an instance and make sure it's a `TdAmeritradeClient` object."""

        self.assertIsInstance(self.td_client, TdAmeritradeClient)
        self.assertIsInstance(self.td_credentials, TdCredentials)

    def test_creates_instance_of_quote(self):
        """Create an instance and make sure it's a `Quotes` object."""

        self.assertIsInstance(self.service, Quotes)

    def test_get_quote(self):
        """Test grabbing a single quote."""

        response = self.service.get_quote(instrument='AAPL')
        self.assertEqual('AAPL', list(response.keys())[0])

    def test_get_quotes(self):
        """Test grabbing multiple quotes."""

        response = self.service.get_quotes(instruments=['AAPL', 'SQ'])
        self.assertListEqual(['AAPL', 'SQ'], list(response.keys()))

    def tearDown(self) -> None:
        """Teardown the `TdAmeritradeClient` Client."""

        del self.td_client
        del self.td_credentials


if __name__ == '__main__':
    unittest.main()
