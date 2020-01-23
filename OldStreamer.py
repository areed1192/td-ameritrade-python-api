import websockets
import asyncio
import pyodbc
import json

class TDStreamerClient():

    def __init__(self, websocket_url = None):
        self.data_holder = []
        self.websocket_url = websocket_url
        

    async def connect(self):
        '''
            Connecting to webSocket server
            websockets.client.connect returns a WebSocketClientProtocol, which is used to send and receive messages
        '''
        
        # define the URI of the data stream, and connect to it.
        uri = "wss://" + self.websocket_url + "/ws"
        self.connection = await websockets.client.connect(uri)
        
        # if all goes well, let the user know.
        if self.connection.open:
            print('Connection established. Client correctly connected')
            return self.connection

    async def sendMessage(self, message):
        '''
            Sending message to webSocket server
        '''
        await self.connection.send(message)
        

    async def receiveMessage(self, connection):
        '''
            Receiving all server messages and handle them
        '''
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