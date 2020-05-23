import json
from enum import Enum
from collections import OrderedDict


class OptionChain():

    '''
        TD Ameritrade API OptionChain Class.

        Implements the OptionChain object for helping users build,
        validate, and modify requests made to the `Get Option Chains`
        endpoint. Getting data from this endpoint can require passing through
        multiple arguments. 

        That, if not specified correctly, can invalidate other
        ones previously passed through. This Class will help valdiate those request
        as their built and provide feedback to the user on how fix them if possible.

    '''

    def __init__(self, **kwargs):
        '''
            Initalizes the Option Chain Object and override any default values that are
            passed through.
        '''

        # the option chain will have multiple arguments you can assign to it, and each of those arguments has multiple possible values.
        # this dictionary, will help with argument, and argument_value validation. The layou is simple, create a dictionary where each
        # argument_name is the key, and the value is a list of possible values.
        self.argument_types = {
            'strategy':  ['SINGLE', 'ANALYTICAL', 'COVERED', 'VERTICAL', 'CALENDAR', 'STRANGLE',
                          'STRADDLE', 'BUTTERFLY', 'CONDOR', 'DIAGONAL', 'COLLAR', 'ROLL'],
            'includeQuotes': ['TRUE', 'FALSE'],
            'range': ['ITM', 'NTM', 'OTM', 'SAK', 'SBK', 'SNK', 'ALL'],
            'expMonth': ['ALL', 'JAN', 'FEB', 'MAR', 'APR', 'MAY',
                         'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'DEC'],
            'optionType': ['S', 'NS', 'ALL']
        }

        # define the parameters that we will take when a new object is initalized.
        self.query_parameters = {
            'apikey': None,
            'symbol': None,
            'contractType': None,
            'strikeCount': None,
            'includeQuotes': None,
            'strategy': None,
            'interval': None,
            'strike': None,
            'range': None,
            'fromDate': None,
            'toDate': None,
            'volatility': None,
            'underlyingPrice': None,
            'interestRate': None,
            'daysToExpiration': None,
            'expMonth': None,
            'optionType': None
        }

        # THIS WILL BE A TWO STEP VALIDATION
        # Step One: Make sure none of the kwargs are invalid. No sense of trying to validate an incorrect argument.
        for key in kwargs:
            if key not in self.query_parameters:
                print("WARNING: The argument, {} is an unkown argument.".format(key))
                raise KeyError('Invalid Argument Name.')

        # Step Two: Validate the argument values, if good then update query parameters.
        if self.validate_chain(kwargs):
            self.query_parameters.update(kwargs.items())

    def validate_chain(self, keyword_args=None):
        '''
            This will validate the OptionChain argument_names and argument_values.

            NAME: keyword_args
            DESC: A dictionary of keyword arguments provided during initalization.
            TYPE: Dictionary

            RTYPE Boolean
        '''

        # An easy check is to see if they try to use an invalid parameter for the "strategy" argument.
        if 'strategy' in keyword_args.keys() and keyword_args['strategy'] == 'SINGLE':

            # The following values values should not be set
            values_to_exclude = [
                'volatility', 'underlyingPrice', 'interestRate', 'daysToExpiration']

            # validate all the keys are being used.
            all_keys = [key in keyword_args for key in values_to_exclude]

            # any will return TRUE if any of the values in the 'all_keys' list are FALSE.
            if any(all_keys):
                print('\nFor the "strategy" argument you specified "SINGLE", the following values must be excluded from the Option Chain: {} \n'.format(
                    ', '.join(values_to_exclude)))
                raise KeyError('Invalid Value.')

        # if we didn't fail early then check the remainder of the values.
        for key, value in keyword_args.items():

            # first make sure the argument_name is valid.
            if key in self.query_parameters.keys():

                # next step is to validate if the argument_value is valid. Keep in mind though not every argument will have multiple possible values.
                if (key in self.argument_types.keys() and (value not in self.argument_types[key])):
                    print('\nThe value "{}" you assigned to field "{}" is not valid, please provide one of the following valid values: {}\n'.format(
                        value, key, ', '.join(self.argument_types[key])))
                    raise KeyError('Invalid Field Value.')

            elif key not in self.query_parameters.keys():
                print(
                    'The argument "{}" passed through is invalid, please provide a valid argument.'.format(key))
                raise KeyError('Invalid Argument Name Value.')

        return True

    def _get_query_parameters(self):
        '''
            This will create a new dictionary, that only contains the items that have a value
            not equal to None in the query_parameters dictionary.

            RTYPE: Dictionary
        '''

        # keep only the values that are not none.
        new_dictionary = {key: value for key,
                          value in self.query_parameters.items() if value != None}

        return new_dictionary

    def add_chain_key(self, key_name=None, key_value=None):
        '''
            This method allows you to add a new key after initalization.

            NAME: key_name
            DESC: The name of the key you wish to add.
            TYPE: String

            NAME: key_value
            DESC: The value you want associated with the key.
            TYPE: String | Integer | Float
        '''

        # validate the key can be used.
        if key_name not in self.query_parameters:
            print('The key "{}" you provided is invalid for the OptionChain Object please provide on of the following valid keys: {}'.format(
                key_name, ', '.join(self.query_parameters.keys())))
            raise KeyError('Invalid Key Supplied.')

        # If possible, validate that the value can be used.
        if key_name in self.argument_types.keys() and key_value not in self.argument_types[key_name]:
            print('The value "{}" you provided for key {} is invalid for the OptionChain Object please provide on of the following valid values: {}'.format(
                key_value, key_name, ', '.join(self.argument_types[key_name])))
            raise ValueError('Invalid Value Supplied.')

        # otherwise add the key and the value to the query parameter dictionary.
        self.query_parameters[key_name] = key_value

    def add_chain_enum(self, item=None):

        # for any Enum member
        if isinstance(item, Enum):
            item = item.name
