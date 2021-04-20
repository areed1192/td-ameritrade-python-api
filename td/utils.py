from dataclasses import dataclass
from dataclasses import fields
from pprint import pprint
from typing import Union
from enum import Enum
from datetime import datetime
from datetime import date
from td.enums import ContractType
from td.enums import StrategyType
from td.enums import OptionaRange
from td.enums import OptionType
from td.enums import ContractType
from td.enums import ExpirationMonth


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


@dataclass
class OptionChainQuery():

    """
    ### Overview
    ----
    A python dataclass which is used to represent a query to the 
    Option Chain service on TD Ameritrade.

    ### Parameters
    ----
    symbol: str (optional, Default=None)
        A single symbol to return option chains for, keep in 
        mind only one symbol may be passed through.

    contract_type: Union[str, Enum] (optional, Default='all')
        Type of contracts to return in the chain. 
        Can be `call`, `put`, or `all`.

    strike_count: int (optional, Default=None)
        The number of strikes to return above and 
        below the at-the-money price.

    include_quotes: bool (optional, Default=False)
        If set to `True` real-time quotes will be provided
        otherwise none will be included.

    strategy: Union[str, Enum] (optional, Default='single')
        Passing a value returns a Strategy Chain. Possible values are 
        `single`, `analytical` (allows use of the volatility, underlyingPrice,
        interestRate, and daysToExpiration params to calculate theoretical
        values), `covered`, `vertical`, `calendar`, `strangle`, `straddle`,
        `butterfly`, `condor`, `diagonal`, `collar`, or `roll`.

    interval: str (optional, Default=None)
        Strike interval for spread strategy chains (see `strategy` param).

    strike: float (optional, Default=None)
        Provide a strike price to return options only at that
        strike price.

    opt_range: Union[str, Enum] (optional, Default='all')
        Returns options for the given range. Possible values are: 
        [(`itm`, In-the-money), (`ntm`: Near-the-money), (`otm`: Out-of-the-money), 
        (`sak`: Strikes Above Market), (`sbk`: Strikes Below Market)
        (`snk`: Strikes Near Market), (`all`: All Strikes)]

    from_date: Union[str, datetime] (optional, Default=None)
        Only return expirations after this date. For strategies, expiration 
        refers to the nearest term expiration in the strategy. Valid ISO-8601
        formats are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz.

    to_date: Union[str, datetime] (optional, Default=None)
        Only return expirations before this date. For strategies, expiration 
        refers to the nearest term expiration in the strategy. Valid ISO-8601
        formats are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz.

    volatility: str (optional, Default=None)
        Volatility to use in calculations. Applies only to `analytical` 
        strategy chains (see strategy param).

    underlying_price: str (optional, Default=None)
        Underlying price to use in calculations. Applies only to 
        `analytical` strategy chains (see strategy param).

    interest_rate: str (optional, Default=None)
        Interest rate to use in calculations. Applies only to 
        `analytical` strategy chains (see strategy param). Defaults to None.

    days_to_expiration: str (optional, Default=None)
        Days to expiration to use in calculations. Applies 
        only to `analytical` strategy chains (see strategy param).

    exp_month: str (optional, Default='all') 
        Return only options expiring in the specified month. Month 
        is given in the three character format. 

    option_type: Union[str, Enum] (optional, Default='all')
        Type of contracts to return. Possible values are: [(`s`: Standard contracts),
        (`ns`: Non-standard contracts), (`all`: All contracts)]
    """

    symbol: str
    contract_type: Union[str, Enum] = ContractType.All
    strike_count: int = None
    include_quotes: bool = False
    strategy: Union[str, Enum] = StrategyType.Single
    interval: int = None
    strike: float = None
    option_range: Union[str, Enum] = OptionaRange.All
    from_date: Union[str, datetime, date] = None
    to_date: Union[str, datetime, date] = None
    volatility: int = None
    underlying_price: float = None
    interest_rate: float = None
    days_to_expiration: int = None
    expiration_month: Union[str, Enum] = ExpirationMonth.All
    option_type: Union[str, Enum] = OptionType.All

    def to_dict(self, raise_errors: bool) -> dict:
        """Generates a dictionary containing all the field
        names and values.

        ### Returns
        ----
        dict
            The Field Name and Values.
        """

        self._raise_errors = raise_errors
        self._validate()

        keys_to_replace = {
            'option_range': 'range',
            'expiration_month': 'expMonth'
        }

        class_dict = {}

        # Loop through each field and grab the value and key.
        for field in fields(self):

            key = field.name
            value = getattr(self, field.name)

            # Handle values that could be Enums.
            if isinstance(value, Enum):
                value = value.value

            if isinstance(value, datetime) or isinstance(value, date):
                value = value.isoformat()

            # Generate the API Key.
            key_parts = key.split("_")
            key = "".join(
                [key_parts[0]] + [key.capitalize() for key in key_parts[1:]]
            )

            # Clean up the keys just to make sure they match the API.
            if key in keys_to_replace:
                key = keys_to_replace[key]

            class_dict[key] = value

        return class_dict

    def _validate(self) -> None:

        self._validate_strike_price()
        self._validate_strategy()

    def _validate_strike_price(self) -> None:
        """Validates the Strike Price of the option."""

        strike_price = getattr(self, 'strike')

        if strike_price:
            strike_price = round(strike_price, 2)
            setattr(self, 'strike', strike_price)

    def _validate_strategy(self) -> None:
        """Validates the Strategy of the option."""

        strategy = getattr(self, 'strategy')

        if isinstance(strategy, Enum):
            strategy = strategy.value
        elif strategy is not None:
            pass
        else:
            return

        if strategy == 'SINGLE':

            values_to_exclude = [
                'volatility',
                'underlying_price',
                'interest_rate',
                'days_to_expiration'
            ]

            for value in values_to_exclude:

                if self._raise_errors and getattr(self, value) is not None:
                    raise ValueError(
                        f"{value} cannot be set with strategy type SINGLE."
                    )
                else:
                    delattr(self, value)
