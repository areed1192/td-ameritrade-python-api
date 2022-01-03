import unittest
from unittest import TestCase
from configparser import ConfigParser

from td.credentials import TdCredentials
from td.client import TdAmeritradeClient
from td.rest.quotes import Quotes
from td.rest.movers import Movers
from td.rest.accounts import Accounts
from td.rest.market_hours import MarketHours
from td.rest.instruments import Instruments
from td.rest.user_info import UserInfo
from td.rest.price_history import PriceHistory
from td.rest.options_chain import OptionsChain
from td.rest.watchlists import Watchlists
from td.rest.orders import Orders
from td.rest.saved_orders import SavedOrders


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

    def test_creates_instance_of_accounts(self):
        """Create an instance and make sure it's a `Accounts` object."""

        self.assertIsInstance(self.td_client.accounts(), Accounts)

    def test_creates_instance_of_market_hours(self):
        """Create an instance and make sure it's a `MarketHours` object."""

        self.assertIsInstance(self.td_client.market_hours(), MarketHours)

    def test_creates_instance_of_instruments(self):
        """Create an instance and make sure it's a `Instruments` object."""

        self.assertIsInstance(self.td_client.instruments(), Instruments)

    def test_creates_instance_of_user_info(self):
        """Create an instance and make sure it's a `UserInfo` object."""

        self.assertIsInstance(self.td_client.user_info(), UserInfo)

    def test_creates_instance_of_price_history(self):
        """Create an instance and make sure it's a `PriceHistory` object."""

        self.assertIsInstance(self.td_client.price_history(), PriceHistory)

    def test_creates_instance_of_options_chain(self):
        """Create an instance and make sure it's a `OptionsChain` object."""

        self.assertIsInstance(self.td_client.options_chain(), OptionsChain)

    def test_creates_instance_of_watchlists(self):
        """Create an instance and make sure it's a `Watchlists` object."""

        self.assertIsInstance(self.td_client.watchlists(), Watchlists)

    def test_creates_instance_of_orders(self):
        """Create an instance and make sure it's a `Orders` object."""

        self.assertIsInstance(self.td_client.orders(), Orders)

    def test_creates_instance_of_saved_orders(self):
        """Create an instance and make sure it's a `SavedOrders` object."""

        self.assertIsInstance(self.td_client.saved_orders(), SavedOrders)

    def tearDown(self) -> None:
        """Teardown the `TdAmeritradeClient` Client."""

        del self.td_client
        del self.td_credentials


if __name__ == '__main__':
    unittest.main()
