import unittest
import td.enums as td_enums

from unittest import TestCase
from configparser import ConfigParser

from td.orders import Order
from td.orders import OrderLeg
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
            account_number=ACCOUNT_NUMBER
        )

        self.td_order = Order()
        self.td_order_leg = OrderLeg()

    def test_creates_instance_of_session(self):
        """Create an instance and make sure it's a robot."""

        self.assertIsInstance(self.td_session, TDClient)
        self.assertIsInstance(self.td_order, Order)
        self.assertIsInstance(self.td_order_leg, OrderLeg)

    def test_define_simple_order(self):
        """Test creating a simple order."""

        # Add the Order session.
        self.td_order.order_session(
            session=td_enums.ORDER_SESSION.NORMAL
        )

        # Add the Order duration.
        self.td_order.order_duration(
            duration=td_enums.DURATION.GOOD_TILL_CANCEL
        )

        # Add the Order Leg Instruction.
        self.td_order_leg.order_leg_instruction(
            instruction=td_enums.ORDER_INSTRUCTIONS.SELL
        )

        # Add the Order Leg price.
        self.td_order_leg.order_leg_price(
            price=112.50
        )

        # Add the Order Leg quantity.
        self.td_order_leg.order_leg_quantity(
            quantity=10
        )

        # Add the Order Leg Asset.
        self.td_order_leg.order_leg_asset(
            asset_type=td_enums.ORDER_ASSET_TYPE.EQUITY,
            symbol='MSFT'
        )

        # Add the Order Leg.
        self.td_order.add_order_leg(
            order_leg=self.td_order_leg
        )

        correct_dict = {
            "session": "NORMAL",
            "duration": "GOOD_TILL_CANCEL",
            "orderLegCollection": [
                {
                    "instruction": "SELL",
                    "price": 112.5, "quantity": 10,
                    "instrument": {
                        "assetType":
                        "EQUITY",
                        "symbol": "MSFT"
                    }
                }
            ]
        }

        self.assertDictEqual(correct_dict, self.td_order._grab_order())

    def tearDown(self):
        """Clean Up."""

        self.td_session = None
        self.td_order = None
        self.td_order_leg = None


if __name__ == '__main__':
    unittest.main()
