import unittest
from unittest import TestCase
from configparser import ConfigParser

from td.utils.orders import Order
from td.utils.orders import OrderLeg
from td.utils.orders import OrderLegInstrument

from td.utils.enums import AssetType
from td.utils.enums import OrderInstructions


class TestTdOrderUtils(TestCase):

    """Will perform a unit test for the different `Order` utility objects."""

    def test_order_leg_instrument(self):
        """Create an instance and make sure it's a `OrderLegInstrument` object."""

        correct = {
            'assetType': 'EQUITY',
            'symbol': 'SQ'
        }

        my_order_leg_instrument = {
            'asset_type': 'EQUITY',
            'symbol': 'SQ',
        }

        my_order_leg_instrument = OrderLegInstrument(**my_order_leg_instrument)
        my_order_leg_instrument = my_order_leg_instrument.to_dict()

        self.assertIsNotNone(my_order_leg_instrument)
        self.assertDictEqual(d1=my_order_leg_instrument, d2=correct)

        my_order_leg_instrument = {
            'asset_type': AssetType.Equity,
            'symbol': 'SQ',
        }

        my_order_leg_instrument = OrderLegInstrument(**my_order_leg_instrument)
        my_order_leg_instrument = my_order_leg_instrument.to_dict()

        self.assertIsNotNone(my_order_leg_instrument)
        self.assertDictEqual(d1=my_order_leg_instrument, d2=correct)

    def test_order_leg(self):
        """Create an instance and make sure it's a `OrderLeg` object."""

        correct = {
            'orderLegType': None,
            'instruction': 'BUY',
            'legId': 0,
            'instrument': {
                'assetType': 'EQUITY',
                'symbol': 'SQ'
            },
            'quantity': 2,
            'positionEffect': None,
            'quantityType': None
        }

        my_order_leg = {
            'instruction': 'BUY',
            'instrument': {
                'asset_type': 'EQUITY',
                'symbol': 'SQ'
            },
            'quantity': 2
        }

        my_order_leg = OrderLeg(**my_order_leg)
        my_order_leg = my_order_leg.to_dict()

        self.assertIsNotNone(my_order_leg)
        self.assertDictEqual(d1=my_order_leg, d2=correct)

        my_order_leg = {
            'instruction': OrderInstructions.Buy,
            'instrument': {
                'asset_type': AssetType.Equity,
                'symbol': 'SQ'
            },
            'quantity': 2
        }

        my_order_leg = OrderLeg(**my_order_leg)
        my_order_leg = my_order_leg.to_dict()

        self.assertIsNotNone(my_order_leg)
        self.assertDictEqual(d1=my_order_leg, d2=correct)


if __name__ == '__main__':
    unittest.main()
