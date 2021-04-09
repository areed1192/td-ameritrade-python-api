import unittest

from unittest import TestCase
from configparser import ConfigParser

from td.credentials import TdCredentials
from td.client import TdAmeritradeClient
from td.quotes import Quotes
from td.movers import Movers


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

    def test_creates_instance_of_mover(self):
        """Create an instance and make sure it's a `Movers` object."""

        self.assertIsInstance(self.td_client.movers(), Movers)

    def tearDown(self) -> None:
        """Teardown the `TdAmeritradeClient` Client."""

        del self.td_client
        del self.td_credentials


if __name__ == '__main__':
    unittest.main()
