import unittest
from unittest import TestCase
from configparser import ConfigParser

from td.utils.orders import Order
from td.utils.orders import OrderLeg
from td.utils.orders import OrderLegInstrument

from td.utils.enums import AssetType
from td.utils.enums import OrderInstructions
from td.utils.enums import OrderStrategyType
from td.utils.enums import OrderType
from td.utils.enums import DefaultOrderDuration


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
        my_order_leg_instrument

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
            'instruction': 'BUY',
            'legId': 0,
            'instrument': {
                'assetType': 'EQUITY',
                'symbol': 'SQ'
            },
            'quantity': 2
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

    def test_order(self):
        """Create an instance and make sure it's a `Order` object."""

        correct = {
            "orderType": "LIMIT",
            "session": "NORMAL",
            "price": 34.97,
            "duration": "DAY",
            "orderStrategyType": "TRIGGER",
            "orderLegCollection": [
                {
                    "instruction": "BUY",
                    "quantity": 10,
                    "instrument": {
                        "symbol": "XYZ",
                        "assetType": "EQUITY"
                    }
                }
            ],
            "childOrderStrategies": [
                {
                    "orderType": "LIMIT",
                    "session": "NORMAL",
                    "price": "42.03",
                    "duration": "DAY",
                    "orderStrategyType": "SINGLE",
                    "orderLegCollection": [
                        {
                            "instruction": "SELL",
                            "quantity": 10,
                            "instrument": {
                                "symbol": "XYZ",
                                "assetType": "EQUITY"
                            }
                        }
                    ]
                }
            ]
        }

        my_order = {
            "order_type": "LIMIT",
            "session": "NORMAL",
            "price": 34.97,
            "duration": "DAY",
            "order_strategy_type": "TRIGGER",
            "order_leg_collection": [
                {
                    "instruction": "BUY",
                    "quantity": 10,
                    "instrument": {
                        "symbol": "XYZ",
                        "asset_type": "EQUITY"
                    }
                }
            ],
            "child_order_strategies": [
                {
                    "order_type": "LIMIT",
                    "session": "NORMAL",
                    "price": "42.03",
                    "duration": "DAY",
                    "order_strategy_type": "SINGLE",
                    "order_leg_collection": [
                        {
                            "instruction": "SELL",
                            "quantity": 10,
                            "instrument": {
                                "symbol": "XYZ",
                                "asset_type": "EQUITY"
                            }
                        }
                    ]
                }
            ]
        }

        my_order = Order(**my_order)
        my_order = my_order.to_dict()

        self.assertIsNotNone(my_order)
        self.assertDictEqual(d1=my_order, d2=correct)

        my_order = {
            "order_type": "LIMIT",
            "session": "NORMAL",
            "price": 34.97,
            "duration": "DAY",
            "order_strategy_type": "TRIGGER",
            "order_leg_collection": [
                {
                    "instruction": OrderInstructions.Buy,
                    "quantity": 10,
                    "instrument": {
                        "symbol": "XYZ",
                        "asset_type": "EQUITY"
                    }
                }
            ],
            "child_order_strategies": [
                {
                    "order_type": OrderType.Limit,
                    "session": "NORMAL",
                    "price": "42.03",
                    "duration": DefaultOrderDuration.Day,
                    "order_strategy_type": OrderStrategyType.Single,
                    "order_leg_collection": [
                        {
                            "instruction": OrderInstructions.Sell,
                            "quantity": 10,
                            "instrument": {
                                "symbol": "XYZ",
                                "asset_type": AssetType.Equity
                            }
                        }
                    ]
                }
            ]
        }

        my_order = Order(**my_order)
        my_order = my_order.to_dict()

        self.assertIsNotNone(my_order)
        self.assertDictEqual(d1=my_order, d2=correct)


if __name__ == '__main__':
    unittest.main()
