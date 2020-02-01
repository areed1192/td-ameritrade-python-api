import json

class WatchlistItem():

    '''
        TD Ameritrade API WatchlistItem Class.

        Implements a the building and validation of Watchlist Item requests. These
        type of requests can take on multiple possible arguments, requires information to be
        nested, and only accepts a pure JSON string.

        This class will help the user build, validate and modify requests made to this endpoint.
    '''

    def __init__(self, **kwargs):
        '''
            Initalizes the WatchListItem Object and override any default values that are
            passed through.
        '''

        # argument types used for validation.
        self.argument_types = {
            'assetType':  ['EQUITY', 'OPTION', 'MUTUAL_FUND', 'FIXED_INCOME', 'INDEX']
        }

        # the possible parameters that can be set during initalization for a watchlist item.
        self.query_parameters = {
            'quantity': 0,
            'averagePrice': 0.00,
            'commission': 0.00,
            'purchasedDate': None,
            'symbol': None,
            'assetType': None
        }

        # THIS WILL BE A TWO STEP VALIDATION
        # Step One: Make sure none of the kwargs are invalid. No sense of trying to validate an incorrect argument.
        for key in kwargs:
            if key not in self.query_parameters:
                print("WARNING: The argument, {} is an unkown argument.".format(key))
                raise KeyError('Invalid Argument Name.')

        # Step Two: Validate the argument values, if good then update query parameters.
        if self.validate_watchlist(keyword_args=kwargs):
            self.query_parameters.update(kwargs.items())

    def validate_watchlist(self, keyword_args=None):
        '''
            A watchlist item can only have specifice values specified, if those values aren't specified
            then errors can happen. This method will validate the arguments passed through during initalization
            and raise an error if any of the values are incorrect.

            Watchlist are relatively simple to validate because the only argument we have to check is
            the `assetType`. However, additional validation protocals may be added in the future, so it's made
            more general.

            NAME: keyword_args
            DESC: A dictionary of keyword arguments provided during initalization.
            TYPE: Dictionary

            RTYPE Boolean
        '''

        # grab the items, if you find a key that needs validation, then compare to the list of possible values.
        for key, value in keyword_args.items():
            if (key in self.argument_types.keys()) and (value not in self.argument_types[key]):
                print('\nFor the "{}" argument you specified "{}", this is an invalid value. Please use one of the following value values: {} \n'.format(
                    key, value, ', '.join(self.argument_types[key])))
                raise KeyError('Invalid Value.')

        return True

    def create_watchlist_json(self):
        '''
            A watchlist request is prone to error because it requires building a nestsed JSON string. This
            method will automate that process and ensure everytime you want to send a request it will be in
            the right format. Additionally, it will convert the dictionary object to a JSON string.


            ALEX NOTES
            ----------

            REQUIRES MORE VALIDATION, MIGHT NOT NEED JSON STRING.

            I feel like this can be simplied, I don't like having to delete keys. Maybe see if you
            can modify initalization process so that it's already nested to begin with?

            Also, it might make sense to add a second round of validation in case the user has modified a value.
            Do something similiar to the OptionChain class that allows user to call a method that will modify
            arguments?


            RTYPE: String
        '''

        # grab the current arguments
        current_params = self.query_parameters

        # create the nested dictionary.
        instrument_dict = {
            'symbol': current_params['symbol'], 'assetType': current_params['assetType']}

        # delete the old values.
        del current_params['symbol']
        del current_params['assetType']

        # add the nested dict to the newly created `instrument` key.
        current_params['instrument'] = instrument_dict

        # make JSON string
        json_string = json.dumps(current_params)

        return json_string
