from enum import Enum
from typing import List
from typing import Dict
from typing import Union

from datetime import datetime
from collections import OrderedDict


class OptionChain():

    """
    TD Ameritrade API `OptionChain` Class.

    Overview:
    ----
    Implements the OptionChain object for helping users build,
    validate, and modify requests made to the `Get Option Chains`
    endpoint. Getting data from this endpoint can require passing through
    multiple arguments.

    That, if not specified correctly, can invalidate other ones previously 
    passed through. This Class will help valdiate those request as their 
    built and provide feedback to the user on how fix them if possible.
    """

    def __init__(self, symbol: str = None, contract_type: str = 'all', strike_count: int = None, include_quotes: bool = False, strategy: str = 'single',
                 interval: str = None, strike: float = None, opt_range: str = 'all', from_date: Union[str, datetime] = None, to_date: Union[str, datetime] = None,
                 volatility: str = None, underlying_price: str = None, interest_rate: str = None, days_to_expiration: str = None, exp_month: str = 'all',
                 option_type: str = 'all') -> None:
        """Initializes the `OptionChain` object.

        Overview:
        ----
        Initalizes the Option Chain Object and override any default 
        values that are passed through.

        Arguments:
        ----
        symbol (str, optional): A single symbol to return option chains for, 
            keep in mind only one symbol may be passed through. Defaults to None.

        contract_type (str, optional): 	Type of contracts to return in the chain. 
            Can be `call`, `put`, or `all`. Defaults to `all`.

        strike_count (int, optional): The number of strikes to return above and 
            below the at-the-money price. Defaults to None.

        include_quotes (bool, optional): Include quotes for options in the option chain. 
            Can be `True` or `False`. Defaults to False.

        strategy (str, optional): Passing a value returns a Strategy Chain. Possible values are 
            `single`, `analytical` (allows use of the volatility, underlyingPrice, interestRate, 
            and daysToExpiration params to calculate theoretical values), `covered`, `vertical`, 
            `calendar`, `strangle`, `straddle`, `butterfly`, `condor`, `diagonal`, `collar`, 
            or `roll`. Defaults to `single`.

        interval (str, optional): Strike interval for spread strategy 
            chains (see `strategy` param). Defaults to None.

        strike (float, optional): Provide a strike price to return options only at that
            strike price. Defaults to None.

        opt_range (str, optional): Returns options for the given range. 
            Possible values are: [(`itm`, In-the-money), (`ntm`: Near-the-money),
            (`otm`: Out-of-the-money), (`sak`: Strikes Above Market), (`sbk`: Strikes Below Market)
            (`snk`: Strikes Near Market), (`all`: All Strikes)
            Defaults to `all`.

        from_date (Union[str, datetime], optional): Only return expirations after this date. 
            For strategies, expiration refers to the nearest term expiration in the strategy. 
            Valid ISO-8601 formats are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz.Can either be
            a string or `datetime` object.
            Defaults to None.

        to_date (Union[str, datetime], optional): Only return expirations before this date. 
            For strategies, expiration refers to the nearest term expiration in the strategy. 
            Valid ISO-8601 formats are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz. Can either be
            a string or `datetime` object.
            Defaults to None.

        volatility (str, optional): Volatility to use in calculations. Applies only to `analytical` 
            strategy chains (see strategy param). Defaults to None.

        underlying_price (str, optional): Underlying price to use in calculations. Applies only to 
            `analytical` strategy chains (see strategy param). Defaults to None.

        interest_rate (str, optional): Interest rate to use in calculations. Applies only to 
            `analytical` strategy chains (see strategy param). Defaults to None.

        days_to_expiration (str, optional): Days to expiration to use in calculations. Applies 
            only to `analytical` strategy chains (see strategy param). Defaults to None.

        exp_month (str, optional): Return only options expiring in the specified month. Month 
            is given in the three character format. Example: `jan` Defaults to `all`. 

        option_type (str, optional): Type of contracts to return. Possible values are:
            [(`s`: Standard contracts), (`ns`: Non-standard contracts), (`all`: All contracts)]
            Defaults to `all`.

        Raises:
        ----
        KeyError: If the keyword argument can't be found it will
            raise a `KeyError`.
        """

        # The option chain will have multiple arguments you can assign to it, and each of those arguments has multiple possible values.
        # This dictionary, will help with argument, and argument_value validation. The layou is simple, create a dictionary where each
        # argument_name is the key, and the value is a list of possible values.
        self.argument_types = {
            'strategy': [
                'SINGLE', 'ANALYTICAL', 'COVERED',
                'VERTICAL', 'CALENDAR', 'STRANGLE',
                'STRADDLE', 'BUTTERFLY', 'CONDOR',
                'DIAGONAL', 'COLLAR', 'ROLL'
            ],
            'includeQuotes': ['TRUE', 'FALSE'],
            'range': ['ITM', 'NTM', 'OTM', 'SAK', 'SBK', 'SNK', 'ALL'],
            'expMonth': [
                'ALL', 'JAN', 'FEB',
                'MAR', 'APR', 'MAY',
                'JUN', 'JUL', 'AUG',
                'SEP', 'OCT', 'DEC'
            ],
            'optionType': ['S', 'NS', 'ALL']
        }

        # If a strike price is provided round it.
        if strike:
            strike = round(strike, 2)

        # Define a new dictionary to store the query arguments.
        self.query_parameters = {
            'symbol': symbol,
            'contractType': contract_type.upper(),
            'strikeCount': strike_count,
            'includeQuotes': include_quotes,
            'strategy': strategy.upper(),
            'interval': interval,
            'strike': strike,
            'range': opt_range.upper(),
            'fromDate': from_date,
            'toDate': to_date,
            'volatility': volatility,
            'underlyingPrice': underlying_price,
            'interestRate': interest_rate,
            'daysToExpiration': days_to_expiration,
            'expMonth': exp_month.upper(),
            'optionType': option_type.upper()
        }

        # Initialize the validation Flag.
        self.validated_arguments = False

    def _remove_empty_keys(self) -> None:
        """Removes the empty keys from the dictionary."""

        # Find the keys with a value of None.
        keys_to_remove = [
            key for key in self.query_parameters if not self.query_parameters[key]
        ]

        # Delete them.
        for key in keys_to_remove:
            del self.query_parameters[key]

    def validate_chain(self) -> bool:
        """This will validate the OptionChain argument_names and argument_values.

        Arguments:
        ----
        keyword_args (dict): A dictionary of keyword arguments provided 
            during initalization.

        Raises:
        ----
        KeyError: A key error if the key doesn't exist.

        Returns:
        ----
        (bool): `True` if the validation passes, `False` otherwise.
        """

        incorrect_val_msg = "The value {val} you assigned to field {key} is not valid, please provide one of the following valid values: {corr}"

        # First remove empty keys.
        self._remove_empty_keys()

        # An easy check is to see if they try to use an invalid parameter for the `strategy` argument.
        if 'strategy' in self.query_parameters.keys() and self.query_parameters['strategy'] == 'SINGLE':

            # The following values values should not be set
            values_to_exclude = [
                'volatility',
                'underlyingPrice',
                'interestRate',
                'daysToExpiration'
            ]

            # So delete them.
            for key_to_delete in values_to_exclude:
                if key_to_delete in self.query_parameters:
                    del self.query_parameters[key_to_delete]

        # If we didn't fail early then check the remainder of the values.
        for key, value in self.query_parameters.items():

            # Next step is to validate if the argument_value is valid.
            # Keep in mind though not every argument will have multiple possible values.
            if key in self.argument_types.keys() and (value not in self.argument_types[key]):
                raise KeyError(incorrect_val_msg.format(
                    val=value,
                    key=key,
                    corr=', '.join(self.argument_types[key])
                )
                )

        return True

    def _get_query_parameters(self) -> dict:
        """Returns only paramters needing to be validated.

        Overview:
        ----
        This will create a new dictionary, that only contains the 
        items that have a value not equal to None in the 
        `query_parameters` dictionary.

        Returns:
        ----
        dict: A filtered dictionary of the values needing
            validation.
        """

        # Keep only the values that are not none.
        new_dictionary = {
            key: value for key, value in self.query_parameters.items() if value != None
        }

        return new_dictionary

    def add_chain_key(self, key_name: str = None, key_value: str = None) -> None:
        """This method allows you to add a new key after initalization.

        Arguments:
        ----
        key_name (str, optional): The name of the key you wish to add.
            Defaults to None.

        key_value (str, optional): The value you want associated with the key. 
            Defaults to None.

        Raises:
        ----
        KeyError: If they are trying to add a key that doesn't exist, it
            will raise a `KeyError`.

        ValueError: If they are trying to assign a value that doesn't exist, it
            will raise a `ValueError`.
        """

        incorrect_key_msg = "The key {incorrect_val} you provided is invalid for the OptionChain Object please provide on of the following valid keys: {correct_vals}"
        incorrect_val_msg = "The value {incorrect_val} you provided for key {incorrect_key} is invalid for the OptionChain Object please provide on of the following valid values: {correct_vals}"
        correct_vals = ', '.join(self.query_parameters.keys())

        # validate the key can be used.
        if key_name not in self.query_parameters:
            raise KeyError(incorrect_key_msg.format(
                incorrect_val=key_name,
                correct_val=correct_vals
            )
            )

        # If possible, validate that the value can be used.
        if key_name in self.argument_types.keys() and key_value not in self.argument_types[key_name]:
            raise ValueError(incorrect_val_msg.format(
                incorrect_val=key_value,
                incorrect_key=key_name,
                correct_val=', '.join(self.argument_types[key_name])
            )
            )

        # Otherwise, add the key and the value to the query parameter dictionary.
        self.query_parameters[key_name] = key_value

    # def add_chain_enum(self, item=None):

    #     # for any Enum member
    #     if isinstance(item, Enum):
    #         item = item.name
