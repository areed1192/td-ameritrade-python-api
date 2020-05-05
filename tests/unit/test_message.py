import json
import unittest
from unittest import TestCase
from td.message import StreamingMessage
from td.message import StreamingMessageComponent


class TDMessage(TestCase):

    """Will perform a unit test for the TD Message"""

    def setUp(self) -> None:
        """Set up the Message test."""

        with open('tests/response_1.jsonc','r') as message_1:
            data_message = message_1.read()
        
        with open('tests/response_2.jsonc','r') as message_2:
            response_message = message_2.read()

        self.data_message = StreamingMessage(message=data_message)
        self.response_message = StreamingMessage(message=response_message)

    def test_creates_instance_of_session(self):
        """Create an instance and make sure they are StreamingMessages."""

        self.assertIsInstance(self.data_message, StreamingMessage)
        self.assertIsInstance(self.response_message, StreamingMessage)

    def test_create_components(self):
        """Test Breaking the messages into their individual components."""
        
        self.data_message.set_components()
        self.response_message.set_components()

        response_count = 1
        data_count = 2

        self.assertEqual(self.data_message.components_count, data_count)
        self.assertEqual(self.response_message.components_count, response_count)

    def test_is_data_response(self):
        """Test if the response is a data response."""

        self.assertEqual(self.data_message.is_data_response, True)
        self.assertEqual(self.response_message.is_data_response, False)

    def test_is_subscription_response(self):
        """Test if the response is a Subscription response."""

        self.assertEqual(self.data_message.is_subscription_response, False)
        self.assertEqual(self.response_message.is_subscription_response, True)

    def tearDown(self) -> None:
        """Teardown the Messages."""

        self.data_message = None
        self.response_message = None


if __name__ == '__main__':
    unittest.main()
