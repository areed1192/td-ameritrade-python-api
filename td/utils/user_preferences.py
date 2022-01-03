from dataclasses import dataclass
from dataclasses import fields
from typing import Union
from enum import Enum


@dataclass
class UserPreferences():

    """
    ### Overview
    ----
    A python dataclass which is used to represent the UserPreferences.
    TD Ameritrade has multiple preferences that can be adjusted by the
    user. To make the process of generating these complex dictionaries
    slightly easier you can use the `UserPreferences` object to store
    your values and then generate the proper dictionary needed for the
    API.
    """

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
        """Generates a dictionary containing all the field
        names and values.

        ### Returns
        ----
        dict
            The Field Name and Values.

        ### Usage
        ----
            >>> my_preferences = {
                'default_equity_order_leg_instruction': DefaultOrderLegInstruction.Buy,
                'default_equity_order_type': DefaultOrderType.Market,
                'default_equity_order_price_link_type': DefaultOrderPriceLinkType.Percent,
                'default_equity_order_duration': DefaultOrderDuration.NoneSpecified,
                'default_equity_order_market_session': DefaultOrderMarketSession.Normal,
                'mutual_fund_tax_lot_method': TaxLotMethod.Fifo,
                'option_tax_lot_method': TaxLotMethod.Fifo,
                'equity_tax_lot_method': TaxLotMethod.Fifo,
                'default_advanced_tool_launch': DefaultAdvancedToolLaunch.Ta,
                'auth_token_timeout': AuthTokenTimeout.EightHours
            }
            >>> my_user_perferences = UserPreferences(**my_preferences)
            >>> my_user_perferences.to_dict()
        """

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
