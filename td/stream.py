import asyncio
import datetime
import json
import pprint
import urllib

import dateutil.parser
# import nest_asyncio

import websockets
import asyncio
import pyodbc
import json

class TDStreamerClient():

    def __init__(self, websocket_url = None, user_principal_data = None):

        self.websocket_url = "wss://{}/ws".format(self.websocket_url)
        self.user_principal_data = user_principal_data
        self.connection = ModuleNotFoundError

    def _build_login_request(self):

        # define a request
        login_request = {"requests": [{"service": "ADMIN",
                                       "requestid": "0",  
                                       "command": "LOGIN",
                                       "account": self.user_principal_data['accounts'][0]['accountId'],
                                       "source": self.user_principal_data['streamerInfo']['appId'],
                                       "parameters": {"credential": urllib.parse.urlencode(self.user_principal_data),
                                                      "token": self.user_principal_data['streamerInfo']['token'],
                                                      "version": "1.0"}}]}
        
        return login_request

    def login(self):

        login_request = self._build_login_request()

    async def connect(self):
        '''
            Connecting to webSocket server
            websockets.client.connect returns a WebSocketClientProtocol, 
            which is used to send and receive messages
        '''

        # Create a connection.
        self.connection = await websockets.client.connect(self.websocket_url)

        if self._check_connection():
            return True
    
    def _check_connection(self):

        if self.connection.open:
            print('Connection established. Streaming will begin shortly.')
        else:
            raise ConnectionError

    async def _send_message(self, message = None):
        '''
            Sending message to webSocket server
        '''
        await self.connection.send(message)

    async def receiveMessage(self, connection):
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
                    
                    # grab the data
                    data = message_decoded['data'][0]

                print('-'*20)
                print('Received message from server: ' + str(message))
                
            except websockets.exceptions.ConnectionClosed:            
                print('Connection with server closed')
                break



