import json
import unittest

from unittest import TestCase
from configparser import ConfigParser

from td.client import TDClient
from td.option_chain import OptionChain


class TDOptionChainSession(TestCase):

    """Will perform a unit test for the TD session."""

    def setUp(self) -> None:
        """Set up the Clients."""

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
            account_number=ACCOUNT_NUMBER
        )

        self.td_option_chain = OptionChain()

    def test_creates_instance_of_session(self):
        """Test to make sure objects are a correct instance."""

        self.assertIsInstance(self.td_session, TDClient)
        self.assertIsInstance(self.td_option_chain, OptionChain)

    def test_initialization_arguments(self):
        """Test to make sure objects are a correct instance."""

        # Initialize an option chain query.
        td_option_chain = OptionChain(
            symbol='F',
            contract_type='all'
        )

        # Validate the arguments.
        td_option_chain.validate_chain()

        # Test to verify everything is correct.
        self.assertIsInstance(td_option_chain, OptionChain)
        self.assertIsNotNone(td_option_chain.query_parameters)
        self.assertEqual(td_option_chain.query_parameters['symbol'], 'F')

    def test_making_a_request(self):
        """Test to make a request to the TD API."""

        # Initialize an option chain query.
        td_option_chain = OptionChain(
            symbol='F',
            contract_type='all'
        )

        # Validate the arguments.
        result = td_option_chain.validate_chain()

        # Verify the validation was the successful.
        self.assertTrue(result)

        # Make the request.
        opt_chain_resp = self.td_session.get_options_chain(
            option_chain=td_option_chain.query_parameters
        )

        # Make sure it's a dictionary.
        self.assertIsInstance(opt_chain_resp, dict)

        # Dump the data to the samples file.
        with open(r'samples\responses\sample_option_chain.jsonc', 'w+') as opt_file:
            json.dump(obj=opt_chain_resp, fp=opt_file, indent=3)

    def tearDown(self):
        """Clean Up."""

        self.td_session = None
        self.td_option_chain = None


if __name__ == '__main__':
    unittest.main()
