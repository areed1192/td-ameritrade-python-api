import csv
import os
import asyncio
import json
import urllib
import websockets
from td.fields import STREAM_FIELD_IDS, CSV_FIELD_KEYS, CSV_FIELD_KEYS_LEVEL_2

class TDStreamerClient():

    '''
        TD Ameritrade Streaming API Client Class.

        Implements a Websocket object that connects to the TD Streaming API, submits requests,
        handles messages, and streams data back to the user.
    '''

    def __init__(self, websocket_url=None, user_principal_data=None, credentials=None):
        '''
            Initalizes the Client Object and defines different components that will be needed to
            make a connection with the TD Streaming API.

            NAME: websocket_url
            DESC: The websocket URL that is returned from a Get_User_Prinicpals Request.
            TYPE: String

            NAME: user_principal_data
            DESC: The data that was returned from the "Get_User_Principals" request. Contains the
                  info need for the account info.
            TYPE: Dictionary

            NAME: credentials
            DESC: A credentials dictionary that is created from the "create_streaming_session" method.
            TYPE: Dictionary

        '''

        self.websocket_url = "wss://{}/ws".format(websocket_url)
        self.credentials = credentials
        self.user_principal_data = user_principal_data
        self.connection = None

        # this will hold all of our requests
        self.data_requests = {"requests": []}

        # this will house all of our field numebrs and keys so that way the user can use names to define the fields they want.
        self.fields_ids_dictionary = STREAM_FIELD_IDS
        self.fields_keys_write = CSV_FIELD_KEYS
        self.fields_keys_write_level_2 = CSV_FIELD_KEYS_LEVEL_2
        self.approved_writes = list(self.fields_keys_write.keys())
        self.approved_writes_level_2 = list(self.fields_keys_write_level_2.keys())

    def write_behavior(self, write = 'csv', file_path = None, append_mode = True):
        """
            Sets the csv dump location and the append mode.

            NAME: write
            DESC: Defines where you want to write the streaming data to. Right now can only specify
                  'csv'
            TYPE: String

            NAME: file_path
            DESC: Specifies where you would like the CSV file to be written to. If nothing is provided then 
                  current working directory is used.
            TYPE: String

            NAME: append-mode
            DESC: Defines whether the write mode should be append or new. If append-mode is True, then all
                  CSV data will go to the existing file. Can either be `True` or `False`.
            TYPE: Boolean

        """

        if write == 'csv':
            self.CSV_PATH = file_path
            self.CSV_PATH_STREAM = self.CSV_PATH.replace(".csv", "_stream.csv")

            # Define Storage mode for CSV files.
            if append_mode == True:
                self.CSV_APPEND_MODE = 'a+'
            elif append_mode == False:
                self.CSV_APPEND_MODE = 'w'       


    async def _write_book_data(self, book_data = None, book_type = None, book_timestamp = None, book_content = None, file_object = None):

        for index, activity_section in enumerate(book_data):                                
            section_id = str(book_timestamp) + "_" + str(index)
            price = activity_section['0']
            total_size = activity_section['1']
            total_count = activity_section['2']
            book_data_collection = activity_section['3']

            for book_data in book_data_collection:
                mpid = book_data["0"]
                size = book_data["1"]
                _time = book_data["2"]
                data = ["book_{}".format(book_type), section_id, 
                        "book_{}_price".format(book_type), price, 
                        "book_{}_size".format(book_type), total_size, 
                        "book_{}_otal_count".format(book_type), total_count, 
                        "book_{}_section_mpid".format(book_type), mpid, 
                        "book_{}_section_size".format(book_type), size, 
                        "book_{}_section_time".format(book_type), _time]

                file_object.writerow(data)
        

    ############################################################################################################################################################

    async def _write_to_csv(self, data = None):
        '''
            ONLY WORKS WITH LEVEL ONE QUOTES RIGHT NOW!

            Takes the data from a stream and writes it to a CSV file for further manipulation.

            NAME: data
            DESC: The streaming data requested.
            TYPE: Dictionary.
        '''

        # check if it's a list, this should always be the case.
        if isinstance(data, list):            
            for service_result in data:

                # A Service response should have the following keys.
                service_name = service_result['service']
                service_timestamp = service_result['timestamp']
                service_command = service_result['command']
                service_contents = service_result['content']

                if service_name in self.approved_writes:

                    # open the new CSV file in write mode, `newline` makes sure we don't have extra blank rows.
                    with open(self.CSV_PATH, mode = self.CSV_APPEND_MODE, newline='') as stream_file:

                        # create the writer.
                        stream_writer = csv.writer(stream_file)
                        for data_section in service_contents:
                            for field_key in data_section:

                                # This adds functionality by allowing us to dump the field names and not numbers.
                                old_key = field_key
                                new_key = self.fields_keys_write[service_name][old_key]
                                field_value = data_section[old_key]
                                data = [service_name, service_timestamp, service_command, old_key, new_key, field_value]
                                stream_writer.writerow(data)

                elif service_name in self.approved_writes_level_2:

                    # open the new CSV file in write mode, `newline` makes sure we don't have extra blank rows.
                    with open(self.CSV_PATH_STREAM, mode = self.CSV_APPEND_MODE, newline='') as stream_file:
                        
                        # create the writer.
                        stream_writer = csv.writer(stream_file)
                        for service_content in service_contents:

                            symbol = service_content['key']
                            book_timestamp = service_content['1']
                            book_bid = service_content['2']
                            book_ask = service_content['3']
                            content_names = [symbol, service_name, service_timestamp, service_command]
                            self._write_book_data(book_bid, book_type='bid', book_timestamp=book_timestamp, book_content=content_names, file_object=stream_writer)
                            self._write_book_data(book_ask, book_type='ask', book_timestamp=book_timestamp, book_content=content_names, file_object=stream_writer)

    ############################################################################################################################################################

    def _build_login_request(self):
        '''
            Builds the login request dictionary that will be used as the first 
            service request with the streaming API.

            RTYPE: Dictionary.
        '''

        # define a request
        login_request = {"requests": [{"service": "ADMIN",
                                       "requestid": "0",
                                       "command": "LOGIN",
                                       "account": self.user_principal_data['accounts'][0]['accountId'],
                                       "source": self.user_principal_data['streamerInfo']['appId'],
                                       "parameters": {"credential": urllib.parse.urlencode(self.credentials),
                                                      "token": self.user_principal_data['streamerInfo']['token'],
                                                      "version": "1.0"}}]}

        return json.dumps(login_request)

    def stream(self):
        '''
            Initalizes the stream by building a login request, starting an event loop,
            creating a connection, passing through the requests, and keeping the loop running.
        '''

        # Grab the login info.
        login_request = self._build_login_request()

        # Grab the Data Request.
        data_request = json.dumps(self.data_requests)

        # Start a loop.
        self.loop = asyncio.get_event_loop()

        # Start connection and get client connection protocol
        connection = self.loop.run_until_complete(self._connect())

        # Start listener and heartbeat
        asyncio.ensure_future(self._receive_message(connection))
        asyncio.ensure_future(self._send_message(login_request))
        asyncio.ensure_future(self._send_message(data_request))
        # asyncio.ensure_future(self.close_stream())
        
        # Keep Going.
        self.loop.run_forever()

    def close_logic(self, run_duration = None):
        '''
            Sets the logic to determine how long to keep the server open. If Not specified,
            Server will remain open forever or until it encounters an error.
            
            NAME: run_duration
            DESC: The time in seconds to run.
            TYPE: int

        '''

        if run_duration is not None:
            self.RUN_DURATION = run_duration
        else:
            self.RUN_DURATION = None


    async def close_stream(self):
        '''
            Closes the connection to the streaming service.
        '''

        if self.RUN_DURATION is not None:
            run_duration = self.RUN_DURATION
        else:
            run_duration = -1

        increment = 0

        while True:
            if increment < run_duration:
                await asyncio.sleep(1)
                increment += 1
            else:
                break
        
        # close the connection.
        await self.connection.close()

        # Stop the loop.
        self.loop.call_soon_threadsafe(self.loop.stop())

        # cancel all the task.
        for index, task in enumerate(asyncio.Task.all_tasks()):
            
            # let the user know which task is cancelled.
            print("Cancelling Task: {}".format(index))

            # cancel it.
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                print("main(): cancel_me is cancelled now")

    async def _connect(self):
        '''
            Connecting to webSocket server websockets.client.connect 
            returns a WebSocketClientProtocol, which is used to send 
            and receive messages
        '''

        # Create a connection.
        self.connection = await websockets.client.connect(self.websocket_url)

        # check it before sending it bacl.
        if self._check_connection():
            return self.connection

    def _check_connection(self):
        '''
            There are multiple times we will need to check the connection 
            of the websocket, this function will help do that.
        '''

        # if it's open we can stream.
        if self.connection.open:
            print('Connection established. Streaming will begin shortly.')
            return True
        else:
            raise ConnectionError

    async def _send_message(self, message=None):
        '''
            Sending message to webSocket server

            NAME: message
            DESC: The streaming request you wish to submit.
            TYPE: String
        '''
        await self.connection.send(message)

    async def _receive_message(self, connection):
        '''
            Receiving all server messages and handle them.

            NAME: connection
            DESC: The WebSocket Connection Client.
            TYPE: Object
        '''

        # Keep going until cancelled.
        while True:

            try:

                # recieve and decode the message.
                message = await connection.recv()

                try:
                    message_decoded = json.loads(message)
                except:
                    message_decoded = "No Data Returned"

                if 'data' in message_decoded.keys():                     
                    await self._write_to_csv(data = message_decoded['data'])

                print('-'*20)
                print('Received message from server: {}'.format(str(message_decoded)))

            except websockets.exceptions.ConnectionClosed:

                # stop the connection if there is an error.
                print('Connection with server closed')
                break

    async def heartbeat(self, connection):
        '''
            Sending heartbeat to server every 5 seconds
            Ping - pong messages to verify connection is alive
        '''
        while True:
            try:
                await connection.send('ping')
                await asyncio.sleep(3)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break

    def _new_request_template(self):
        '''
            This takes the Request template and populates the service count
            so that the requests are in order.
        '''

        # first get the current service request count
        service_count = len(self.data_requests['requests']) + 1

        request = {"service": None, "requestid": service_count, "command": None,
                   "account": self.user_principal_data['accounts'][0]['accountId'],
                   "source": self.user_principal_data['streamerInfo']['appId'],
                   "parameters": {"keys": None, "fields": None}}

        return request

    def _validate_argument(self, argument=None, endpoint=None):
        '''
            Validate arguments before submitting request.

            NAME: argument
            DESC: The argument that needs to be validated.
            TYPE: String | Integer

            NAME: endpoint
            DESC: The endpoint which the argument will be fed to. For example, "level_one_quote".
            TYPE: String

            RTYPE: Boolean
        '''
        # initalize a new list.
        arg_list = []

        # see if the argument is a list or not.
        if isinstance(argument, list):

            for arg in argument:

                arg_str = str(arg)
                key_list = list(self.fields_ids_dictionary[endpoint].keys())
                val_list = list(self.fields_ids_dictionary[endpoint].values())

                if arg_str in key_list:
                    arg_list.append(arg_str)
                elif arg_str in val_list:
                    key_value = key_list[val_list.index(arg_str)]
                    arg_list.append(key_value)                  

            return arg_list

        else:

            arg_str = str(argument)
            key_list = list(self.fields_ids_dictionary[endpoint].keys())
            val_list = list(self.fields_ids_dictionary[endpoint].values())

            if arg_str in key_list:
                return arg_str
            elif arg_str in val_list:
                key_value = key_list[val_list.index(arg_str)]
                return key_value
                

    def quality_of_service(self, qos_level=None):
        '''
            Allows the user to set the speed at which they recieve messages
            from the TD Server.

            NAME: qos_level
            DESC: The Quality of Service level that you wish to set. Ranges from 0
                  to 5 where 0 is the fastest and 5 is the slowest.
            TYPE: String
        '''

        # valdiate argument.
        qos_level = self._validate_argument(argument=qos_level, endpoint='qos_request')

        if qos_level is not None:

            # Build the request
            request = self._new_request_template()
            request['service'] = 'ADMIN'
            request['command'] = 'QOS'
            request['parameters']['qoslevel'] = qos_level
            self.data_requests['requests'].append(request)

        else:
            raise ValueError('ERROR!')

    def chart(self, service=None, symbols=None, fields=None):
        '''
            Represents the CHART_EQUITY endpoint that can be used to stream info
            needed to recreate charts.

            NAME: service
            DESC: The type of Chart Service you wish to recieve. Can be either CHART_EQUITY, CHART_FUTURES
                  or CHART_OPTIONS.
            TYPE: String

            NAME: symbols
            DESC: The symbol you wish to get chart data for.
            TYPE: String

            NAME: fields
            DESC: The fields for the request. Can either be a list of keys ['key 1','key 2'] or a list
                  of ints [1, 2, 3]
            TYPE: List<int> | List<str>
         '''

        # check to make sure it's a valid Chart Service.
        service_flag = service in ['CHART_EQUITY',
                                   'CHART_FUTURES', 'CHART_OPTIONS']

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint=service.lower())

        if service_flag and fields is not None:

            # Build the request
            request = request = self._new_request_template()
            request['service'] = service
            request['command'] = 'SUBS'
            request['parameters']['keys'] = ','.join(symbols)
            request['parameters']['fields'] = ','.join(fields)
            self.data_requests['requests'].append(request)

        else:
            raise ValueError('ERROR!')

    def actives(self, service=None, venue=None, duration=None):
        '''
            Represents the ACTIVES endpoint for the TD Streaming API where
            you can get the most actively traded stocks for a specific exchange.

            NAME: service
            DESC: The type of Active Service you wish to recieve. Can be one of the following:
                  [NASDAQ, NYSE, OTCBB, CALLS, OPTS, PUTS, CALLS-DESC, OPTS-DESC, PUTS-DESC]
            TYPE: String

            NAME: venue
            DESC: The symbol you wish to get chart data for.
            TYPE: String

            NAME: duration
            DESC: Specifies the look back period for collecting most actively traded instrument. Can be either
                  ['ALL', '60', '300', '600', '1800', '3600'] where the integrers represent number of seconds.
            TYPE: String
        '''

        # check to make sure it's a valid active service.
        service_flag = service in [
            'ACTIVES_NASDAQ', 'ACTIVES_NYSE', 'ACTIVES_OPTIONS', 'ACTIVES_OTCBB']

        # check to make sure it's a valid active service venue.
        venue_flag = venue in ['NASDAQ', 'NYSE', 'OTCBB', 'CALLS',
                               'OPTS', 'PUTS', 'CALLS-DESC', 'OPTS-DESC', 'PUTS-DESC']

        # check to make sure it's a valid duration
        duration_flag = duration in ['ALL', '60', '300', '600', '1800', '3600']

        if service_flag and venue_flag and duration_flag:

            # Build the request
            request = self._new_request_template()
            request['service'] = service
            request['command'] = 'SUBS'
            request['parameters']['keys'] = venue + '-' + duration
            request['parameters']['fields'] = '1'
            self.data_requests['requests'].append(request)

        else:
            raise ValueError('ERROR!')

    def account_activity(self):
        '''
            Represents the ACCOUNT_ACTIVITY endpoint of the TD Streaming API. This service is used to 
            request streaming updates for one or more accounts associated with the logged in User ID. 
            Common usage would involve issuing the OrderStatus API request to get all transactions 
            for an account, and subscribing to ACCT_ACTIVITY to get any updates.     
        '''

        # NOTE: If ACCT_ACTIVITY is one of the streaming requests, then the request MUST BE
        # on a SSL secure connection (HTTPS)

        # Build the request
        request = self._new_request_template()
        request['service'] = 'ACCT_ACTIVITY'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = self.user_principal_data['streamerSubscriptionKeys']['keys'][0]['key']
        request['parameters']['fields'] = '0,1,2,3'

        self.data_requests['requests'].append(request)

    def chart_history_futures(self, symbol=None, frequency=None, period=None, start_time=None, end_time=None):
        '''
            Represents the CHART HISTORY FUTURES endpoint for the TD Streaming API. Only Futures 
            chart history is available via Streamer Server.

            NAME: symbol
            DESC: A single futures symbol that you wish to get chart data for.
            TYPE: String

            NAME: frequency
            DESC: The frequency at which you want the data to appear. Can be one of the following options:
                  [m1, m5, m10, m30, h1, d1, w1, n1] where [m=minute, h=hour, d=day, w=week, n=month]
            TYPE: String

            NAME: period
            DESC: The period you wish to return historical data for. Can be one of the following options:
                  [d5, w4, n10, y1, y10] where [d=day, w=week, n=month, y=year]
            TYPE: String

            NAME: start_time
            DESC: Start time of chart in milliseconds since Epoch. OPTIONAL
            TYPE: String

            NAME: end_time
            DESC: End time of chart in milliseconds since Epoch. OPTIONAL
            TYPE: String

        '''

        # define the valid inputs.
        valid_frequencies = ['m1', 'm5', 'm10', 'm30', 'h1', 'd1', 'w1', 'n1']
        valid_periods = ['d1', 'd5', 'w4', 'n10', 'y1', 'y10']

        # validate the frequency input.
        if frequency not in valid_frequencies:
            raise ValueError(
                "The FREQUENCY you have chosen is not correct please choose a valid option:['m1', 'm5', 'm10', 'm30', 'h1', 'd1', 'w1', 'n1']")

        # validate the period input.
        if period not in valid_periods:
            raise ValueError(
                "The PERIOD you have chosen is not correct please choose a valid option:['d5', 'w4', 'n10', 'y1', 'y10']")

        # Build the request
        request = self._new_request_template()
        request['service'] = 'CHART_HISTORY_FUTURES'
        request['command'] = 'GET'
        request['parameters']['symbols'] = symbol[0]
        request['parameters']['frequency'] = frequency

        # handle the case where we get a start time or end time. DO FURTHER VALIDATION.
        if start_time is not None or end_time is not None:
            request['parameters']['END_TIME'] = end_time
            request['parameters']['START_TIME'] = end_time
        else:
            request['parameters']['period'] = period

        self.data_requests['requests'].append(request)

    def level_one_quotes(self, symbols=None, fields=None):
        '''
            Represents the LEVEL ONE QUOTES endpoint for the TD Streaming API. This
            will return quotes for a given list of symbols along with specified field information.

            NAME: symbols
            DESC: A List of symbols you wish to stream quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>
        '''

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='level_one_quote')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'QUOTE'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def level_one_options(self, symbols=None, fields=None):
        '''
            Represents the LEVEL ONE OPTIONS endpoint for the TD Streaming API. This
            will return quotes for a given list of option symbols along with specified field information.

            NAME: symbols
            DESC: A List of option symbols you wish to stream quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>
        '''

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='level_one_option')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'OPTION'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def level_one_futures(self, symbols=None, fields=None):
        '''
            Represents the LEVEL ONE FUTURES endpoint for the TD Streaming API. This
            will return quotes for a given list of futures symbols along with specified field information.

            NAME: symbols
            DESC: A List of futures symbols you wish to stream quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>
        '''

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='level_one_futures')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'LEVELONE_FUTURES'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def level_one_forex(self, symbols=None, fields=None):
        '''
            Represents the LEVEL ONE FOREX endpoint for the TD Streaming API. This
            will return quotes for a given list of forex symbols along with specified field information.

            NAME: symbols
            DESC: A List of forex symbols you wish to stream quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>
        '''

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='level_one_forex')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'LEVELONE_FOREX'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        print(request)

        self.data_requests['requests'].append(request)

    def level_one_futures_options(self, symbols=None, fields=None):
        '''
            Represents the LEVEL ONE FUTURES OPTIONS endpoint for the TD Streaming API. This
            will return quotes for a given list of forex symbols along with specified field information.

            NAME: symbols
            DESC: A List of forex symbols you wish to stream quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>
        '''

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='level_one_futures_options')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'LEVELONE_FUTURES_OPTIONS'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def news_headline(self, symbols=None, fields=None):
        '''
            Represents the NEWS_HEADLINE endpoint for the TD Streaming API. This endpoint
            is used to stream news headlines for different instruments.

            NAME: symbols
            DESC: A List of symbols you wish to stream news for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>         
        '''

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='news_headline')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'NEWS_HEADLINE'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def timesale(self, service=None, symbols=None, fields=None):
        '''
            Represents the TIMESALE endpoint for the TD Streaming API. The TIMESALE server ID is used to 
            request Time & Sales data for all supported symbols

            NAME: symbols
            DESC: A List of symbols you wish to stream time and sales data for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>         
        '''

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='timesale')

        # Build the request
        request = self._new_request_template()
        request['service'] = service
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    '''
        EXPERIMENTATION SECTION

        NO GUARANTEE THESE WILL WORK.
    '''

    def level_two_quotes(self, symbols=None, fields=None):
        '''
            EXPERIMENTAL: USE WITH CAUTION!

            Represents the LEVEL_TWO_QUOTES endpoint for the streaming API. Documentation on this
            service does not exist, but it appears that we can pass through 1 of 3 fields.

            NAME: symbols
            DESC: A List of symbols you wish to stream time level two quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings> 

        '''

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='level_two_quotes')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'LISTED_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def level_two_nyse(self, symbols=None, fields=None):
        '''
            EXPERIMENTAL: USE WITH CAUTION!

            Represents the LEVEL_TWO_QUOTES_NYSE endpoint for the streaming API. Documentation on this
            service does not exist, but it appears that we can pass through 1 of 3 fields.

            NAME: symbols
            DESC: A List of symbols you wish to stream time level two quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings> 

        '''

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='level_two_nyse')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'NYSE_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def level_two_options(self, symbols=None, fields=None):
        '''
            EXPERIMENTAL: USE WITH CAUTION!

            Represents the LEVEL_TWO_QUOTES_OPTIONS endpoint for the streaming API. Documentation on this
            service does not exist, but it appears that we can pass through 1 of 3 fields.

            NAME: symbols
            DESC: A List of symbols you wish to stream time level two quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings> 

        '''

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='level_two_options')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'OPTIONS_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def level_two_nasdaq(self, symbols=None, fields=None):
        '''
            EXPERIMENTAL: USE WITH CAUTION!

            Represents the LEVEL_TWO_QUOTES_NASDAQ endpoint for the streaming API. Documentation on this
            service does not exist, but it appears that we can pass through 1 of 3 fields.

            NAME: symbols
            DESC: A List of symbols you wish to stream time level two quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings> 

        '''
        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='level_two_nasdaq')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'NASDAQ_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def level_two_futures(self, symbols=None, fields=None):
        '''
            EXPERIMENTAL: USE WITH CAUTION!

            Represents the LEVEL_TWO_QUOTES_FUTURES endpoint for the streaming API. Documentation on this
            service does not exist, but it appears that we can pass through 1 of 3 fields.

            NAME: symbols
            DESC: A List of symbols you wish to stream time level two quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings> 

        '''

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='level_two_futures')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'FUTURES_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = '0,1,2'

        print(request)

        self.data_requests['requests'].append(request)

    def level_two_total_view(self, symbols=None, fields=None):

        # Build the request
        request = self._new_request_template()
        request['service'] = 'TOTAL_VIEW'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def level_two_forex(self, symbols=None, fields=None):
        '''
            EXPERIMENTAL: USE WITH CAUTION!

            Represents the LEVEL_TWO_FOREX endpoint for the streaming API. Documentation on this
            service does not exist, but it appears that we can pass through 1 of 3 fields.

            NAME: symbols
            DESC: A List of symbols you wish to stream time level two quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings> 

        '''

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='level_two_forex')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'FOREX_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    '''
        NOT WORKING
    '''

    def _streamer_server(self):

        # Build the request
        request = self._new_request_template()
        request['service'] = 'STREAMER_SERVER'
        request['command'] = 'ADMIN'
        request['parameters'] = {}

        self.data_requests['requests'].append(request)

    def _news_history(self):

        # OFFICIALLY DEAD

        # Build the request
        request = self._new_request_template()
        request['service'] = 'NEWS'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = 'IBM'
        request['parameters']['fields'] = 1576828800000

        self.data_requests['requests'].append(request)

    def _level_two_opra(self, symbols=None, fields=None):
        '''
            EXPERIMENTAL: USE WITH CAUTION!

            Represents the LEVEL_TWO_OPRA endpoint for the streaming API. Documentation on this
            service does not exist, but it appears that we can pass through 1 of 3 fields.

            NAME: symbols
            DESC: A List of symbols you wish to stream time level two quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings> 

        '''

        # Build the request
        request = self._new_request_template()
        request['service'] = 'OPRA'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def _level_two_futures_options(self, symbols=None, fields=None):
        '''
            EXPERIMENTAL: USE WITH CAUTION!

            Represents the LEVEL_TWO_FUTURES_OPTIONS endpoint for the streaming API. Documentation on this
            service does not exist, but it appears that we can pass through 1 of 3 fields.

            NAME: symbols
            DESC: A List of symbols you wish to stream time level two quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings> 

        '''

        if fields is not None:
            fields = [str(field) for field in fields]

        # Build the request
        request = self._new_request_template()
        request['service'] = 'FUTURES_OPTIONS_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = symbols
        request['parameters']['fields'] = '0,1,2,3'

        print(repr(request))

        self.data_requests['requests'].append(request)
