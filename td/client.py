import os
import time
import json
import datetime
import requests
import urllib.parse
from td.orders import Order, OrderLeg
from td.stream import TDStreamerClient


class TDClient():

    '''
        TD Ameritrade API Client Class.

        Implements OAuth 2.0 Authorization Code Grant workflow, handles configuration
        and state management, adds token for authenticated calls, and performs request 
        to the TD Ameritrade API.
    '''

    def __init__(self, **kwargs):
        '''
            Initializes the session with default values and any user-provided overrides.

            The following arguments MUST be specified at runtime or else initalization
            will fail.

            NAME: consumer_id
            DESC: The Consumer ID assigned to you during the App registration. This can
                  be found at the app registration portal.

            NAME: account_number
            DESC: This is the account number for your main TD Ameritrade Account.

            NAME: account_password
            DESC: This is the account password for your main TD Ameritrade Account.

            NAME: redirect_uri
            DESC: This is the redirect URL that you specified when you created your
                  TD Ameritrade Application.

        '''

        # define the configuration settings.
        self.config = {'consumer_id': None,
                       'account_number': None,
                       'account_password': None,
                       'redirect_uri': None,
                       'resource': 'https://api.tdameritrade.com',
                       'api_version': '/v1',
                       'cache_state': True,
                       'json_path': None,
                       'authenticaiton_url': 'https://auth.tdameritrade.com',
                       'auth_endpoint': 'https://auth.tdameritrade.com' + '/auth?',
                       'token_endpoint': 'https://api.tdameritrade.com' + '/v1' + '/oauth2/token',
                       'refresh_enabled': True}

        # This serves as a mechanism to validate input parameters for the different endpoint arguments.
        self.endpoint_arguments = {
            'search_instruments': {'projection': ['symbol-search', 'symbol-regex', 'desc-search', 'desc-regex', 'fundamental']},
            'get_market_hours': {'markets': ['EQUITY', 'OPTION', 'FUTURE', 'BOND', 'FOREX']},
            'get_movers': {'market': ['$DJI', '$COMPX', '$SPX.X'],
                           'direction': ['up', 'down'],
                           'change': ['value', 'percent']},
            'get_user_principals': {'fields': ['streamerSubscriptionKeys', 'streamerConnectionInfo', 'preferences', 'surrogateIds']}
        }

        # loop through the key word arguments.
        for key in kwargs:

            # there may be a chance an unknown argument was pass through. Print a warning if this is the case.
            if key not in self.config:
                print("WARNING: The argument, {} is an unkown argument.".format(key))
                raise KeyError('Invalid Argument Name.')

        # update the configuration settings so they now contain the passed through value.
        self.config.update(kwargs.items())

        # call the state_manager method and update the state to init (initalized)
        self.state_manager('init')

        # define a new attribute called 'authstate' and initalize it to '' (Blank). This will be used by our login function.
        self.authstate = False

        # Initalize the client with no streaming session.
        self.streaming_session = None

    def __repr__(self):
        '''
            Defines the string representation of our TD Ameritrade Class instance.

            RTYPE: String
        '''

        # grab the logged in state.
        if self.state['loggedin']:
            logged_in_state = 'True'
        else:
            logged_in_state = 'False'

        # define the string representation
        str_representation = '<TDAmeritrade Client (logged_in = {}, authorized = {})>'.format(
            logged_in_state, self.authstate)

        return str_representation

    def headers(self, mode=None):
        ''' 
            Returns a dictionary of default HTTP headers for calls to TD Ameritrade API,
            in the headers we defined the Authorization and access token.

            NAME: mode            
            DESC: Defines the content-type for the headers dictionary.
            TYPE: String
        '''

        # grab the access token
        token = self.state['access_token']

        # create the headers dictionary
        headers = {'Authorization': f'Bearer {token}'}

        if mode == 'application/json':
            headers['Content-type'] = 'application/json'

        return headers

    def api_endpoint(self, url):
        '''
            Convert relative endpoint (e.g., 'quotes') to full API endpoint.

            NAME: url
            DESC: The URL that needs conversion to a full endpoint URL.
            TYPE: String

            RTYPE: String
        '''

        # if they pass through a valid url then, just use that.
        if urllib.parse.urlparse(url).scheme in ['http', 'https']:
            return url

        # otherwise build the URL
        return urllib.parse.urljoin(self.config['resource'] + self.config['api_version'] + "/", url.lstrip('/'))

    def state_manager(self, action):
        '''
            Manages the self.state dictionary. Initalize State will set
            the properties to their default value. Save will save the 
            current state if 'cache_state' is set to TRUE.

            NAME: action
            DESC: action argument must of one of the following:
                    'init' -- Initalize State.
                    'save' -- Save the current state.
            TYPE: String            
        '''

        # define the initalized state, these are the default values.
        initialized_state = {'access_token': None,
                             'refresh_token': None,
                             'access_token_expires_at': 0,
                             'refresh_token_expires_at': 0,
                             'authorization_url': None,
                             'redirect_code': None,
                             'token_scope': '',
                             'loggedin': False}

        # Grab the current directory of the client file, that way we can store the JSON file in the same folder.
        if self.config['json_path'] is not None:
            file_path = self.config['json_path']
        else:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            filename = 'TDAmeritradeState.json'
            file_path = os.path.join(dir_path, filename)

        # if the state is initalized
        if action == 'init':
            self.state = initialized_state

            # if they allowed for caching and the file exist, load the file.
            if self.config['cache_state'] and os.path.isfile(file_path):
                with open(file_path, 'r') as fileHandle:
                    self.state.update(json.load(fileHandle))

            # if they didnt allow for caching delete the file.
            elif not self.config['cache_state'] and os.path.isfile(os.path.join(dir_path, filename)):
                os.remove(file_path)

        # if they want to save it and have allowed for caching then load the file.
        elif action == 'save' and self.config['cache_state']:
            with open(file_path, 'w') as fileHandle:

                # build JSON string using dictionary comprehension.
                json_string = {key: self.state[key]
                               for key in initialized_state}
                json.dump(json_string, fileHandle)

    def login(self):
        '''
            Ask the user to authenticate  themselves via the TD Ameritrade Authentication Portal. This will
            create a URL, display it for the User to go to and request that they paste the final URL into
            command window.

            Once the user is authenticated the API key is valide for 90 days, so refresh tokens may be used
            from this point, up to the 90 days.
        '''

        # if caching is enabled then attempt silent authentication.
        if self.config['cache_state']:

            # if it was successful, the user is authenticated.
            if self.silent_sso():

                # update the authentication state
                self.authstate = 'Authenticated'

                return True

        # update the authentication state
        self.authstate = 'Authenticated'

        # prepare the payload to login
        data = {'response_type': 'code',
                'redirect_uri': self.config['redirect_uri'],
                'client_id': self.config['consumer_id'] + '@AMER.OAUTHAP'}

        # url encode the data.
        params = urllib.parse.urlencode(data)

        # build the full URL for the authentication endpoint.
        url = self.config['auth_endpoint'] + params

        # set the newly created 'authorization_url' key to the newly created url
        self.state['authorization_url'] = url

        # aks the user to go to the URL provided, they will be prompted to authenticate themsevles.
        print('Please go to URL provided authorize your account: {}'.format(
            self.state['authorization_url']))

        # ask the user to take the final URL after authentication and paste here so we can parse.
        my_response = input('Paste the full URL redirect here: ')

        # store the redirect URL
        self.state['redirect_code'] = my_response

        # this will complete the final part of the authentication process.
        self.grab_access_token()

    def logout(self):
        '''
            Clears the current TD Ameritrade Connection state.
        '''

        # change state to initalized so they will have to either get a
        # new access token or refresh token next time they use the API
        self.state_manager('init')

    def grab_access_token(self):
        '''
            Access token handler for AuthCode Workflow. This takes the
            authorization code parsed from the auth endpoint to call the
            token endpoint and obtain an access token.
        '''

        # Parse the URL
        url_dict = urllib.parse.parse_qs(self.state['redirect_code'])

        # Convert the values to a list.
        url_values = list(url_dict.values())

        # Grab the Code, which is stored in a list.
        url_code = url_values[0][0]

        # define the parameters of our access token post.
        data = {'grant_type': 'authorization_code',
                'client_id': self.config['consumer_id'],
                'access_type': 'offline',
                'code': url_code,
                'redirect_uri': self.config['redirect_uri']}

        # post the data to the token endpoint and store the response.
        token_response = requests.post(
            url=self.config['token_endpoint'], data=data, verify=True)

        # call the save_token method to save the access token.
        self.token_save(token_response)

        # update the state if the request was successful.
        if token_response and token_response.ok:
            self.state_manager('save')

    def silent_sso(self):
        '''
            Attempt a silent authentication, by checking whether current access token
            is valid and/or attempting to refresh it. Returns True if we have successfully 
            stored a valid access token.

            RTYPE: Boolean
        '''

        # if the current access token is not expired then we are still authenticated.
        if self.token_seconds(token_type='access_token') > 0:
            return True

        # if the refresh token is expired then you have to do a full login.
        elif self.token_seconds(token_type='refresh_token') <= 0:
            return False

        # if the current access token is expired then try and refresh access token.
        elif self.state['refresh_token'] and self.token_refresh():
            return True

        # More than likely a first time login, so can't do silent authenticaiton.
        return False

    def token_refresh(self):
        '''
            Refreshes the current access token.

            RTYPE: Boolean
        '''

        # build the parameters of our request
        data = {'client_id': self.config['consumer_id'] + '@AMER.OAUTHAP',
                'grant_type': 'refresh_token',
                'access_type': 'offline',
                'refresh_token': self.state['refresh_token']}

        # make a post request to the token endpoint
        response = requests.post(
            self.config['token_endpoint'], data=data, verify=True)

        # if there was an error go through the full authentication
        if response.status_code == 401:
            print('The Credentials you passed through are invalid.')
            return False
        elif response.status_code == 400:
            print('Validation was unsuccessful.')
            return False
        elif response.status_code == 500:
            print('The TD Server is experiencing an error, please try again later.')
            return False
        elif response.status_code == 403:
            print("You don't have access to this resource, cannot authenticate.")
            return False
        elif response.status_code == 503:
            print("The TD Server can't respond, please try again later.")
            return False
        else:
            # save the token and the state, since we now have a new access token that has a new expiration date.
            self.token_save(response)
            self.state_manager('save')
            return True

    def token_save(self, response):
        '''
            Parses an access token from the response of a POST request and saves it
            in the state dictionary for future use. Additionally, it will store the
            expiration time and the refresh token.

            NAME: response
            DESC: A response object recieved from the `token_refresh` or `grab_access_token`
                  methods.
            TYPE: requests.Response

            RTYPE: Boolean
        '''

        # parse the data.
        json_data = response.json()

        # make sure there is an access token before proceeding.
        if 'access_token' not in json_data:
            self.logout()
            return False

        # save the access token and refresh token
        self.state['access_token'] = json_data['access_token']
        self.state['refresh_token'] = json_data['refresh_token']

        # and the logged in status
        self.state['loggedin'] = True

        # store token expiration time
        self.state['access_token_expires_at'] = time.time() + \
            int(json_data['expires_in'])
        self.state['refresh_token_expires_at'] = time.time(
        ) + int(json_data['refresh_token_expires_in'])

        return True

    def token_seconds(self, token_type='access_token'):
        '''
            Return the number of seconds until the current access token or refresh token
            will expire. The default value is access token because this is the most commonly used
            token during requests.

            NAME: token_type
            DESC: The type of token you would like to determine lifespan for. Possible values are:
                  'access_token'
                  'refresh_token'
            TYPE: String

            RTYPE: Boolean
        '''

        # if needed check the access token.
        if token_type == 'access_token':

            # if the time to expiration is less than or equal to 0, return 0.
            if not self.state['access_token'] or time.time() >= self.state['access_token_expires_at']:
                return 0

            # else return the number of seconds until expiration.
            token_exp = int(
                self.state['access_token_expires_at'] - time.time())

        # if needed check the refresh token.
        elif token_type == 'refresh_token':

            # if the time to expiration is less than or equal to 0, return 0.
            if not self.state['refresh_token'] or time.time() >= self.state['refresh_token_expires_at']:
                return 0

            # else return the number of seconds until expiration.
            token_exp = int(
                self.state['refresh_token_expires_at'] - time.time())

        return token_exp

    def token_validation(self, nseconds=5):
        '''
            Verify the current access token is valid for at least N seconds, and
            if not then attempt to refresh it. Can be used to assure a valid token
            before making a call to the TD Ameritrade API.

            PARA: nseconds
            TYPE: integer
            DESC: The minimum number of seconds the token has to be valid for before
                  attempting to get a refresh token.
        '''

        if self.token_seconds(token_type='access_token') < nseconds and self.config['refresh_enabled']:
            self.token_refresh()

    '''
    ----------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------
    
        THIS BEGINS THE ALL ENDPOINTS PORTION.

    ----------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------
    '''

    def validate_arguments(self, endpoint=None, parameter_name=None, parameter_argument=None):
        '''
            This will validate an argument for the specified endpoint and raise an error if the argument
            is not valid. Can take both a list of arguments or a single argument.

            NAME: endpoint
            DESC: This is the endpoint name, and should line up exactly with the TD Ameritrade Client library.
            TYPE: String

            NAME: parameter_name
            DESC: An endpoint can have a parameter that needs to be passed through, this represents the name of
                  that parameter.
            TYPE: String

            NAME: parameter_argument
            DESC: The arguments being validated for the particular parameter name. This can either be a single value
                  or a list of values.
            TYPE: List<Strings> OR String


            EXAMPLES:

            WITH NO LIST:
            ------------------------------------------------------------
            api_endpoint = 'search_instruments'
            para_name = 'projection'
            para_args = 'fundamental'

            self.validate_arguments(endpoint = api_endpoint, 
                                    parameter_name = para_name, 
                                    parameter_argument = para_args)


            WITH LIST:
            ------------------------------------------------------------
            api_endpoint = 'get_market_hours'
            para_name = 'markets'
            para_args = ['FOREX', 'EQUITY']

            self.validate_arguments(endpoint = api_endpoint, 
                                    parameter_name = para_name, 
                                    parameter_argument = para_args)

        '''

        # grab the possible parameters for the endpoint.
        parameters_dictionary = self.endpoint_arguments[endpoint]

        # grab the parameter arguments, for the specified parameter name.
        parameter_possible_arguments = parameters_dictionary[parameter_name]

        # if it's a list then see if it matches any of the possible values.
        if type(parameter_argument) is list:

            # build the validation result list.
            validation_result = [
                argument not in parameter_possible_arguments for argument in parameter_argument]

            # if any of the results are FALSE then raise an error.
            if any(validation_result):
                print('\nThe value you passed through is not valid, please choose one of the following valid values: {} \n'.format(
                    ' ,'.join(parameter_possible_arguments)))
                raise ValueError('Invalid Value.')
            elif not any(validation_result):
                return True

        # if the argument isn't in the list of possible values, raise an error.
        elif parameter_argument not in parameter_possible_arguments:
            print('\nThe value you passed through is not valid, please choose one of the following valid values: {} \n'.upper(
            ).format(' ,'.join(parameter_possible_arguments)))
            raise ValueError('Invalid Value.')

        elif parameter_argument in parameter_possible_arguments:
            return True

    def prepare_arguments_list(self, parameter_list=None):
        '''
            Some endpoints can take multiple values for a parameter, this
            method takes that list and creates a valid string that can be 
            used in an API request. The list can have either one index or
            multiple indexes.

            NAME: parameter_list
            DESC: A list of paramater values assigned to an argument.
            TYPE: List

            EXAMPLE:

            SessionObject.prepare_arguments_list(parameter_list = ['MSFT', 'SQ'])

        '''

        # validate it's a list.
        if type(parameter_list) is list:

            # specify the delimeter and join the list.
            delimeter = ','
            parameter_list = delimeter.join(parameter_list)

        return parameter_list

    def get_quotes(self, instruments=None):
        '''

            Serves as the mechanism to make a request to the Get Quote and Get Quotes Endpoint.
            If one item is provided a Get Quote request will be made and if more than one item
            is provided then a Get Quotes request will be made.

            Documentation Link: https://developer.tdameritrade.com/quotes/apis

            NAME: instruments
            DESC: A list of different financial instruments.
            TYPE: List

            EXAMPLES:

            SessionObject.get_quotes(instruments = ['MSFT'])
            SessionObject.get_quotes(instruments = ['MSFT','SQ'])

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # because we have a list argument, prep it for the request.
        instruments = self.prepare_arguments_list(parameter_list=instruments)

        # build the params dictionary
        data = {'apikey': self.config['consumer_id'],
                'symbol': instruments}

        # define the endpoint
        endpoint = '/marketdata/quotes'

        # build the url
        url = self.api_endpoint(endpoint)

        # return the response of the get request.
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()

    def get_price_history(self, symbol=None, periodType=None, period=None, startDate=None, endDate=None,
                          frequencyType=None, frequency=None,  needExtendedHoursData=None):
        '''
            STILL BUILDING

            NAME: symbol
            DESC: The ticker symbol to request data for. 
            TYPE: String

            NAME: periodType
            DESC: The type of period to show. Valid values are day, month, year, or ytd (year to date). Default is day.
            TYPE: String

            NAME: period
            DESC: The number of periods to show.
            TYPE: Integer

            NAME: startDate
            DESC: Start date as milliseconds since epoch.
            TYPE: Integer

            NAME: endDate
            DESC: End date as milliseconds since epoch.
            TYPE: Integer

            NAME: frequencyType
            DESC: The type of frequency with which a new candle is formed.
            TYPE: String

            NAME: frequency
            DESC: The number of the frequencyType to be included in each candle.
            TYPE: Integer

            NAME: needExtendedHoursData
            DESC: True to return extended hours data, false for regular market hours only. Default is true
            TYPE: Boolean

        '''

        # Validator function for get_price_history
        def validate(data):

            # Valid periods by periodType
            valid_periods = {
                'day': [1, 2, 3, 4, 5, 10],
                'month': [1, 2, 3, 6],
                'year': [1, 2, 3, 5, 10, 15, 20],
                'ytd': [1],
            }

            # Valid frequencyType by period
            valid_frequency_types = {
                'day': ['minute'],
                'month': ['daily', 'weekly'],
                'year': ['daily', 'weekly', 'monthly'],
                'ytd': ['daily', 'weekly'],
            }

            # Valid frequency by frequencyType
            valid_frequencies = {
                'minute': [1, 5, 10, 15, 30],
                'daily': [1],
                'weekly': [1],
                'monthly': [1]
            }

            # check data to confirm that either period or date range is provided
            if (data['startDate'] and data['endDate'] and not data['period']) or (not data['startDate'] and not data['endDate'] and data['period']):

                # Validate periodType
                if data['periodType'] not in valid_periods.keys():
                    print('Period Type: {} is not valid. Valid values are {}'.format(
                        data['periodType'], valid_periods.keys()))
                    raise ValueError('Invalid Value')

                # Validate period
                if data['period'] and data['period'] not in valid_periods[data['periodType']]:
                    print('Period: {} is not valid. Valid values are {}'.format(
                        data['period'], valid_periods[data['periodType']]))
                    raise ValueError('Invalid Value')

                # Validate frequencyType by frenquency
                if data['frequencyType'] not in valid_frequencies.keys():
                    print('frequencyType: {} is not valid. Valid values are {}'.format(
                        data['frequencyType'],  valid_frequencies.keys()))
                    raise ValueError('Invalid Value')

                # Validate frequencyType by periodType
                if data['frequencyType'] not in valid_frequency_types[data['periodType']]:
                    print('frequencyType: {} is not valid. Valid values for period: {} are {}'.format(
                        data['frequencyType'], data['periodType'], valid_frequency_types[data['periodType']]))
                    raise ValueError('Invalid Value')

                # Validate periodType
                if data['frequency'] not in valid_frequencies[data['frequencyType']]:
                    print('frequency: {} is not valid. Valid values are {}'.format(
                        data['frequency'], valid_frequencies[data['frequencyType']]))
                    raise ValueError('Invalid Value')

                # TODO Validate startDate and endDate

                # Recompute payload dictionary and remove any None values
                return({k: v for k, v in data.items() if v is not None})

            else:
                print('Either startDate/endDate or period must be provided exclusively.')
                raise ValueError('Invalid Value')

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # build the params dictionary
        data = {'apikey': self.config['consumer_id'],
                'period': period,
                'periodType': periodType,
                'startDate': startDate,
                'endDate': endDate,
                'frequency': frequency,
                'frequencyType': frequencyType,
                'needExtendedHoursData': needExtendedHoursData}

        # define the endpoint
        endpoint = '/marketdata/{}/pricehistory'.format(symbol)

        # validate the data
        data = validate(data)

        # build the url
        url = self.api_endpoint(endpoint)

        # return the response of the get request.
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()

    def search_instruments(self, symbol=None, projection='symbol-search'):
        '''
            Search or retrieve instrument data, including fundamental data.

            Documentation Link: https://developer.tdameritrade.com/instruments/apis/get/instruments

            NAME: symbol
            DESC: The symbol of the financial instrument you would like to search.
            TYPE: string

            NAME: projection
            DESC: The type of request, default is "symbol-search". The type of request include the following:

                  1. symbol-search
                     Retrieve instrument data of a specific symbol or cusip

                  2. symbol-regex
                     Retrieve instrument data for all symbols matching regex. 
                     Example: symbol=XYZ.* will return all symbols beginning with XYZ

                  3. desc-search
                     Retrieve instrument data for instruments whose description contains 
                     the word supplied. Example: symbol=FakeCompany will return all 
                     instruments with FakeCompany in the description

                  4. desc-regex
                     Search description with full regex support. Example: symbol=XYZ.[A-C] 
                     returns all instruments whose descriptions contain a word beginning 
                     with XYZ followed by a character A through C

                  5. fundamental
                     Returns fundamental data for a single instrument specified by exact symbol.

            TYPE: string

            EXAMPLES:

            SessionObject.search_instrument(symbol = 'XYZ', projection = 'symbol-search')
            SessionObject.search_instrument(symbol = 'XYZ.*', projection = 'symbol-regex')
            SessionObject.search_instrument(symbol = 'FakeCompany', projection = 'desc-search')
            SessionObject.search_instrument(symbol = 'XYZ.[A-C]', projection = 'desc-regex')
            SessionObject.search_instrument(symbol = 'XYZ.[A-C]', projection = 'fundamental')

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # validate argument
        self.validate_arguments(endpoint='search_instruments',
                                parameter_name='projection', parameter_argument=projection)

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # build the params dictionary
        data = {'apikey': self.config['consumer_id'],
                'symbol': symbol,
                'projection': projection}

        # define the endpoint
        endpoint = '/instruments'

        # build the url
        url = self.api_endpoint(endpoint)

        # return the response of the get request.
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()

    def get_instruments(self, cusip=None):
        '''
            Get an instrument by CUSIP (Committee on Uniform Securities Identification Procedures) code.

            Documentation Link: https://developer.tdameritrade.com/instruments/apis/get/instruments/%7Bcusip%7D

            NAME: cusip
            DESC: The CUSIP code of a given financial instrument.
            TYPE: string

            EXAMPLES:

            SessionObject.get_instruments(cusip = 'SomeCUSIPNumber')
        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # build the params dictionary
        data = {'apikey': self.config['consumer_id']}

        # define the endpoint
        endpoint = '/instruments'

        # build the url
        url = self.api_endpoint(endpoint) + "/" + cusip

        # return the response of the get request.
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()

    def get_market_hours(self, markets=None, date=None):
        '''
            Serves as the mechanism to make a request to the "Get Hours for Multiple Markets" and 
            "Get Hours for Single Markets" Endpoint. If one market is provided a "Get Hours for Single Markets" 
            request will be made and if more than one item is provided then a "Get Hours for Multiple Markets" 
            request will be made.

            Documentation Link: https://developer.tdameritrade.com/market-hours/apis

            NAME: markets
            DESC: The markets for which you're requesting market hours, comma-separated. 
                  Valid markets are EQUITY, OPTION, FUTURE, BOND, or FOREX.
            TYPE: List<Strings>

            NAME: date
            DESC: The date you wish to recieve market hours for. Valid ISO-8601 formats 
                  are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz
            TYPE: String

            EXAMPLES:

            SessionObject.get_market_hours(markets = ['EQUITY'], date = '2019-10-19')
            SessionObject.get_market_hours(markets = ['EQUITY','FOREX'], date = '2019-10-19')
        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # validate argument
        self.validate_arguments(endpoint='get_market_hours',
                                parameter_name='markets', parameter_argument=markets)

        # because we have a list argument, prep it for the request.
        markets = self.prepare_arguments_list(parameter_list=markets)

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # build the params dictionary
        data = {'apikey': self.config['consumer_id'],
                'markets': markets,
                'date': date}

        # define the endpoint
        endpoint = '/marketdata/hours'

        # build the url
        url = self.api_endpoint(endpoint)

        # return the response of the get request.
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()

    def get_movers(self, market=None, direction=None, change=None):
        '''
            Top 10 (up or down) movers by value or percent for a particular market.

            Documentation Link: https://developer.tdameritrade.com/movers/apis/get/marketdata

            NAME: market
            DESC: The index symbol to get movers for. Can be $DJI, $COMPX, or $SPX.X.
            TYPE: String

            NAME: direction
            DESC: To return movers with the specified directions of up or down. Valid values
                  are up or down
            TYPE: String

            NAME: change
            DESC: To return movers with the specified change types of percent or value Valid
                  values are percent or value.   
            TYPE: String

            EXAMPLES:

            SessionObject.get_movers(market = '$DJI', direction = 'up', change = 'value')
            SessionObject.get_movers(market = '$COMPX', direction = 'down', change = 'percent')           

        '''

        # grabs a dictionary representation of our arguments and their inputs.
        local_args = locals()

        # we don't need the 'self' key
        del local_args['self']

        # first make sure that the token is still valid.
        self.token_validation()

        # validate arguments, before making request.
        for key, value in local_args.items():
            self.validate_arguments(
                endpoint='get_movers', parameter_name=key, parameter_argument=value)

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # build the params dictionary
        data = {'apikey': self.config['consumer_id'],
                'direction': direction,
                'change': change}

        # define the endpoint
        endpoint = '/marketdata/{}/movers'.format(market)

        # build the url
        url = self.api_endpoint(endpoint)

        # return the response of the get request.
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()

    def get_options_chain(self, option_chain=None, args_dictionary=None):
        '''
            Get option chain for an optionable Symbol using one of two methods. Either,
            use the OptionChain object which is a built-in object that allows for easy creation of the
            POST request. Otherwise, can pass through a dictionary of all the arguments needed.

            Documentation Link: https://developer.tdameritrade.com/option-chains/apis/get/marketdata/chains

            NAME: option_chain
            DESC: Represents a single OptionChainObject.
            TYPE: TDAmeritrade.OptionChainObject

            EXAMPLE:

            from td.option_chain import OptionChain

            option_chain_1 = OptionChain(args)

            SessionObject.get_options_chain( option_chain = option_chain_1)

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # define the endpoint
        endpoint = '/marketdata/chains'

        # build the url
        url = self.api_endpoint(endpoint)

        # Grab the items needed for the request.
        if option_chain is not None:

            # this request requires an API key, so let's add that.
            option_chain.add_chain_key(
                key_name='apikey', key_value=self.config['consumer_id'])

            # take the JSON representation of the string
            data = option_chain._get_query_parameters()

        else:

            # otherwise take the args dictionary.
            data = args_dictionary

        # return the response of the get request.
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()

    '''
    ----------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------
    
        THIS BEGINS THE ACCOUNTS ENDPOINTS PORTION.

    ----------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------
    '''

    def get_accounts(self, account='all', fields=None):
        '''
            Serves as the mechanism to make a request to the "Get Accounts" and "Get Account" Endpoint. 
            If one account is provided a "Get Account" request will be made and if more than one account 
            is provided then a "Get Accounts" request will be made.

            Documentation Link: https://developer.tdameritrade.com/account-access/apis

            NAME: account
            DESC: The account number you wish to recieve data on. Default value is 'all'
                  which will return all accounts of the user.
            TYPE: String

            NAME: fields
            DESC: Balances displayed by default, additional fields can be added here by 
                  adding positions or orders.
            TYPE: List<String>

            EXAMPLES:

            SessionObject.get_accounts(account = 'all', fields = ['orders'])
            SessionObject.get_accounts(account = 'MyAccountNumber', fields = ['orders','positions'])

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # because we have a list argument, prep it for the request.
        fields = self.prepare_arguments_list(parameter_list=fields)

        # build the params dictionary
        data = {'apikey': self.config['consumer_id'],
                'fields': fields}

        # if all use '/accounts' else pass through the account number.
        if account == 'all':
            endpoint = '/accounts'
        else:
            endpoint = '/accounts/{}'.format(account)

        # build the url
        url = self.api_endpoint(endpoint)

        # return the response of the get request.
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()

    '''
    ----------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------
    
        THIS BEGINS THE TRANSACTIONS ENDPOINTS PORTION.

    ----------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------
    '''

    def get_transactions(self, account=None, transaction_type=None, symbol=None,
                         start_date=None, end_date=None, transaction_id=None):
        '''
            Serves as the mechanism to make a request to the "Get Transactions" and "Get Transaction" Endpoint. 
            If one `transaction_id` is provided a "Get Transaction" request will be made and if it is not provided
            then a "Get Transactions" request will be made.

            Documentation Link: https://developer.tdameritrade.com/transaction-history/apis

            NAME: account
            DESC: The account number you wish to recieve transactions for.
            TYPE: String

            NAME: transaction_type
            DESC: The type of transaction. Only transactions with the specified type will be returned. Valid
                  values are the following: ALL, TRADE, BUY_ONLY, SELL_ONLY, CASH_IN_OR_CASH_OUT, CHECKING,
                                            DIVIDEND, INTEREST, OTHER, ADVISOR_FEES
            TYPE: String

            NAME: symbol
            DESC: The symbol in the specified transaction. Only transactions with the specified 
                  symbol will be returned.
            TYPE: String

            NAME: start_date
            DESC: Only transactions after the Start Date will be returned. Note: The maximum date range is 
                  one year. Valid ISO-8601 formats are: yyyy-MM-dd.
            TYPE: String

            NAME: end_date
            DESC: Only transactions before the End Date will be returned. Note: The maximum date range is 
                  one year. Valid ISO-8601 formats are: yyyy-MM-dd.
            TYPE: String

            NAME: transaction_id
            DESC: The transaction ID you wish to search. If this is specifed a "Get Transaction" request is
                  made. Should only be used if you wish to return one transaction.
            TYPE: String

            EXAMPLES:

            SessionObject.get_transactions(account = 'MyAccountNumber', transaction_type = 'ALL', start_date = '2019-01-31', end_date = '2019-04-28')
            SessionObject.get_transactions(account = 'MyAccountNumber', transaction_type = 'ALL', start_date = '2019-01-31')
            SessionObject.get_transactions(account = 'MyAccountNumber', transaction_type = 'TRADE')
            SessionObject.get_transactions(transaction_id = 'MyTransactionID')

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # default to a "Get Transaction" Request if anything else is passed through along with the transaction_id.
        if transaction_id != None:
            account = None
            transaction_type = None,
            start_date = None,
            end_date = None

        # if the request type they made isn't valid print an error and return nothing.
        else:

            if transaction_type not in ['ALL', 'TRADE', 'BUY_ONLY', 'SELL_ONLY', 'CASH_IN_OR_CASH_OUT', 'CHECKING', 'DIVIDEND', 'INTEREST', 'OTHER', 'ADVISOR_FEES']:
                print('The type of transaction type you specified is not valid.')
                return False

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # if transaction_id is not none, it means we need to make a request to the get_transaction endpoint.
        if transaction_id:

            # define the endpoint
            endpoint = '/accounts/{}/transactions/{}'.format(
                account, transaction_id)

            # build the url
            url = self.api_endpoint(endpoint)

            # return the response of the get request.
            return requests.get(url=url, headers=merged_headers, verify=True).json()

        # if it isn't then we need to make a request to the get_transactions endpoint.
        else:

            # build the params dictionary
            data = {'type': transaction_type,
                    'symbol': symbol,
                    'startDate': start_date,
                    'endDate': end_date}

            # define the endpoint
            endpoint = '/accounts/{}/transactions'.format(account)

            # build the url
            url = self.api_endpoint(endpoint)

            # return the response of the get request.
            return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()

    '''
    ----------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------
    
        THIS BEGINS THE USER INFOS & PREFERENCES ENDPOINTS PORTION.

    ----------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------
    '''

    def get_preferences(self, account=None):
        '''
            Get's User Preferences for a specific account.

            Documentation Link: https://developer.tdameritrade.com/user-principal/apis/get/accounts/%7BaccountId%7D/preferences-0

            NAME: account
            DESC: The account number you wish to recieve preference data for.
            TYPE: String

            EXAMPLES:

            SessionObject.get_preferences(account = 'MyAccountNumber')
        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # define the endpoint
        endpoint = '/accounts/{}/preferences'.format(account)

        # build the url
        url = self.api_endpoint(endpoint)

        # return the response of the get request.
        return requests.get(url=url, headers=merged_headers, verify=True).json()

    def get_streamer_subscription_keys(self, accounts=None):
        '''
            SubscriptionKey for provided accounts or default accounts.

            Documentation Link: https://developer.tdameritrade.com/user-principal/apis/get/userprincipals/streamersubscriptionkeys-0

            NAME: account
            DESC: A list of account numbers you wish to recieve a streamer key for.
            TYPE: List<String>

            EXAMPLES:

            SessionObject.get_streamer_subscription_keys(account = ['MyAccountNumber'])
            SessionObject.get_streamer_subscription_keys(account = ['MyAccountNumber1', 'MyAccountNumber2'])

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # because we have a list argument, prep it for the request.
        accounts = self.prepare_arguments_list(parameter_list=accounts)

        # define the endpoint
        endpoint = '/userprincipals/streamersubscriptionkeys'

        # build the params dictionary
        data = {'accountIds': accounts}

        # build the url
        url = self.api_endpoint(endpoint)

        # return the response of the get request.
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()

    def get_user_principals(self, fields=None):
        '''
            Returns User Principal details.

            Documentation Link: https://developer.tdameritrade.com/user-principal/apis/get/userprincipals-0

            NAME: fields
            DESC: A comma separated String which allows one to specify additional fields to return. None of 
                  these fields are returned by default. Possible values in this String can be:

                    1. streamerSubscriptionKeys
                    2. streamerConnectionInfo
                    3. preferences
                    4. surrogateIds
            TYPE: List<String>

            EXAMPLES:

            SessionObject.get_user_principals(fields = ['preferences'])
            SessionObject.get_user_principals(fields = ['preferences', 'streamerConnectionInfo'])
        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # validate arguments
        self.validate_arguments(endpoint='get_user_principals',
                                parameter_name='fields', parameter_argument=fields)

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # because we have a list argument, prep it for the request.
        fields = self.prepare_arguments_list(parameter_list=fields)

        # define the endpoint
        endpoint = '/userprincipals'

        # build the params dictionary
        data = {'fields': fields}

        # build the url
        url = self.api_endpoint(endpoint)

        # return the response of the get request.
        return requests.get(url=url, headers=merged_headers, params=data, verify=True).json()

    def update_preferences(self, account=None, dataPayload=None):
        '''
            Update preferences for a specific account. Please note that the directOptionsRouting and 
            directEquityRouting values cannot be modified via this operation.

            Documentation Link: https://developer.tdameritrade.com/user-principal/apis/put/accounts/%7BaccountId%7D/preferences-0

            NAME: account
            DESC: The account number you wish to update preferences for.
            TYPE: String

            NAME: dataPayload
            DESC: A dictionary that provides all the keys you wish to update. It must contain the following keys to be valid.

                  1. expressTrading
                  2. directOptionsRouting
                  3. directEquityRouting
                  4. defaultEquityOrderLegInstruction
                  5. defaultEquityOrderType
                  6. defaultEquityOrderPriceLinkType
                  7. defaultEquityOrderDuration
                  8. defaultEquityOrderMarketSession
                  9. defaultEquityQuantity
                  10. mutualFundTaxLotMethod
                  11. optionTaxLotMethod
                  12. equityTaxLotMethod
                  13. defaultAdvancedToolLaunch
                  14. authTokenTimeout
            TYPE: dictionary

            EXAMPLES:

            SessionObject.update_preferences(account = 'MyAccountNumer', dataPayload = <Dictionary>)

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()
        merged_headers['Content-Type'] = 'application/json'

        # define the endpoint
        endpoint = '/accounts/{}/preferences'.format(account)

        # build the url
        url = self.api_endpoint(endpoint)

        # make the request
        response = requests.put(
            url=url, headers=merged_headers, data=json.dumps(dataPayload), verify=True)

        if response.status_code == 204:
            return "Data successfully updated."
        else:
            return response.content

    '''
    ----------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------
    
        THIS BEGINS THE WATCHLISTS ENDPOINTS PORTION.

    ----------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------
    '''

    def create_watchlist(self, account=None, name=None, watchlistItems=None):
        '''
            Create watchlist for specific account. This method does not verify that the symbol or asset type are valid.

            Documentation Link: https://developer.tdameritrade.com/watchlist/apis/post/accounts/%7BaccountId%7D/watchlists-0

            NAME: account
            DESC: The account number you wish to create the watchlist for.
            TYPE: String

            NAME: name
            DESC: The name you want to give your watchlist.
            TYPE: String

            NAME: watchlistItems
            DESC: A list of WatchListItems object.
            TYPE: List<WatchListItems>

            EXAMPLES:

            WatchListItem1 = WatchListItem()
            WatchListItem2 = WatchListItem()

            SessionObject.create_watchlist(account = 'MyAccountNumber', 
                                           name = 'MyWatchlistName', 
                                           watchlistItems = [ WatchListItem1, WatchListItem2 ])

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()
        merged_headers['Content-Type'] = 'application/json'

        # define the endpoint
        endpoint = '/accounts/{}/watchlists'.format(account)

        # define the payload
        payload = {"name": name, "watchlistItems": watchlistItems}

        # build the url
        url = self.api_endpoint(endpoint)

        # make the request
        response = requests.post(
            url=url, headers=merged_headers, data=json.dumps(payload), verify=True)

        if response.status_code == 201:
            return "Watchlist {} was successfully created.".format(name)
        else:
            return response.content

    def get_watchlist_accounts(self, account='all'):
        '''
            Serves as the mechanism to make a request to the "Get Watchlist for Single Account" and 
            "Get Watchlist for Multiple Accounts" Endpoint. If one account is provided a 
            "Get Watchlist for Single Account" request will be made and if 'all' is provided then a 
            "Get Watchlist for Multiple Accounts" request will be made.

            Documentation Link: https://developer.tdameritrade.com/watchlist/apis

            NAME: account
            DESC: The account number you wish to pull watchlists from. Default value is 'all'
            TYPE: String

            EXAMPLES:

            SessionObject.get_watchlist_accounts(account = 'all')
            SessionObject.get_watchlist_accounts(account = 'MyAccount1')

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # define the endpoint
        if account == 'all':
            endpoint = '/accounts/watchlists'
        else:
            endpoint = '/accounts/{}/watchlists'.format(account)

        # build the url
        url = self.api_endpoint(endpoint)

        # make the request
        return requests.get(url=url, headers=merged_headers, verify=True).json()

    def get_watchlist(self, account=None, watchlist_id=None):
        '''
            Returns a specific watchlist for a specific account.

            Documentation Link: https://developer.tdameritrade.com/watchlist/apis/get/accounts/%7BaccountId%7D/watchlists/%7BwatchlistId%7D-0

            NAME: account
            DESC: The account number you wish to pull watchlists from.
            TYPE: String

            NAME: watchlist_id
            DESC: The ID of the watchlist you wish to return.
            TYPE: String

            EXAMPLES:

            SessionObject.get_watchlist(account = 'MyAccount1', watchlist_id = 'MyWatchlistId')

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # define the endpoint
        endpoint = '/accounts/{}/watchlists/{}'.format(account, watchlist_id)

        # build the url
        url = self.api_endpoint(endpoint)

        # make the request
        return requests.get(url=url, headers=merged_headers, verify=True).json()

    def delete_watchlist(self, account=None, watchlist_id=None):
        '''

            Deletes a specific watchlist for a specific account.

            Documentation Link: https://developer.tdameritrade.com/watchlist/apis/delete/accounts/%7BaccountId%7D/watchlists/%7BwatchlistId%7D-0

            NAME: account
            DESC: The account number you wish to delete the watchlist from.
            TYPE: String

            NAME: watchlist_id
            DESC: The ID of the watchlist you wish to delete.
            TYPE: String

            EXAMPLES:

            SessionObject.delete_watchlist(account = 'MyAccount1', watchlist_id = 'MyWatchlistId')

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # define the endpoint
        endpoint = '/accounts/{}/watchlists/{}'.format(account, watchlist_id)

        # build the url
        url = self.api_endpoint(endpoint)

        # make the request
        return requests.delete(url=url, headers=merged_headers, verify=True).status_code

    def update_watchlist(self, account=None, watchlist_id=None, name=None, watchlistItems=None):
        '''

            Partially update watchlist for a specific account: change watchlist name, add to the beginning/end of a 
            watchlist, update or delete items in a watchlist. This method does not verify that the symbol or asset 
            type are valid.

            Documentation Link: https://developer.tdameritrade.com/watchlist/apis/patch/accounts/%7BaccountId%7D/watchlists/%7BwatchlistId%7D-0

            NAME: account
            DESC: The account number that contains the watchlist you wish to update.
            TYPE: String

            NAME: watchlist_id
            DESC: The ID of the watchlist you wish to update.
            TYPE: String

            NAME: watchlistItems
            DESC: A list of the original watchlist items you wish to update and their modified keys.
            TYPE: List<WatchListItems>            

            EXAMPLES:

            WatchListItem1 = WatchListItem()
            WatchListItem2 = WatchListItem()

            SessionObject.update_watchlist(account = 'MyAccountNumber', 
                                           watchlist_id = 'WatchListID', 
                                           watchlistItems = [ WatchListItem1, WatchListItem2 ])

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()
        merged_headers['Content-Type'] = 'application/json'

        # define the payload
        payload = {"name": name, "watchlistItems": watchlistItems}

        # define the endpoint
        endpoint = '/accounts/{}/watchlists/{}'.format(account, watchlist_id)

        # build the url
        url = self.api_endpoint(endpoint)

        # make the request
        return requests.patch(url=url, headers=merged_headers, data=json.dumps(payload),  verify=True).status_code

    def replace_watchlist(self, account=None, watchlist_id_new=None, watchlist_id_old=None, name_new=None, watchlistItems_new=None):
        '''
            STILL BUILDING

            Replace watchlist for a specific account. This method does not verify that the symbol or asset type are valid.

            Documentation Link: https://developer.tdameritrade.com/watchlist/apis/put/accounts/%7BaccountId%7D/watchlists/%7BwatchlistId%7D-0

            NAME: account
            DESC: The account number that contains the watchlist you wish to replace.
            TYPE: String

            NAME: watchlist_id_new
            DESC: The ID of the watchlist you wish to replace with the old one.
            TYPE: String

            NAME: watchlist_id_old
            DESC: The ID of the watchlist you wish to replace.
            TYPE: String

            NAME: name_new
            DESC: The name of the new watchlist.
            TYPE: String

            NAME: watchlistItems_New
            DESC: The new watchlist items you wish to add to the watchlist.
            TYPE: List<WatchListItems>            

            EXAMPLES:

            WatchListItem1 = WatchListItem()
            WatchListItem2 = WatchListItem()

            SessionObject.replace_watchlist(account = 'MyAccountNumber', 
                                            watchlist_id_new = 'WatchListIDNew', 
                                            watchlist_id_old = 'WatchListIDOld', 
                                            name_new = 'MyNewName', 
                                            watchlistItems_new = [ WatchListItem1, WatchListItem2 ])

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()
        merged_headers['Content-Type'] = 'application/json'

        # define the payload
        payload = {"name": name_new, "watchlistId": watchlist_id_new,
                   "watchlistItems": watchlistItems_new}

        # define the endpoint
        endpoint = '/accounts/{}/watchlists/{}'.format(
            account, watchlist_id_old)

        # build the url
        url = self.api_endpoint(endpoint)

        # make the request
        return requests.put(url=url, headers=merged_headers, data=json.dumps(payload),  verify=True).status_code

    '''
    ----------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------

        THIS BEGINS THE ORDERS ENDPOINTS PORTION.

    ----------------------------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------------------------
    '''

    def get_orders_path(self, account=None, max_results=None, from_entered_time=None, to_entered_time=None, status=None):
        '''
            Returns the orders for a specific account.

            Documentation Link: https://developer.tdameritrade.com/account-access/apis/get/accounts/%7BaccountId%7D/orders-0

            NAME: account
            DESC: The account number that you want to query for orders.
            TYPE: String

            NAME: max_results
            DESC: The maximum number of orders to retrieve.
            TYPE: integer

            NAME: from_entered_time
            DESC: Specifies that no orders entered before this time should be returned. Valid ISO-8601 formats are:
                  yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz Date must be within 60 days from today's date. 'to_entered_time' 
                  must also be set.
            TYPE: String

            NAME: to_entered_time
            DESC: Specifies that no orders entered after this time should be returned.Valid ISO-8601 formats are:
                  yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz. 'from_entered_time' must also be set.
            TYPE: String

            NAME: status
            DESC: Specifies that only orders of this status should be returned. Possible Values are:

                  1. AWAITING_PARENT_ORDER
                  2. AWAITING_CONDITION
                  3. AWAITING_MANUAL_REVIEW
                  4. ACCEPTED
                  5. AWAITING_UR_NOT
                  6. PENDING_ACTIVATION
                  7. QUEDED
                  8. WORKING
                  9. REJECTED
                  10. PENDING_CANCEL
                  11. CANCELED
                  12. PENDING_REPLACE
                  13. REPLACED
                  14. FILLED
                  15. EXPIRED

            EXAMPLES:

            SessionObject.get_orders_query(account = 'MyAccountID', max_results = 6, from_entered_time = '2019-10-01', to_entered_time = '2019-10-10', status = 'FILLED')
            SessionObject.get_orders_query(account = 'MyAccountID', max_results = 6, status = 'EXPIRED')
            SessionObject.get_orders_query(account = 'MyAccountID', status = 'REJECTED')
            SessionObject.get_orders_query(account = 'MyAccountID')

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # define the payload
        data = {"maxResults": max_results, "fromEnteredTime": from_entered_time,
                "toEnteredTime": to_entered_time, "status": status}

        # define the endpoint
        endpoint = '/accounts/{}/orders'.format(account)

        # build the url
        url = self.api_endpoint(endpoint)

        # make the request
        return requests.get(url=url, headers=merged_headers, params=data,  verify=True).json()

    def get_orders_query(self, account=None, max_results=None, from_entered_time=None, to_entered_time=None, status=None):
        '''
            All orders for a specific account or, if account ID isn't specified, orders will be returned for all linked accounts

            Documentation Link: https://developer.tdameritrade.com/account-access/apis/get/orders-0

            NAME: account
            DESC: The account number that you want to query for orders, or if none provided will query all.
            TYPE: String

            NAME: max_results
            DESC: The maximum number of orders to retrieve.
            TYPE: integer

            NAME: from_entered_time
            DESC: Specifies that no orders entered before this time should be returned. Valid ISO-8601 formats are:
                  yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz Date must be within 60 days from today's date. 'to_entered_time' 
                  must also be set.
            TYPE: String

            NAME: to_entered_time
            DESC: Specifies that no orders entered after this time should be returned.Valid ISO-8601 formats are:
                  yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz. 'from_entered_time' must also be set.
            TYPE: String

            NAME: status
            DESC: Specifies that only orders of this status should be returned. Possible Values are:

                  1. AWAITING_PARENT_ORDER
                  2. AWAITING_CONDITION
                  3. AWAITING_MANUAL_REVIEW
                  4. ACCEPTED
                  5. AWAITING_UR_NOT
                  6. PENDING_ACTIVATION
                  7. QUEDED
                  8. WORKING
                  9. REJECTED
                  10. PENDING_CANCEL
                  11. CANCELED
                  12. PENDING_REPLACE
                  13. REPLACED
                  14. FILLED
                  15. EXPIRED

            EXAMPLES:

            SessionObject.get_orders_query(account = 'MyAccountID', max_results = 6, from_entered_time = '2019-10-01', to_entered_time = '2019-10-10', status = 'FILLED')
            SessionObject.get_orders_query(account = 'MyAccountID', max_results = 6, status = 'EXPIRED')
            SessionObject.get_orders_query(account = 'MyAccountID', status = 'REJECTED')
            SessionObject.get_orders_query(account =  None)

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # define the payload
        data = {"accountId": account,
                "maxResults": max_results,
                "fromEnteredTime": from_entered_time,
                "toEnteredTime": to_entered_time,
                "status": status}

        # define the endpoint
        endpoint = '/orders'

        # build the url
        url = self.api_endpoint(endpoint)

        # make the request
        return requests.get(url=url, headers=merged_headers, params=data,  verify=True).json()

    def get_order(self, account=None, order_id=None):
        '''
            All orders for a specific account or, if account ID isn't specified, orders will be returned for all linked accounts

            Documentation Link: https://developer.tdameritrade.com/account-access/apis/get/orders-0

            NAME: account
            DESC: The account number that you want to query the order for.
            TYPE: String

            NAME: order_id
            DESC: The order id.
            TYPE: integer

            EXAMPLES:

            SessionObject.get_order(account = 'MyAccountID', order_id = 'MyOrderID')
        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # define the endpoint
        endpoint = 'accounts/{}/orders/{}'.format(account, order_id)

        # build the url
        url = self.api_endpoint(endpoint)

        # make the request
        return requests.get(url=url, headers=merged_headers,  verify=True).json()

    def cancel_order(self, account=None, order_id=None):
        '''
            Cancel a specific order for a specific account.

            Documentation Link: https://developer.tdameritrade.com/account-access/apis/delete/accounts/%7BaccountId%7D/orders/%7BorderId%7D-0

            NAME: account
            DESC: The account number that you want to query the order for.
            TYPE: String

            NAME: order_id
            DESC: The order id.
            TYPE: integer
            
            RTYPE: Integer

            EXAMPLES:

            SessionObject.cancel_order(account = 'MyAccountID', order_id = 'MyOrderID')

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers()

        # define the endpoint
        endpoint = 'accounts/{}/orders/{}'.format(account, order_id)

        # build the url
        url = self.api_endpoint(endpoint)

        # delete the request
        delete_response = requests.delete(url=url, headers=merged_headers, verify=True)
        delete_status = delete_response.status_code
        
        if delete_status == 200:
            print('ORDER DELETE REQUEST FOR ORDER ID {} RETURNED STATUS CODE {}'.format(order_id, delete_status))
            return delete_status
        else:
            print('ORDER DELETE REQUEST FOR ORDER ID {} RETURNED STATUS CODE {} AND WAS NOT DELETED'(order_id, delete_status))
            return order_id


    def place_order(self, account=None, order=None):
        '''
            Places an order for a specific account.

            Documentation Link: https://developer.tdameritrade.com/account-access/apis/delete/accounts/%7BaccountId%7D/orders/%7BorderId%7D-0

            NAME: account
            DESC: The account number that you want to place the order for.
            TYPE: String

            NAME: order
            DESC: Either a JSON string or a TDOrder object that contains the info needed for an order placement.
            TYPE: String | Order

            EXAMPLES:

            SessionObject.place_order(account = 'MyAccountID', order = {'orderKey':'OrderValue'})
            SessionObject.place_order(account = 'MyAccountID', order = <Order>)

        '''

        # first make sure that the token is still valid.
        self.token_validation()

        # grab the original headers we have stored.
        merged_headers = self.headers(mode='application/json')

        # define the endpoint
        endpoint = 'accounts/{}/orders'.format(account)

        # build the url
        url = self.api_endpoint(endpoint)

        # check to see if it's an order object.
        if isinstance(order, Order):
            order = order._saved_order_to_json()
        else:
            order = json.dumps(order)

        # make the request
        response = requests.post(url=url, headers=merged_headers, data=order, verify=True)

        # Check if the order was successful.
        if response.status_code == 201:
            print("Order was successfully placed.")
            return response
        else:
            return response.json()

    def _create_token_timestamp(self, token_timestamp=None):
        '''
            Takes the token timestamp and converts it to the proper format
            needed for the streaming API.

            NAME: token_timestamp
            DESC: The timestamp returned from the get_user_principals endpoint.
            TYPE: String.

            RTYPE: TDStream Object
        '''

        token_timestamp = datetime.datetime.strptime(token_timestamp, "%Y-%m-%dT%H:%M:%S%z")
        token_timestamp = int(token_timestamp.timestamp()) * 1000

        return token_timestamp

    def create_streaming_session(self):
        '''
            Creates a new streaming session that can be used to stream different data sources.

            RTYPE: TDStream Object
        '''
        
        # Grab the Streamer Info.
        userPrincipalsResponse = self.get_user_principals(
            fields=['streamerConnectionInfo','streamerSubscriptionKeys','preferences','surrogateIds'])

        # Grab the timestampe.
        tokenTimeStamp = userPrincipalsResponse['streamerInfo']['tokenTimestamp']

        # Grab socket
        socket_url = userPrincipalsResponse['streamerInfo']['streamerSocketUrl']

        # Parse the token timestamp.
        tokenTimeStampAsMs = self._create_token_timestamp(
            token_timestamp=tokenTimeStamp)

        # Define our Credentials Dictionary used for authentication.
        credentials = {"userid": userPrincipalsResponse['accounts'][0]['accountId'],
                       "token": userPrincipalsResponse['streamerInfo']['token'],
                       "company": userPrincipalsResponse['accounts'][0]['company'],
                       "segment": userPrincipalsResponse['accounts'][0]['segment'],
                       "cddomain": userPrincipalsResponse['accounts'][0]['accountCdDomainId'],
                       "usergroup": userPrincipalsResponse['streamerInfo']['userGroup'],
                       "accesslevel": userPrincipalsResponse['streamerInfo']['accessLevel'],
                       "authorized": "Y",
                       "timestamp": tokenTimeStampAsMs,
                       "appid": userPrincipalsResponse['streamerInfo']['appId'],
                       "acl": userPrincipalsResponse['streamerInfo']['acl']}

        # Create the session
        streaming_session = TDStreamerClient(
            websocket_url=socket_url, user_principal_data=userPrincipalsResponse, credentials=credentials)

        return streaming_session


if __name__ == "__main__":
    pass