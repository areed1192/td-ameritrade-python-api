import asyncio
import datetime
import json
import pprint
import urllib

import dateutil.parser

import websockets
import asyncio
import pyodbc
import json

class TDStreamerClient():

    def __init__(self, websocket_url = None, user_principal_data = None, credentials = None):

        self.websocket_url = "wss://{}/ws".format(websocket_url)
        self.credentials = credentials
        self.user_principal_data = user_principal_data
        self.connection = None
        self.data_requests = {"requests": []}
        self.request = {"service":None, "requestid":None, "command":None, 
                        "account": self.user_principal_data['accounts'][0]['accountId'],
                        "source": self.user_principal_data['streamerInfo']['appId'],
                        "parameters": {"keys": None, "fields":None}}

    def _build_login_request(self):

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
        
        # Grab the login info.
        login_request = self._build_login_request()

        # Grab the Data Request.
        data_request = json.dumps(self.data_requests)

        # Start a loop.
        loop = asyncio.get_event_loop()

        # Start connection and get client connection protocol
        connection = loop.run_until_complete(self._connect())

        # Start listener and heartbeat 
        tasks = [asyncio.ensure_future(self._receive_message(connection)),
                 asyncio.ensure_future(self._send_message(login_request)),
                 asyncio.ensure_future(self._send_message(data_request))]

        # Keep Going.
        loop.run_until_complete(asyncio.wait(tasks))

    async def _connect(self):
        '''
            Connecting to webSocket server
            websockets.client.connect returns a WebSocketClientProtocol, 
            which is used to send and receive messages
        '''

        # Create a connection.
        self.connection = await websockets.client.connect(self.websocket_url)

        if self._check_connection():
            return self.connection
    
    def _check_connection(self):
        '''
            There are multiple times we will need to check the connection of the
            websocket, this function will help do that.
        '''

        if self.connection.open:
            print('Connection established. Streaming will begin shortly.')
            return True
        else:
            raise ConnectionError

    async def _send_message(self, message = None):
        '''
            Sending message to webSocket server

            NAME: message
            DESC: The streaming request you wish to submit.
            TYPE: String
        '''
        await self.connection.send(message)

    async def _receive_message(self, connection):
        '''
            Receiving all server messages and handle them
        '''

        # Keep going until cancelled.
        while True:

            try:

                # grab and decode the message
                message = await connection.recv()                
                message_decoded = json.loads(message)
                
                # check if the response contains a key called data if so then it contains the info we want to insert.
                if 'data' in message_decoded.keys():
                    data = message_decoded['data'][0]

                print('-'*20)
                print('Received message from server: ' + str(message))
                
            except websockets.exceptions.ConnectionClosed:            
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
                await asyncio.sleep(5)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break

    def chart_equity(self, symbols = None, fields = None):

        chart_equity_dict = {'key':0,'open_price':1,'high_price':2,'low_price':3,'close_price':4,'volume':5,'sequence':6,'chart_time':7,'chart_day':8}
        chart_field_nums = [str(chart_equity_dict[field]) for field in fields if field in chart_equity_dict]

        # first get the current service request count
        service_count = len(self.data_requests)

        # Build the request
        chart_equity_request = self.request.copy()
        chart_equity_request['service'] = 'CHART_EQUITY'
        chart_equity_request['requestid'] = service_count
        chart_equity_request['command'] = 'ADD'
        chart_equity_request['parameters']['keys'] = ','.join(symbols)
        chart_equity_request['parameters']['fields'] = ','.join(chart_field_nums)

        self.data_requests['requests'].append(chart_equity_request)


    def actives(self, service = None, venue = None, duration = None):
        
        # first get the current service request count
        service_count = len(self.data_requests)

        # Build the request
        actives_request = self.request.copy()
        actives_request['service'] = service
        actives_request['requestid'] = service_count
        actives_request['command'] = 'SUBS'
        actives_request['parameters']['keys'] = venue + '-' + duration
        actives_request['parameters']['fields'] = '1'

        self.data_requests['requests'].append(actives_request)




