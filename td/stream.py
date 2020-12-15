import asyncio
import csv
import io
import json
import os
import textwrap
import unicodedata
import urllib

from typing import List
from typing import Union

import websockets

from td.enums import CSV_FIELD_KEYS
from td.enums import CSV_FIELD_KEYS_LEVEL_2
from td.enums import STREAM_FIELD_IDS


class TDStreamerClient():

    """
        TD Ameritrade Streaming API Client Class.

        Implements a Websocket object that connects to the TD Streaming API, submits requests,
        handles messages, and streams data back to the user.
    """

    def __init__(self, websocket_url: str, user_principal_data: dict, credentials: dict) -> None:     
        """Initalizes the Streaming Client.
        
        Initalizes the Client Object and defines different components that will be needed to
        make a connection with the TD Streaming API.

        Arguments:
        ----
        websocket_url {str} -- The websocket URL that is returned from a Get_User_Prinicpals Request.

        user_principal_data {dict} -- The data that was returned from the "Get_User_Principals" request. 
            Contains the info need for the account info.

        credentials {dict} -- A credentials dictionary that is created from the "create_streaming_session"
            method.
        
        Usage:
        ----

            >>> td_session = TDClient(
                client_id='<CLIENT_ID>',
                redirect_uri='<REDIRECT_URI>',
                credentials_path='<CREDENTIALS_PATH>'
            )
            >>> td_session.login()
            >>> td_stream_session = td_session.create_streaming_session()

        """

        self.websocket_url = "wss://{}/ws".format(websocket_url)
        self.credentials = credentials
        self.user_principal_data = user_principal_data
        self.connection: websockets.WebSocketClientProtocol = None
        self.file_stream_level_1: io.TextIOWrapper = None
        self.file_stream_level_2: io.TextIOWrapper = None

        # this will hold all of our requests
        self.data_requests = {"requests": []}

        # this will house all of our field numebrs and keys so that way the user can use names to define the fields they want.
        self.fields_ids_dictionary = STREAM_FIELD_IDS
        self.fields_keys_write = CSV_FIELD_KEYS
        self.fields_keys_write_level_2 = CSV_FIELD_KEYS_LEVEL_2
        self.approved_writes_level_1 = list(self.fields_keys_write.keys())
        self.approved_writes_level_2 = list(self.fields_keys_write_level_2.keys())

        self.print_to_console = True
        self.write_flag = False

        try:
            self.loop = asyncio.get_event_loop()
        except websockets.WebSocketException:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

        self.unsubscribe_count = 0

    def write_behavior(self, file_path: str, write: str = 'csv', append_mode: bool = True) -> None:        
        """Sets the csv dump location and the append mode.

        Arguments:
        ----

        file_path {str} -- Specifies where you would like the CSV file to be written to. 
            If nothing is provided then current working directory is used.

        Keyword Arguments:
        ----
        
        write {str} -- Defines where you want to write the streaming data to. Right now can only specify
            'csv'. (default: {'csv'})

        append_mode {bool} -- Defines whether the write mode should be append or new. If append-mode is True, 
            then all CSV data will go to the existing file. Can either be `True` or `False`. (default: {True})

        Usage:
        ----
            >>> td_session = TDClient(
                client_id='<CLIENT_ID>',
                redirect_uri='<REDIRECT_URI>',
                credentials_path='<CREDENTIALS_PATH>'
            )
            >>> td_session.login()
            >>> td_stream_session = td_session.create_streaming_session()
            >>> td_stream_session.write_behavior(file_path='data_dump.csv')
        """

        if write == 'csv':
            self.CSV_PATH = file_path
            self.CSV_PATH_STREAM = self.CSV_PATH.replace(".csv", "_level_2.csv")

            # Define Storage mode for CSV files.
            if append_mode == True:
                self.CSV_APPEND_MODE = 'a+'
            elif append_mode == False:
                self.CSV_APPEND_MODE = 'w+'

            self.file_stream_level_1 = open(
                file=self.CSV_PATH, 
                mode=self.CSV_APPEND_MODE, 
                newline=''
            )

            self.file_stream_level_2 = open(
                file=self.CSV_PATH_STREAM,
                mode=self.CSV_APPEND_MODE,
                newline=''
            )

            self.write_flag = True

    def _write_non_chart_services(self, data_content: dict, service_name: str) -> List:
        """Takes a Non-Chart Services and parses the values to write.

        Arguments:
        ----
        data_content {dict} -- The content from the stream.

        service_name {str} -- The name of the service the data came from.

        Returns:
        ----
        list -- A single row of data.
        """

        all_data = []

        for data_section in data_content:
            for field_key in data_section:
                new_key = self.fields_keys_write[service_name][field_key]
                field_value = data_section[field_key]
                data = [service_name, field_key, new_key, field_value]
                all_data.append(data)
        
        return all_data

    def _write_chart_services(self, data_content: dict, service_name: str) -> List:
        """Takes a Chart Services and parses the values to write.

        Arguments:
        ----
        data_content {dict} -- The content from the stream.

        service_name {str} -- The name of the service the data came from.

        Returns:
        ----
        List -- A single row of data.
        """

        all_data = []

        for data_section in data_content:
            for field_key in data_section:

                if field_key != '3':
                    new_key = self.fields_keys_write[service_name][field_key]
                    field_value = data_section[field_key]
                    data = [service_name, field_key, new_key, field_value]
                    all_data.append(data)

                elif field_key == '3':

                    for candle in data_section['3']:
                        for candle_key in candle:
                            new_key = self.fields_keys_write[service_name][candle_key]
                            field_value = candle[candle_key]
                            data = [service_name, candle_key, new_key, field_value]
                            all_data.append(data)

        return all_data

    def _write_level_two_services(self, data_content: dict, service_name: str) -> List:
        """Takes Level 2 services and parses them so they can be written.

        Arguments:
        ----
        data_content {dict} -- The content from the stream.

        service_name {str} -- The name of the service the data came from.

        Returns:
        ----
        List -- A single row of data.
        """

        all_data = []

        for service_content in data_content:

            symbol = service_content['key']
            book_timestamp = service_content['1']
            book_bid = service_content['2']
            book_ask = service_content['3']

            content_names = [symbol, service_name]
            book_data_full = [
                {'book_type':'bid','book_data':book_bid}, 
                {'book_type':'ask','book_data':book_ask}
            ]

            for book_dict in book_data_full:
                book_data = book_dict['book_data']
                book_type = book_dict['book_type']

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

                        data = [
                            "book_{}".format(book_type), section_id, 
                            "book_{}_price".format(book_type), price, 
                            "book_{}_size".format(book_type), total_size, 
                            "book_{}_total_count".format(book_type), total_count, 
                            "book_{}_section_mpid".format(book_type), mpid, 
                            "book_{}_section_size".format(book_type), size, 
                            "book_{}_section_time".format(book_type), _time
                        ]

                        all_data.append(content_names + data)

        return all_data
    
    def _write_active_services(self,data_content: dict, service_name: str) -> List:
        """Takes Level 2 services and parses them so they can be written.

        Arguments:
        ----
        data_content {dict} -- The content from the stream.

        service_name {str} -- The name of the service the data came from.

        Returns:
        ----
        List -- A single row of data.
        """

        all_data = []    

        for data_section in data_content:

            active_key = data_section['key']
            active_data = data_section['1']

            active_data_parts = active_data.split(';')
            active_data_id = active_data_parts[0]
            active_data_duration = active_data_parts[1]
            active_data_timestamp = active_data_parts[2]
            active_data_display_time = active_data_parts[3]
            active_data_number_of_groups = active_data_parts[4]

            all_data.append([service_name, "", 'active-key', active_key])
            all_data.append([service_name, "", 'active-id', active_data_id])
            all_data.append([service_name, "", 'active-duration', active_data_duration])
            all_data.append([service_name, "", 'active-timestamp', active_data_timestamp])
            all_data.append([service_name, "", 'active-display-time', active_data_display_time])
            all_data.append([service_name, "", 'active-group-count', active_data_number_of_groups])

            active_data_groups = active_data_parts[5:]

            for active_data_group in active_data_groups:

                group_split = active_data_group.split(':')

                group_id = group_split[0]
                group_count = group_split[1]
                group_total_volume = group_split[2]

                group_id_label = 'active-group-id'
                group_id_count_label = 'active-group-id-{}-count'.format(group_id)
                group_id_volume_label = 'active-group-id-{}-volume'.format(group_id)

                all_data.append([service_name, "", group_id_label, group_id])
                all_data.append([service_name, "", group_id_count_label, group_count])
                all_data.append([service_name, "", group_id_volume_label, group_total_volume])

                group_symbols = group_split[3:]
                new_groups = [group_symbols[i:i + 3] for i in range(0, len(group_symbols), 3)]

                for index, group in enumerate(new_groups):

                    group_item_id_label = 'active-group-id-{}-item-{}-symbol'.format(group_id, index + 1)
                    group_item_volume_label = 'active-group-id-{}-item-{}-volume'.format(group_id, index + 1)
                    group_item_percent_label = 'active-group-id-{}-item-{}-percent'.format(group_id, index + 1)

                    all_data.append([service_name, "", group_item_id_label, group[0]])
                    all_data.append([service_name, "", group_item_volume_label, group[1]])
                    all_data.append([service_name, "", group_item_percent_label, group[2]])
        
        return all_data

    async def _write_to_csv(self, data: dict) -> None:
        """Writes the stream to a CSV file.

        Takes the data from a stream, determines which sections can be
        written and then writes it to a CSV file for further manipulation.

        Arguments:
        ----
        data {dict} -- The data stream.
        """

        # Deterimne what part of the message we need to get.
        if 'data' in data.keys():
            data = data['data']
        elif 'snapshot' in data.keys():
            data = data['snapshot']
        else:
            return None

        stream_writer_level_1 = csv.writer(self.file_stream_level_1)
        stream_writer_level_2 = csv.writer(self.file_stream_level_2)

        for service_result in data:

            # A Service response should have the following keys.
            service_name = service_result['service']
            service_timestamp = service_result['timestamp']
            service_contents = service_result['content']

            approved_level_1 = service_name in self.approved_writes_level_1
            approved_level_2 = service_name in self.approved_writes_level_2
            chart_history_service = service_name == 'CHART_HISTORY_FUTURES'
            active_service = 'ACTIVES_' in service_name

            # Write the non-chart level 1 services.
            if approved_level_1 and chart_history_service == False and active_service == False:

                # Grab the data
                new_data = self._write_non_chart_services(data_content=service_contents, service_name=service_name)

                for row in new_data:
                    new_row = [service_timestamp] + row
                    stream_writer_level_1.writerow(new_row)  

            # Write the Chart Services.
            elif approved_level_1 and chart_history_service and active_service == False:
                
                # Grab the data
                new_data = self._write_chart_services(data_content=service_contents, service_name=service_name)

                for row in new_data:
                    new_row = [service_timestamp] + row
                    stream_writer_level_1.writerow(new_row)  

            # Write the Active Services.
            elif approved_level_1 and chart_history_service == False and active_service:
                
                # Grab the data
                new_data = self._write_active_services(data_content=service_contents, service_name=service_name)

                for row in new_data:
                    new_row = [service_timestamp] + row
                    stream_writer_level_1.writerow(new_row)  

            # Write the Level 2 Services
            elif approved_level_2:
                    
                # Grab the data
                new_data = self._write_level_two_services(data_content=service_contents, service_name=service_name)

                for row in new_data:
                    new_row = [service_timestamp] + row
                    stream_writer_level_2.writerow(new_row)

    async def unsubscribe(self, service: str) -> dict:
        """Unsubscribe from a service.

        Arguments:
        ----
        service {str} -- The name of the service, to unsubscribe from. For example,
            "LEVELONE_FUTURES" or "QUOTES".

        Returns:
        ----
        dict -- A message from the websocket specifiying whether the unsubscribe command
            was successful.
        """

        self.unsubscribe_count += 1

        service_count = len(self.data_requests['requests']) + self.unsubscribe_count
        
        request = {
            "requests":[
                {
                    "service": service.upper(), 
                    "requestid": service_count, 
                    "command": 'UNSUBS',
                    "account": self.user_principal_data['accounts'][0]['accountId'],
                    "source": self.user_principal_data['streamerInfo']['appId']
                }
            ]
        }

        await self._send_message(json.dumps(request))

        return await self._receive_message(return_value=True)

    def _build_login_request(self) -> str:
        """Builds the Login request for the streamer.

        Builds the login request dictionary that will 
        be used as the first service request with the 
        streaming API.

        Returns:
        ----
        [str] -- A JSON string with the login details.

        """        

        # define a request
        login_request = {
            "requests": [
                {
                    "service": "ADMIN",
                    "requestid": "0",
                    "command": "LOGIN",
                    "account": self.user_principal_data['accounts'][0]['accountId'],
                    "source": self.user_principal_data['streamerInfo']['appId'],
                    "parameters": {
                        "credential": urllib.parse.urlencode(self.credentials),
                        "token": self.user_principal_data['streamerInfo']['token'],
                        "version": "1.0"
                    }
                }
            ]
        }

        return json.dumps(login_request)

    def _build_data_request(self) -> str:
        """Builds the data request for the streaming service.

        Takes all the service requests and converts them to a JSON 
        string.

        Returns:
        ----
        [str] -- A JSON string with the login details.

        """

        return json.dumps(self.data_requests)

    async def build_pipeline(self) -> websockets.WebSocketClientProtocol:
        """Builds a data pipeine for processing data.

        Often we want to take the data we are streaming and
        use it in other functions or store it in other platforms.
        This method makes the process of building a pipeline easy
        by handling all the connection setup and request setup.

        Returns:
        ----
        websockets.WebSocketClientProtocol -- The websocket connection.
        """

        # In this case, we don't want things printing to the console.
        self.print_to_console = False

        # Connect to Websocket.
        await self._connect()

        # Build the Data Request.
        await self._send_message(self._build_data_request())

        return self.connection

    async def start_pipeline(self) -> dict:     
        """Recieves the data as it streams in.

        Returns:
        ----
        dict -- The data coming from the websocket.
        """

        return await self._receive_message(return_value=True)

    def stream(self, print_to_console: bool = True) -> None:
        """Starts the stream and prints the output to the console.

        Initalizes the stream by building a login request, starting 
        an event loop, creating a connection, passing through the 
        requests, and keeping the loop running.

        Keyword Arguments:
        ----
        print_to_console {bool} -- Specifies whether the content is to be printed
            to the console or not. (default: {True})
        """        

        # Print it to the console.
        self.print_to_console = print_to_console

        # Connect to the Websocket.
        self.loop.run_until_complete(self._connect())

        # Send the Request.
        asyncio.ensure_future(self._send_message(self._build_data_request()))

        # Start Recieving Messages.
        asyncio.ensure_future(self._receive_message(return_value=False))

        # Keep the Loop going, until an exception is reached.
        self.loop.run_forever()

    def close_logic(self, logic_type: str) -> bool:
        """Defines how the stream should close.

        Sets the logic to determine how long to keep the server open. 
        If Not specified, Server will remain open forever or until 
        it encounters an error.

        Keyword Arguments:
        ----
        logic_type {str} -- Defines what rules to follow to close the conneciton.
            can be either of the following: ['empty', 'market-hours']

        Returns:
        ----
        bool -- Specifiying whether the close logic was set `True`, or
            wasn't set `False`
        """
        pass

    async def close_stream(self) -> None:
        """Closes the connection to the streaming service."""        
        
        # close the connection.
        await self.connection.close()

        # Define the Message.
        message = textwrap.dedent("""
        {lin_brk}
        CLOSING PROCESS INITIATED:
        {lin_brk}
        WebSocket Closed: True
        Event Loop Closed: True
        {lin_brk}
        """).format(lin_brk="="*80)
        
        # Shutdown all asynchronus generators.
        await self.loop.shutdown_asyncgens()

        # Stop the loop.
        if self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop())
            print(message)
            await asyncio.sleep(3)

        # # Once closed, verify it's closed.
        # if self.loop.is_closed():
        #     print('Event loop was closed.')
        # else:            
        #     print('Event loop was not closed.')

        # # cancel all the task.
        # for index, task in enumerate(asyncio.Task.all_tasks()):
            
        #     # let the user know which task is cancelled.
        #     print("Cancelling Task: {}".format(index))

        #     # cancel it.
        #     task.cancel()

        #     try:
        #         await task
        #     except asyncio.CancelledError:
        #         print("main(): cancel_me is cancelled now")

    async def _connect(self) -> websockets.WebSocketClientProtocol:
        """Connects the Client to the TD Websocket.

        Connecting to webSocket server websockets.client.connect 
        returns a WebSocketClientProtocol, which is used to send 
        and receive messages

        Keyword Arguments:
        ----
        pipeline_start {bool} -- This is also used to start the data
            pipeline so, in that case we can handle more tasks here.
            (default: {True})

        Returns:
        ---
        websockets.WebSocketClientProtocol -- The websocket connection.
        """        

        # Grab the login info.
        login_request = self._build_login_request()

        # Create a connection.
        self.connection = await websockets.client.connect(self.websocket_url)

        # See if we are connected.
        is_connected = await self._check_connection()

        # If we are connected then login.
        if is_connected:

            await self._send_message(login_request)

            while True:
                
                # Grab the Response.
                response = await self._receive_message(return_value=True)
                responses = response.get('response')

                # If we get a code 3, we had a login error.
                if responses[0]['content']['code'] == 3:
                    raise ValueError('LOGIN ERROR: ' + responses[0]['content']['msg'])
                
                # see if we had a login response.
                for r in responses:
                    if r.get('service') == 'ADMIN' and r.get('command') == 'LOGIN':
                        return self.connection

    async def _check_connection(self) -> bool:
        """Determines if we have an active connection

        There are multiple times we will need to check the connection 
        of the websocket, this function will help do that.

        Raises:
        ----
        ConnectionError: An error is raised if we can't connect to the
            websocket.

        Returns:
        ----
        bool -- True if the connection healthy, False otherwise.
        """        

        # if it's open we can stream.
        if self.connection.open:
            print('Connection established. Streaming will begin shortly.')
            return True
        elif self.connection.close:
            print('Connection was never opened and was closed.')
            return False
        else:
            raise ConnectionError

    async def _send_message(self, message: str):
        """Sends a message to webSocket server

        Arguments:
        ----
        message {str} -- The JSON string with the
            data streaming service subscription.
        """        

        await self.connection.send(message)


    async def _receive_message(self, return_value: bool = False) -> dict:
        """Recieves and processes the messages as needed.

        Keyword Arguments:
        ----
        return_value {bool} -- Specifies whether the messages should be returned
            back to the calling function or not. (default: {False})

        Returns:
        ----
        {dict} -- A python dictionary
        """

        # Keep going until cancelled.
        while True:

            try:
                
                # Grab the Message
                message = await self.connection.recv()

                # Parse Message
                message_decoded = await self._parse_json_message(message=message)

                # Write the data if needed.
                if self.write_flag:
                    try:
                        await self._write_to_csv(data = message_decoded)
                    except:
                        print('Could not write content to CSV file, closing stream')
                        await self.close_stream()
                        break

                if return_value:
                    return message_decoded

                elif self.print_to_console:
                    print('='*20)
                    print('Message Received:')
                    print('-'*20)
                    print(message_decoded)
                    print('-'*20)
                    print('')         

            except websockets.exceptions.ConnectionClosed:

                # stop the connection if there is an error.
                await self.close_stream()
                break           

    async def _parse_json_message(self, message: str) -> dict:
        """Parses incoming messages from the stream

        Arguments:
        ----
        message {str} -- The JSON string needing to be parsed.

        Returns:
        ----
        dict -- A python dictionary containing the original values.
        """

        try:
            message_decoded = json.loads(message)
        except:
            message = message.encode('utf-8').replace(b'\xef\xbf\xbd', bytes('"None"','utf-8')).decode('utf-8')
            message_decoded = json.loads(message)

        return message_decoded

    async def heartbeat(self) -> None:
        """Sending heartbeat to server every 5 seconds."""

        while True:
            try:
                await self.connection.send('ping')
                await asyncio.sleep(5)
            except websockets.exceptions.ConnectionClosed:
                self.close_stream()
                break

    def _new_request_template(self) -> dict:
        """Serves as a template to build new service requests.

        This takes the Request template and populates the required fields
        for a subscription request.

        Returns:
        ----
        {dict} -- The service request with the standard fields filled out.
        """

        # first get the current service request count
        service_count = len(self.data_requests['requests']) + 1

        request = {
            "service": None, 
            "requestid": service_count, 
            "command": None,
            "account": self.user_principal_data['accounts'][0]['accountId'],
            "source": self.user_principal_data['streamerInfo']['appId'],
            "parameters": {
                "keys": None, 
                "fields": None
            }
        }

        return request

    def _validate_argument(self, argument: Union[str, int], endpoint: str) -> Union[List[str], str]:
        """Validate field arguments before submitting request.

        Arguments:
        ---
        argument {Union[str, int]} -- Either a single argument or a list of arguments that are
            fields to be requested.
        
        endpoint {str} -- The subscription service the request will be sent to. For example,
            "level_one_quote".

        Returns:
        ----
        Union[List[str], str] -- The field or fields that have been validated.
        """        

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
                

    def quality_of_service(self, qos_level: str) -> None:
        """Quality of Service Subscription.
        
        Allows the user to set the speed at which they recieve messages
        from the TD Server.

        Arguments:
        ----
        qos_level {str} -- The Quality of Service level that you wish to set. 
            Ranges from 0 to 5 where 0 is the fastest and 5 is the slowest.

        Raises:
        ----
        ValueError: Error if no field is passed through.

        Usage:
        ----
            >>> td_session = TDClient(
                client_id='<CLIENT_ID>',
                redirect_uri='<REDIRECT_URI>',
                credentials_path='<CREDENTIALS_PATH>'
            )

            >>> td_session.login()
            >>> td_stream_session = td_session.create_streaming_session()
            >>> td_stream_session.quality_of_service(qos_level='express')
            >>> td_stream_session.stream()
        """
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
            raise ValueError('No Quality of Service Level provided.')

    def chart(self, service: str, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """Subscribes to the Chart Service.

        Represents the CHART_EQUITY, CHART_FUTRUES, and CHART_OPTIONS endpoint that can 
        be used to stream info needed to recreate charts.

        Arguments:
        ---
        service {str} -- The type of Chart Service you wish to recieve. Can be either 
            `CHART_EQUITY`, `CHART_FUTURES` or `CHART_OPTIONS`
        
        symbols {List[str]} -- The symbol you wish to get chart data for.
        
        fields {Union[List[str], List[int]]} -- The fields for the request. Can either be a list of 
            keys ['key 1','key 2'] or a list of ints [1, 2, 3]

        Raises:
        ----
        ValueError: Error if no field is passed through.

        Usage:
        ----
            >>> td_session = TDClient(
                client_id='<CLIENT_ID>',
                redirect_uri='<REDIRECT_URI>',
                credentials_path='<CREDENTIALS_PATH>'
            )

            >>> td_session.login()
            >>> td_stream_session = td_session.create_streaming_session()
        
            >>> td_stream_session.charts(
                service='CHART_EQUITY', 
                symbols=['AAPL','MSFT'], 
                fields=[0,1,2,3,4,5,6,7]
            )

            >>> td_stream_session.charts(
                service='CHART_OPTIONS', 
                symbols=['AAPL_040920C115'], 
                fields=[0,1,2,3,4,5,6,7]
            )

            >>> td_stream_session.charts(
                service='CHART_FUTURES', 
                symbols=['/ES','/CL'], 
                fields=[0,1,2,3,4,5,6,7]
            )

            >>> td_stream_session.stream()
        """        

        # check to make sure it's a valid Chart Service.
        service_flag = service in ['CHART_EQUITY', 'CHART_FUTURES', 'CHART_OPTIONS']

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

    def actives(self, service: str, venue: str, duration: str) -> None:
        """
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
        """

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
        """
            Represents the ACCOUNT_ACTIVITY endpoint of the TD Streaming API. This service is used to 
            request streaming updates for one or more accounts associated with the logged in User ID. 
            Common usage would involve issuing the OrderStatus API request to get all transactions 
            for an account, and subscribing to ACCT_ACTIVITY to get any updates.     
        """

        # Build the request
        request = self._new_request_template()
        request['service'] = 'ACCT_ACTIVITY'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = self.user_principal_data['streamerSubscriptionKeys']['keys'][0]['key']
        request['parameters']['fields'] = '0,1,2,3'

        self.data_requests['requests'].append(request)

    def chart_history_futures(self, symbol: str, frequency: str, start_time: str = None, end_time: str = None, period: str = None) -> None:
        """
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
        """

        # define the valid inputs.
        valid_frequencies = ['m1', 'm5', 'm10', 'm30', 'h1', 'd1', 'w1', 'n1']
        valid_periods = ['d1', 'd5', 'w4', 'n10', 'y1', 'y10']

        # validate the frequency input.
        if frequency not in valid_frequencies:
            raise ValueError(
                "The FREQUENCY you have chosen is not correct please choose a valid option:['m1', 'm5', 'm10', 'm30', 'h1', 'd1', 'w1', 'n1']")

        # validate the period input.
        if period not in valid_periods and start_time is None and end_time is None:
            raise ValueError(
                "The PERIOD you have chosen is not correct please choose a valid option:['d5', 'w4', 'n10', 'y1', 'y10']")

        # Build the request
        request = self._new_request_template()
        request['service'] = 'CHART_HISTORY_FUTURES'
        request['command'] = 'GET'
        request['parameters']['symbol'] = symbol[0]
        request['parameters']['frequency'] = frequency


        # handle the case where we get a start time or end time. DO FURTHER VALIDATION.
        if start_time is not None or end_time is not None:
            request['parameters']['END_TIME'] = end_time
            request['parameters']['START_TIME'] = start_time
        else:
            request['parameters']['period'] = period

        del request['parameters']['keys']
        del request['parameters']['fields']

        request['requestid'] = str(request['requestid'])

        self.data_requests['requests'].append(request)

    def level_one_quotes(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
            Represents the LEVEL ONE QUOTES endpoint for the TD Streaming API. This
            will return quotes for a given list of symbols along with specified field information.

            NAME: symbols
            DESC: A List of symbols you wish to stream quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>
        """

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

    def level_one_options(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
            Represents the LEVEL ONE OPTIONS endpoint for the TD Streaming API. This
            will return quotes for a given list of option symbols along with specified field information.

            NAME: symbols
            DESC: A List of option symbols you wish to stream quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>
        """

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

    def level_one_futures(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
            Represents the LEVEL ONE FUTURES endpoint for the TD Streaming API. This
            will return quotes for a given list of futures symbols along with specified field information.

            NAME: symbols
            DESC: A List of futures symbols you wish to stream quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>
        """

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

    def level_one_forex(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
            Represents the LEVEL ONE FOREX endpoint for the TD Streaming API. This
            will return quotes for a given list of forex symbols along with specified field information.

            NAME: symbols
            DESC: A List of forex symbols you wish to stream quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>
        """

        # valdiate argument.
        fields = self._validate_argument(
            argument=fields, endpoint='level_one_forex')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'LEVELONE_FOREX'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def level_one_futures_options(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
            Represents the LEVEL ONE FUTURES OPTIONS endpoint for the TD Streaming API. This
            will return quotes for a given list of forex symbols along with specified field information.

            NAME: symbols
            DESC: A List of forex symbols you wish to stream quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>
        """

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

    def news_headline(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
            Represents the NEWS_HEADLINE endpoint for the TD Streaming API. This endpoint
            is used to stream news headlines for different instruments.

            NAME: symbols
            DESC: A List of symbols you wish to stream news for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>         
        """

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

    def timesale(self, service: str, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
            Represents the TIMESALE endpoint for the TD Streaming API. The TIMESALE server ID is used to 
            request Time & Sales data for all supported symbols

            NAME: symbols
            DESC: A List of symbols you wish to stream time and sales data for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings>         
        """

        # valdiate argument.
        fields = self._validate_argument(argument=fields, endpoint='timesale')

        # Build the request
        request = self._new_request_template()
        request['service'] = service
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    """
        EXPERIMENTATION SECTION

        NO GUARANTEE THESE WILL WORK.
    """

    def level_two_quotes(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
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

        """

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

    def level_two_options(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
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

        """

        # valdiate argument.
        fields = self._validate_argument(argument=fields, endpoint='level_two_options')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'OPTIONS_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def level_two_nasdaq(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
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

        """
        # valdiate argument.
        fields = self._validate_argument(argument=fields, endpoint='level_two_nasdaq')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'NASDAQ_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def level_two_total_view(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:

        fields = [str(field) for field in fields]

        # Build the request
        request = self._new_request_template()
        request['service'] = 'TOTAL_VIEW'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    """
        NOT WORKING
    """

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

    def _level_two_opra(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
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

        """

        # Build the request
        request = self._new_request_template()
        request['service'] = 'OPRA'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def _level_two_nyse(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
            EXPERIMENTAL: USE WITH CAUTION!

            Represents the LEVEL_TWO_NYSE endpoint for the streaming API. Documentation on this
            service does not exist, but it appears that we can pass through 1 of 3 fields.

            NAME: symbols
            DESC: A List of symbols you wish to stream time level two quotes for.
            TYPE: List<String>

            NAME: fields
            DESC: The fields you want returned from the Endpoint, can either be the numeric representation
                  or the key value representation. For more info on fields, refer to the documentation.
            TYPE: List<Integer> | List<Strings> 

        """

        fields = [str(field) for field in fields]

        # Build the request
        request = self._new_request_template()
        request['service'] = 'NYSE_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def _level_two_futures_options(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
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

        """

        if fields is not None:
            fields = [str(field) for field in fields]

        # Build the request
        request = self._new_request_template()
        request['service'] = 'FUTURES_OPTIONS_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = symbols
        request['parameters']['fields'] = '0,1,2,3'

        self.data_requests['requests'].append(request)

    def _level_two_futures(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
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

        """

        # valdiate argument.
        fields = self._validate_argument(argument=fields, endpoint='level_two_futures')

        # Build the request
        request = self._new_request_template()
        request['service'] = 'FUTURES_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.data_requests['requests'].append(request)

    def _level_two_forex(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """
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

        """

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
