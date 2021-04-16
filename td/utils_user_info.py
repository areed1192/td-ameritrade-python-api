from dataclasses import dataclass
from dataclasses import fields
from pprint import pprint
from typing import Union
from enum import Enum
from td.enums import DefaultOrderDuration
from td.enums import DefaultAdvancedToolLaunch
from td.enums import DefaultOrderLegInstruction
from td.enums import DefaultOrderMarketSession
from td.enums import DefaultOrderPriceLinkType
from td.enums import DefaultOrderType
from td.enums import TaxLotMethod
from td.enums import AuthTokenTimeout


@dataclass
class UserPreferences():

    default_equity_order_leg_instruction: Union[str, Enum]
    default_equity_order_type: Union[str, Enum]
    default_equity_order_price_link_type: Union[str, Enum]
    default_equity_order_duration: Union[str, Enum]
    default_equity_order_market_session: Union[str, Enum]
    mutual_fund_tax_lot_method: Union[str, Enum]
    option_tax_lot_method: Union[str, Enum]
    equity_tax_lot_method: Union[str, Enum]
    default_advanced_tool_launch: Union[str, Enum]
    auth_token_timeout: Union[str, Enum]
    express_trading: bool = False
    default_equity_quantity: int = 0

    def to_dict(self) -> dict:

        class_dict = {}

        # Loop through each field and grab the value and key.
        for field in fields(self):

            key = field.name
            value = getattr(self, field.name)

            # Handle values that could be Enums.
            if isinstance(value, Enum):
                value = value.value

            # Generate the API Key.
            key_parts = key.split("_")
            key = "".join(
                [key_parts[0]] + [key.capitalize() for key in key_parts[1:]]
            )

            class_dict[key] = value

        return class_dict
