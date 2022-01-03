import unittest
from unittest import TestCase
from configparser import ConfigParser

from td.utils.enums import OptionaRange
from td.utils.enums import OptionType
from td.utils.enums import ContractType
from td.utils.enums import ExpirationMonth

from td.credentials import TdCredentials
from td.client import TdAmeritradeClient
from td.rest.options_chain import OptionsChain
from td.rest.options_chain import OptionChainQuery


class TestOptionsChainService(TestCase):

    """Will perform a unit test for the `OptionsChain` object."""

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

        self.service = self.td_client.options_chain()

    def test_creates_instance_of_client(self):
        """Create an instance and make sure it's a `TdAmeritradeClient` object."""

        self.assertIsInstance(self.td_client, TdAmeritradeClient)
        self.assertIsInstance(self.td_credentials, TdCredentials)

    def test_creates_instance_of_service(self):
        """Create an instance and make sure it's a `OptionsChain` object."""

        self.assertIsInstance(self.service, OptionsChain)

    def test_creates_instance_of_options_chain_query(self):
        """Create an instance and make sure it's a `OptionsChainQuery` object."""

        # Build a Query.
        option_chain_query = OptionChainQuery(
            symbol='MSFT',
            contract_type=ContractType.Call,
            expiration_month=ExpirationMonth.June,
            option_type=OptionType.StandardContracts,
            option_range=OptionaRange.InTheMoney,
            include_quotes=True
        )

        self.assertIsInstance(option_chain_query, OptionChainQuery)

    def test_get_option_chains_through_query_object(self):
        """Test grabbing option chains data using the `Query` object."""

        # Build a Query.
        option_chain_query = OptionChainQuery(
            symbol='MSFT',
            contract_type=ContractType.Call,
            expiration_month=ExpirationMonth.June,
            option_type=OptionType.StandardContracts,
            option_range=OptionaRange.InTheMoney,
            include_quotes=True
        )

        # Query the Options Data.
        options_data = self.service.get_option_chain(
            option_chain_query=option_chain_query
        )

        self.assertIn('numberOfContracts', list(options_data.keys()))

    def test_get_option_chains(self):
        """Test grabbing option chains data using a dictionary object."""

        # Build a Query.
        option_chain_dict = {
            'symbol': 'MSFT',
            'contractType': 'CALL',
            'expirationMonth': 'JUN',
            'optionType': 'SC',
            'range': 'ITM',
            'includeQuotes': True
        }

        # Query the Options Data.
        options_data = self.service.get_option_chain(
            option_chain_dict=option_chain_dict
        )

        self.assertIn('numberOfContracts', list(options_data.keys()))

    def tearDown(self) -> None:
        """Teardown the `TdAmeritradeClient` Client."""

        del self.td_client
        del self.td_credentials


if __name__ == '__main__':
    unittest.main()
