from dataclasses import dataclass
from dataclasses import fields
from typing import Union
from enum import Enum
from datetime import datetime
from datetime import date
from td.utils.enums import ContractType
from td.utils.enums import StrategyType
from td.utils.enums import OptionaRange
from td.utils.enums import OptionType
from td.utils.enums import ExpirationMonth


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

        ### Parameters
        ----
        raises_errors: bool
            If set to `True` will raise errors when
            validating the strategy. If `False` no validation
            errors will be raised.

        ### Returns
        ----
        dict
            The Field Name and Values.
        """

        self._validate(raise_errors=raise_errors)

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

    def _validate(self, raise_errors: bool) -> None:
        """Run the validation process."""

        self._validate_strike_price()
        self._validate_strategy(raise_errors=raise_errors)

    def _validate_strike_price(self) -> None:
        """Validates the Strike Price of the option."""

        strike_price = getattr(self, 'strike')

        if strike_price:
            strike_price = round(strike_price, 2)
            setattr(self, 'strike', strike_price)

    def _validate_strategy(self, raise_errors: bool) -> None:
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

                if raise_errors and getattr(self, value) is not None:
                    raise ValueError(
                        f"{value} cannot be set with strategy type SINGLE."
                    )

                delattr(self, value)
