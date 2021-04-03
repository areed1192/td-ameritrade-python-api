import unittest

from unittest import TestCase
from configparser import ConfigParser


class MySession(TestCase):

    """Will perform a unit test for the <PLACEHOLDER> session."""

    def setUp(self) -> None:
        """Set up the <PLACEHOLDER> Client."""

        # Initialize the Parser.
        config = ConfigParser()

        # Read the file.
        config.read('configs/config.ini')

        # Get the specified credentials.
        config.get('main', '')

    def test_creates_instance_of_session(self):
        """Create an instance and make sure it's a <PLACEHOLDER>."""
        pass

    def tearDown(self) -> None:
        """Teardown the <PLACEHOLDER> Client."""
        pass


if __name__ == '__main__':
    unittest.main()
