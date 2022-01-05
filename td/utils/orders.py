from dataclasses import fields
from dataclasses import dataclass
from dataclasses import is_dataclass

from typing import Union
from typing import List
from enum import Enum


def _to_dict(data_class_obj: Union[dataclass, dict]) -> dict:

    class_dict = {}

    if is_dataclass(data_class_obj):

        # Loop through each field and grab the value and key.
        for field in fields(data_class_obj):

            key = field.name
            value = getattr(data_class_obj, field.name)

            # Handle values that could be Enums.
            if isinstance(value, Enum):
                value = value.value

            if isinstance(value, dict):
                value = _to_dict(data_class_obj=value)

            if isinstance(value, list):
                value = [_to_dict(data_class_obj=item) for item in value]

            # Generate the API Key.
            key_parts = key.split("_")
            key = "".join(
                [key_parts[0]] + [key.capitalize() for key in key_parts[1:]]
            )

            if value is not None:
                class_dict[key] = value

    elif isinstance(data_class_obj, dict):

        for key, value in data_class_obj.items():

            # Handle values that could be Enums.
            if isinstance(value, Enum):
                value = value.value

            if isinstance(value, dict):
                value = _to_dict(data_class_obj=value)

            if isinstance(value, list):
                value = [_to_dict(data_class_obj=item) for item in value]

            # Generate the API Key.
            key_parts = key.split("_")
            key = "".join(
                [key_parts[0]] + [key.capitalize() for key in key_parts[1:]]
            )

            if value is not None:
                class_dict[key] = value

    return class_dict


@dataclass
class OrderLegInstrument():

    """
    ## Overview
    ----
    Represents the Instrument object that is part of an order leg.
    The instrument is one of the financial objects that TD Ameritrade
    allows you to trade.
    """

    asset_type: Union[str, Enum]
    symbol: str

    def to_dict(self) -> dict:
        """Generates a dictionary containing all the field
        names and values.

        ### Returns
        ----
        dict
            The Field Name and Values.

        ### Usage
        ----
            >>> my_order_leg_instrument = {
                'asset_type': 'EQUITY',
                'symbol': 'SQ',
            }
            >>> my_order_leg_instrument = OrderLegInstrument(**my_order_leg_instrument)
            >>> my_order_leg_instrument.to_dict()
        """

        return _to_dict(data_class_obj=self)


@dataclass
class OrderLeg():

    """
    ## Overview
    ----
    Represents an OrderLeg object that is used to specify
    instructions about the order.
    """

    order_leg_type: Union[str, Enum] = None
    leg_id: int = 0
    instrument: Union[dict, OrderLegInstrument] = None
    instruction: Union[str, Enum] = None
    position_effect: Union[str, Enum] = None
    quantity: int = None
    quantity_type: str = None

    def to_dict(self) -> dict:
        """Generates a dictionary containing all the field
        names and values.

        ### Returns
        ----
        dict
            The Field Name and Values.

        ### Usage
        ----
            >>> my_order_leg = {
                'instruction': 'BUY',
                'instrument':{
                    'asset_type': 'EQUITY',
                    'symbol': 'SQ'
                },
                'quantity': 2
            }
            >>> my_order_leg = OrderLeg(**my_order_leg)
            >>> my_order_leg.to_dict()
        """

        return _to_dict(data_class_obj=self)


@dataclass
class Order():

    """
    ## Overview
    ----
    Represents the order object that you want to submit to
    TD Ameritrade.
    """

    order_leg_collection: List
    child_order_strategies: List

    price: float = 0.00
    session: Union[str, Enum] = None
    duration: Union[str, Enum] = None
    requested_destination: Union[str, Enum] = None
    complex_order_strategy_type: Union[str, Enum] = None
    stop_price_link_basis: Union[str, Enum] = None
    stop_price_link_type: Union[str, Enum] = None
    stop_type: Union[str, Enum] = None
    price_link_basis: Union[str, Enum] = None
    price_link_type: Union[str, Enum] = None
    order_type: Union[str, Enum] = None
    order_strategy_type: Union[str, Enum] = None

    def to_dict(self) -> dict:
        """Generates a dictionary containing all the field
        names and values.

        ### Returns
        ----
        dict
            The Field Name and Values.

        ### Usage
        ----
            >>> my_order_leg = {
                'instruction': 'BUY',
                'instrument':{
                    'asset_type': 'EQUITY',
                    'symbol': 'SQ'
                },
                'quantity': 2
            }
            >>> my_order_leg = OrderLeg(**my_order_leg)
            >>> my_order_leg.to_dict()
        """

        return _to_dict(data_class_obj=self)
