import unittest
from datetime import datetime
from unittest import TestCase
from configparser import ConfigParser

from td.utils.enums import Markets
from td.credentials import TdCredentials
from td.client import TdAmeritradeClient
from td.rest.market_hours import MarketHours


class TestMarketHourService(TestCase):

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

        self.service = self.td_client.market_hours()

    def test_creates_instance_of_client(self):
        """Create an instance and make sure it's a `TdAmeritradeClient` object."""

        self.assertIsInstance(self.td_client, TdAmeritradeClient)
        self.assertIsInstance(self.td_credentials, TdCredentials)

    def test_creates_instance_of_market_hours(self):
        """Create an instance and make sure it's a `MarketHours` object."""

        self.assertIsInstance(self.service, MarketHours)

    def test_get_single_market_hours(self):
        """Test grabbing market hours for a single market."""

        # Grab the market hours for the equity Markets.
        response = self.service.get_market_hours(
            market='EQUITY',
            date=datetime.now()
        )

        self.assertEqual('equity', list(response.keys())[0])

        # Grab the market hours for the equity Markets, using Enums.
        response = self.service.get_market_hours(
            market=Markets.Equity,
            date=datetime.now()
        )

        self.assertEqual('equity', list(response.keys())[0])

    def test_get_multiple_market_hours(self):
        """Test grabbing market hours for a multiple markets."""

        # Grab the market hours for the equity Markets.
        response = self.service.get_multiple_market_hours(
            markets=['EQUITY', 'BOND'],
            date=datetime.now()
        )

        self.assertEqual('equity', list(response.keys())[0])

        # Grab the market hours for the equity Markets, using Enums.
        response = self.service.get_multiple_market_hours(
            markets=[Markets.Equity, Markets.Bond],
            date=datetime.now()
        )

        self.assertEqual('equity', list(response.keys())[0])

    def tearDown(self) -> None:
        """Teardown the `TdAmeritradeClient` Client."""

        del self.td_client
        del self.td_credentials


if __name__ == '__main__':
    unittest.main()
